import textwrap
from cloudmesh.common.console import Console
from dataclasses import dataclass, is_dataclass
import textwrap


# TODO: docstrings comments missing
# TODO: description missing
# TODO: why are we not using the latest version of openapi?
# TODO: why are we not using Inspect code from pyCharm?
# TODO: why are we not using Code Format from pyCharm?

class Generator:
    openAPITemplate = textwrap.dedent("""
        openapi: 3.0.0
        info:
          title: {title}
          description: {description}
          version: "{version}"
        servers:
          - url: http://localhost/cloudmesh
            description: TODO THIS MUST BE CHANGEABLE
        paths:
          /{baseurl}:
             get:
              summary: {description}
              description: Optional extended description in CommonMark or HTML.
              operationId: {filename}.{name}
              parameters:
                {parameters}
              responses:
                {responses}
        
        components:
          schemas:
            {schemas}
        """)

    def parse_type(self, _type):
        """
        function to parse supported openapi3 data types

        :param _type:
        :return:
        """
        parser = {
            int: 'type: integer',
            bool: 'type: boolean',
            float: 'type: number',
            str: 'type: string',
            list: 'type: array\nitems: {}',
            dict: 'type: object\nadditionalProperties: true'
        }
        if is_dataclass(_type):
            return f'$ref: "#/components/schemas/{_type.__name__}'
        # exits with KeyError if unsupported type is given
        try:
            t = parser[_type]
        except KeyError:
            print(f'unsupported data type supplied for {_type.__name__}:')
            print(_type)
            raise
        return t

    def generate_parameter(self, name, _type, description):
        """
        function to generate parameters YAMAL contents

        :param name:
        :param _type:
        :param description:
        :return:
        """
        _type = self.parse_type(_type)
        spec = textwrap.dedent(f"""
            - in: query
              name: {name}
              description: {description}
              schema:
                {_type}""")
        return spec

    def generate_response(self, code, _type, description):
        """
        function to generate response yaml contents

        :param code:
        :param _type:
        :param description:
        :return:
        """
        _type = self.parse_type(_type)
        if not _type.startswith('object'):
            # int, bool, float, str, list
            spec = textwrap.dedent(f"""
              '{code}':
                description: {description}
                content:
                  text/plain:
                    schema:
                      {_type}""")
        else:
            # dict (generic json) or dataclass ($ref)
            spec = textwrap.dedent(f"""
              '{code}':
                description: {description}
                content:
                  application/json:
                    schema:
                      {_type}""")
        return spec

    def generate_properties(self, attr, _type):
        """
        function to generate properties of a schema

        :param attr:
        :param _type:
        :return:
        """
        _type = self.parse_type(_type)
        spec = textwrap.dedent(f"""
          {attr}:
            {_type}""")

    def generate_schema(self, _class):
        """
        function to generate schema in the components section from @dataclass
        attributes

        :param _class:
        :return:
        """
        class_name = _class.__name__
        if not is_dataclass(_class):
            raise TypeError(
                f'{class_name} is not a dataclass. '
                'Use the @dataclass decorator to define the class properly')
        properties = str()
        for attr, _type in _class.__annotations__.items():
            properties = properties + self.generate_properties(attr, _type)
        spec = textwrap.dedent(f"""
          {class_name}:
            type: object
            properties:
              {properties}""")

    def populate_parameters(self, function_name):
        """
        Function to loop all the parameters of given function and generate
        specification

        :param function_name:
        :return:
        """
        spec = str()
        for parameter, _type in function_name.__annotations__.items():
            if parameter == 'return':
                continue  # dicts are unordered, so use continue
                # intead of break to be safe
            else:
                spec = spec + self.generate_parameter(
                    parameter,
                    _type,
                    "not yet available, you can read it from docstring")
        return spec

    def generate_openapi(self, f, baseurl, outdir, yaml, dataclass_list, write=True):
        """
        function to generate open API of python function.

        :param f:
        :param baseurl:
        :param outdir:
        :param yaml:
        :param write:
        :return:
        """
        description = f.__doc__.strip().split("\n")[0]
        version = "1.0"  # TODO:  hard coded for now
        title = f.__name__
        parameters = self.populate_parameters(f)
        parameters = textwrap.indent(parameters, ' ' * 8)
        responses = self.generate_response('200',
                                           f.__annotations__['return'],
                                           'OK')
        responses = textwrap.indent(responses, ' ' * 8)
        
        schemas = ''
        # shouldn't do anything if the list is empty
        for dc in dataclass_list:
            schemas = schemas + self.generate_schema(dc)

        # TODO: figure out where to define dataclasses and how
        #  best to pass them to generate_schema()
        filename = f.__code__.co_filename.strip().split("\\")[-1].split(".")[0]
        spec = self.openAPITemplate.format(
            title=title,
            name=f.__name__,
            description=description,
            version=version,
            parameters=parameters.strip(),
            responses=responses.strip(),
            baseurl=baseurl,
            filename=filename,
            schemas=schemas
        )

        # return code
        rc = 0

        if write:
            try:
                if yaml != "" and yaml is not None:
                    version = open(f"{outdir}/{yaml}.yaml", 'w').write(spec)
                else:
                    version = open(f"{outdir}/{title}.yaml", 'w').write(spec)
            except IOError:
                Console.error("Unable to write yaml file")
                rc = 1
            except Exception as e:
                print(e)
                rc = 1

        return rc
