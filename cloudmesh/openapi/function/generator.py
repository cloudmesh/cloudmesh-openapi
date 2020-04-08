import pathlib
import textwrap
from dataclasses import is_dataclass

import requests
from cloudmesh.common.console import Console
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
            description: {description}
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
            description: {description}
        paths:
          {paths}
        {components}
        """)

    def parse_type(self, _type):
        """
        function to parse supported openapi data types

        :param _type:
        :return:
        """

        parser = {
            'int': 'type: integer',
            'bool': 'type: boolean',
            'float': 'type: number',
            'str': 'type: string',
            'list': 'type: array\n          items: {}',
            'dict': 'type: object\n         additionalProperties: true'
        }

        if is_dataclass(_type):
            return f'$ref: "#/components/schemas/{_type}'
        # exits with KeyError if unsupported type is given

        try:
            t = parser[_type]
        except KeyError:
            print(f'unsupported data type supplied for {_type}')
            raise Exception
        return t

    def generate_parameter(self, name, _type, description):
        """
        function to generate parameters YAML contents

        :param name:
        :param _type:
        :param description:
        :return:
        """

        if type(_type) == str:
            _type = self.parse_type(_type)
        else:
            _type = self.parse_type(_type.__name__)

        spec = textwrap.dedent("""
            - in: query
              name: {name}
              description: {description}
              schema:
                {_type}""").format(name=name.strip(),
                                   description=description.strip(),
                                   _type=_type.strip())

        return spec

    def generate_response(self, code, _type, description):
        """
        function to generate response yaml contents

        :param code:
        :param _type:
        :param description:
        :return:
        """

        # TODO need to figure out how to set up docstring return type correctly
        #   so that it's parsable

        if type(_type) == str:
            _type = self.parse_type(_type)
        else:
            _type = self.parse_type(_type.__name__)

        if not _type.startswith('object'):
            # int, bool, float, str, list
            spec = textwrap.dedent("""
              '{code}':
                description: {description}
                content:
                  text/plain:
                    schema:
                      {_type}""").format(code=code.strip(),
                                         description=description.strip(),
                                         _type=_type.strip())
        else:
            # dict (generic json) or dataclass ($ref)
            spec = textwrap.dedent("""
              '{code}':
                description: {description}
                content:
                  application/json:
                    schema:
                      {_type}""").format(code=code.strip(),
                                         description=description.strip(),
                                         _type=_type.strip())
        return spec

    def generate_properties(self, attr, _type):
        """
        function to generate properties of a schema

        :param attr:
        :param _type:
        :return:
        """

        if type(_type) == str:
            _type = self.parse_type(_type)
        else:
            _type = self.parse_type(_type.__name__)

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
        return spec

    def populate_parameters(self, func_obj):
        """
        Function to loop all the parameters of given function and generate
        specification

        :param func_obj:
        :return:
        """
        spec = str()
        description = None
        for parameter, _type in func_obj.__annotations__.items():
            if parameter == 'return':
                continue  # dicts are unordered, so use continue
                # intead of break to be safe
            else:

                # TODO: used dosctring_parser package for now.  But this
                #   requires pip install.  Consider alternatives.

                docstring = parse(func_obj.__doc__)
                print(docstring.params)
                for param in docstring.params:
                    if param.arg_name == parameter:
                        description = param.description.strip()
                spec = spec + self.generate_parameter(
                    parameter,
                    _type,
                    description if description else "no description provided in docstring")
                VERBOSE(spec)

        return spec

    def generate_path(self,
                      class_name=None,
                      description=None,
                      long_description=None,
                      funcname=None,
                      parameters=None,
                      responses=None,
                      filename=None,
                      all_function=None):
        """
        function to generate path yaml contents

        :param class_name:
        :param description:
        :param long_description:
        :param funcname:
        :param parameters:
        :param responses:
        :param filename:
        :param all_function:
        :return:
        """

        l_description = long_description \
            if long_description != None \
            else 'None (Optional extended description in CommonMark or HTML)'

        if all_function:
            operationId = f"{filename}.{funcname}"
        else:
            operationId = f"{filename}.{class_name}.{funcname}"

        spec = textwrap.dedent("""
            /{class_name}/{funcname}:
               get:
                summary: {description}
                description: {l_description}
                operationId: {operationId}
                parameters:
                  {parameters}
                responses:
                  {responses}
        """).format(
            description=description,
            l_description=l_description,
            class_name=class_name,
            funcname=funcname,
            parameters=parameters.strip(),
            responses=responses.strip(),
            operationId=operationId
        )

        return spec

    def generate_openapi_class(self,
                               class_name=None,
                               class_description=None,
                               filename=None,
                               func_objects=None,
                               baseurl=None,
                               outdir=None,
                               yaml=None,
                               dataclass_list=None,
                               all_function=False,
                               write=True):
        """
        function to generate open API of python function.

        :param class_name:
        :param class_description:
        :param filename:
        :param func_objects:
        :param baseurl:
        :param outdir:
        :param yaml:
        :param dataclass_list:
        :param all_function:
        :param write:
        :return:
        """

        # Initializing and setting global variables
        paths = ""
        description = class_description \
            if class_description \
            else "No description found"
        version = "1.0"  # TODO:  hard coded for now

        # Loop through all functions
        for k, v in func_objects.items():   # k = function_name, v = function object
            VERBOSE(v)
            func_name = v.__name__

            # func_description = v.__doc__.strip().split("\n")[0]
            docstring = parse(v.__doc__)
            func_description = docstring.short_description
            func_ldescription = docstring.long_description

            VERBOSE(func_description)
            VERBOSE(func_ldescription)

            # TODO: handling functions with no input parameters and no return
            # value needs additional testing

            if v.__annotations__:
                Console.info("Annotations found for function...processing")
            else:
                Console.error(f"No annotations found for function '{func_name}'")
                raise Exception

            # Define parameters section(s) for openapi yaml
            parameters = self.populate_parameters(v)
            if parameters != "":
                parameters = textwrap.indent(parameters, ' ' * 6)
                VERBOSE(parameters, label="openapi function parameters")
            else:
                Console.info(f"Function {func_name} has no parameters "
                             "defined in docstring")

            # Define responses section(s) for openapi yaml
            responses = self.generate_response('200',
                                               v.__annotations__['return'],
                                               'OK')
            responses = textwrap.indent(responses, ' ' * 6)
            VERBOSE(responses, label="openapi function responses")

            # Define paths section(s) for openapi yaml
            paths = paths + self.generate_path(class_name,
                                               func_description,
                                               func_ldescription,
                                               func_name,
                                               parameters,
                                               responses,
                                               filename,
                                               all_function)

            VERBOSE(paths, label="openapi function path")

        # Indent full paths section for openapi yaml
        paths = textwrap.indent(paths, ' ' * 2)
        VERBOSE(paths, label="openapi function paths")

        # Define components section(s) for openapi yaml
        components = ""
        schemas = ""
        if len(dataclass_list) > 0:
            components = textwrap.dedent("""
                      components:
                        schemas:
                          """)
            for dc in dataclass_list:
                schemas = schemas + textwrap.indent(self.generate_schema(dc), ' ' * 6)
        VERBOSE(components, label="openapi function components")

        # Update openapi template to create final version of openapi yaml
        spec = self.openAPITemplate2.format(
            title=class_name,
            description=description,
            version=version,
            paths=paths.strip(),
            baseurl=baseurl,
            filename=filename,
            components=components.strip()
        )

        # Write openapi yaml to file
        if write:
            try:
                if yaml != "" and yaml is not None:
                    version = open(f"{outdir}/{yaml}.yaml", 'w').write(spec.strip())
                else:
                    version = open(f"{outdir}/{class_name}.yaml", 'w').write(spec.strip())
            except IOError:
                Console.error("Unable to write yaml file")
            except Exception as e:
                print(e)

        return

    def generate_openapi(self,
                         f=None,
                         baseurl=None,
                         outdir=None,
                         yaml=None,
                         dataclass_list=None,
                         write=True):
        """
        function to generate open API of python function.

        :param f:
        :param baseurl:
        :param outdir:
        :param yaml:
        :param dataclass_list:
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
        schemas = ''
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

    #we have to test below functions
    def file_put(root_url, service, filename, verbose=False):

        url = f'http://{root_url}/cloudmesh/{service}/file/put'
        print("URL", url)
        files = {'file': open(filename, 'rb')}
        r = requests.post(url, files=files)
        return r.text

    def file_list(root_url):
        r = requests.get(f'http://{root_url}/file/list')
        return r.text

    def file_get(root_url, service, filename):

        url = f'http://{root_url}/cloudmesh/{service}/file/get/{filename}'

        print("URL", url)

        r = requests.get(url)
        return r.text
