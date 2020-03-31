import textwrap
from cloudmesh.common.console import Console
from dataclasses import dataclass, is_dataclass
import textwrap
import sys, pathlib
from cloudmesh.common.debug import VERBOSE
from docstring_parser import parse


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
        {components}
        """)

    openAPITemplate2 = textwrap.dedent("""
        openapi: 3.0.0
        info:
          title: {title}
          description: {description}
          version: "{version}"
        servers:
          - url: http://localhost/cloudmesh
            description: TODO THIS MUST BE CHANGEABLE
        paths:
          /{baseurl}/{filename}:
             {methods}
        {components}
        """)

    def parse_type(self, _type, ptype):
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

        parser2 = {
            'int': 'type: integer',
            'bool': 'type: boolean',
            'float': 'type: number',
            'str': 'type: string',
            'list': 'type: array items: {}',
            'dict': 'type: object\n       additionalProperties: true'
        }

        if is_dataclass(_type):
            return f'$ref: "#/components/schemas/{_type.__name__}'
        # exits with KeyError if unsupported type is given

        print(ptype)
        if ptype == 1:
            try:
                t = parser[_type]
            except KeyError:
                print(f'unsupported data type supplied for {_type.__name__}:')
                raise Exception
        else:
            try:
                print("got here 2")
                t = parser2[_type]
            except KeyError:
                print(f'unsupported data type supplied for {_type}:')
                raise Exception
        return t

    def generate_parameter(self, name, _type, description):
        """
        function to generate parameters YAMAL contents

        :param name:
        :param _type:
        :param description:
        :return:
        """

        if type(_type) == str:
            _type = self.parse_type(_type, 2)
        else:
            _type = self.parse_type(_type, 1)

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

        # TODO need to figure out how to set up docstring return type correctly so that it's parsable

        if type(_type) == str:
            _type = self.parse_type(_type, 2)
        else:
            _type = self.parse_type(_type, 1)

        str(_type)
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
        return spec

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


    def populate_parameters(self, func_obj):
        """
        Function to loop all the parameters of given function and generate
        specification

        :param function_name:
        :return:
        """
        spec = str()
        print(func_obj.__annotations__)

        if func_obj.__annotations__ and len(func_obj.__annotations__) > 1:
            for parameter, _type in func_obj.__annotations__.items():
                if parameter == 'return':
                    continue  # dicts are unordered, so use continue
                    # intead of break to be safe
                else:
                    spec = spec + self.generate_parameter(
                        parameter,
                        _type,
                        "not yet available, you can read it from docstring")
                    VERBOSE(spec)
        else:  # use docstring_parser.parse to retrieve parameters
            docstring = parse(func_obj.__doc__)
            print(docstring.params)
            for param in docstring.params:
                print(param.arg_name, "::", param.type_name)
                spec = spec + self.generate_parameter(
                    param.arg_name,
                    param.type_name,
                    "not yet available, you can read it from docstring")
                VERBOSE(spec)
        return spec

    def generate_path(self, classname, description, funcname, parameters, responses):
        """
        function to generate path yaml contents

        :param code:
        :param _type:
        :param description:
        :return:
        """

        '''
        spec = textwrap.dedent(f"""
           get:
            summary: {description}
            description: Optional extended description in CommonMark or HTML.
            operationId: {classname}.{funcname}
            parameters:
              {parameters}
            responses:
              {responses}
        """).strip()


        '''
        spec = f"""
                get:
                 summary: {description}
                 description: Optional extended description in CommonMark or HTML.
                 operationId: {classname}.{funcname}
                 parameters:
                   {parameters}
                 responses:
                   {responses}""".strip()

        return textwrap.dedent(spec)

    def generate_openapiClass(self, classname, func_objects, baseurl, outdir, yaml, dataclass_list, write=True):
        """
                function to generate open API of python function.

                :param classname:
                :param func_objects:
                :param baseurl:
                :param outdir:
                :param yaml:
                :param write:
                :return:
                """

        print("Got to openapiClass")

        methods = ""
        description = "TBD"
        version = "1.0"  # TODO:  hard coded for now

        filename = pathlib.Path(next(iter(func_objects.items()))[1].__code__.co_filename).stem

        print("filename: ", filename)
        for k, v in func_objects.items():   # k = function_name, v = function object
            VERBOSE(v)
            func_name = v.__name__
            func_description = v.__doc__.strip().split("\n")[0]
            VERBOSE(func_description)
            VERBOSE(v.__annotations__)
            parameters = self.populate_parameters(v)
            if parameters != "":
                parameters = textwrap.indent(parameters, ' ' * 3)
                VERBOSE(parameters, label="openapi function parameters")
            else:
                Console.info(f"Function {func_name} has no parameters defined in docstring")
                # TODO: handling functions with no input parameters needs additional testing

            # TODO the below response parsing logic only works with annotations but not docstring
            if v.__annotations__:
                return_type = v.__annotations__['return']
            else:
                return_type = parse(v.__doc__).returns

            VERBOSE(return_type)
            responses = self.generate_response('200',
                                               return_type,
                                               'OK')
            responses = textwrap.indent(responses, ' ' * 3)
            VERBOSE(responses, label="openapi function responses")

            methods = methods + self.generate_path(classname, func_description, func_name, parameters, responses)
            methods.strip()
            VERBOSE(methods, label="openapi function method")

        methods = textwrap.indent(methods, ' ' * 5)
        VERBOSE(methods, label="openapi function methods")

        components = ""
        schemas = ""
        if len(dataclass_list) > 0:
            components = textwrap.dedent("""
                      components:
                        schemas:
                          """)
            for dc in func['dataclass_list']:
                schemas = schemas + textwrap.indent(self.generate_schema(dc), ' ' * 6)
        VERBOSE(components, label="openapi function components")

        spec = self.openAPITemplate2.format(
            title=classname,
            description=description,
            version=version,
            methods=methods.strip(),
            baseurl=baseurl,
            filename=filename,
            components=components.strip()
        )

        print(spec)

        if write:
            try:
                if yaml != "" and yaml is not None:
                    version = open(f"{outdir}/{yaml}.yaml", 'w').write(spec)
                else:
                    version = open(f"{outdir}/{classname}.yaml", 'w').write(spec)
            except IOError:
                Console.error("Unable to write yaml file")
            except Exception as e:
                print(e)

        return

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
        if parameters != "":
            parameters = textwrap.indent(parameters, ' ' * 8)
            VERBOSE(parameters, label="openapi function parameters")
        else:
            Console.info(f"Function {title} has no parameters defined in docstring")
            # TODO: handling functions with no input parameters needs additional testing

        responses = self.generate_response('200',
                                           f.__annotations__['return'],
                                           'OK')
        responses = textwrap.indent(responses, ' ' * 8)
        VERBOSE(responses, label="openapi function responses")

        components = ''
        if len(dataclass_list) > 0:
            components = textwrap.dedent("""
              components:
                schemas:
                  """)
            for dc in dataclass_list:
                schemas = schemas + textwrap.indent(self.generate_schema(dc), ' ' * 6)

        VERBOSE(components, label="openapi function components")

        # TODO: figure out where to define dataclasses and how
        #  best to pass them to generate_schema()
        filename = pathlib.Path(f.__code__.co_filename).stem
        spec = self.openAPITemplate.format(
            title=title,
            name=f.__name__,
            description=description,
            version=version,
            parameters=parameters.strip(),
            responses=responses.strip(),
            baseurl=baseurl,
            filename=filename,
            components=components
        )

        if write:
            try:
                if yaml != "" and yaml is not None:
                    version = open(f"{outdir}/{yaml}.yaml", 'w').write(spec)
                else:
                    version = open(f"{outdir}/{title}.yaml", 'w').write(spec)
            except IOError:
                Console.error("Unable to write yaml file")
            except Exception as e:
                print(e)

        return
