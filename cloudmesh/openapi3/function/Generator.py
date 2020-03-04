import textwrap

class Generator:
    openAPITemplate = """
openapi: 3.0.0
info:
  title: {title}
  description: {description}
  version: "{version}"
servers:
  - url: http://localhost/cloudmesh
    description: Optional server description, e.g. Main (production) server
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
"""

    def parse_type(self,_type):
        """function to parse supported openapi3 data types"""
        parser = {
                int: 'integer',
                bool: 'boolean',
                float: 'number',
                str: 'string',
                list: 'array\nitems: {}',
                dict: 'object\nadditionalProperties: true',
                }
        # exits with KeyError if unsupported type is given
        try:
            t=parser[_type]
        except KeyError:
            print('unsupported data type supplied:')
            print(_type)
            raise
        return t

    def generate_parameter(self, name, _type, description):
        """ function to generate parameters YAMAL contents"""
        _type = self.parse_type(_type)
        spec = textwrap.dedent(f"""
            - in: query
              name: {name}
              schema:
                type: {_type}
              description: {description}""")
        return spec

    def generate_response(self, code, _type, description):
        """function to generate response yaml contents"""
        _type = self.parse_type(_type)
        if not _type.startswith('object'):
            # int, bool, float, str, list
            spec = textwrap.dedent(f"""
              '{code}':
                description: {description}
                content:
                  text/plain:
                    schema:
                      type: {_type}""")
        else:
            # dict (generic json)
            spec = textwrap.dedent(f"""
              '{code}':
                description: {description}
                content:
                  application/json:
                    schema:
                      type: {_type}""")
        return spec
            

    def populateParameters(self,functionName):
        """ Function to loop all the parameters of given function and generate specification"""
        spec = str()
        for parameter, _type in functionName.__annotations__.items():
            if parameter == 'return':
                continue # dicts are unordered, so use continue intead of break to be safe
            else:
                spec = spec + self.generate_parameter(parameter, _type, "not yet available, you can read it from docstring")
        return spec
    
    def generate_openapi(self, f, baseurl, outdir, write=True):
        """ function to generate open API of python function."""
        description = f.__doc__.strip().split("\n")[0]
        version = "1.0"  # TODO:  hard coded for now
        title = f.__name__
        parameters = self.populateParameters(f)
        parameters = textwrap.indent(parameters, ' ' * 8)
        responses = self.generate_response('200', f.__annotations__['return'], 'OK')
        responses = textwrap.indent(responses, ' ' * 8)

        spec = self.openAPITemplate.format(
            title=title,
            name=f.__name__,
            description=description,
            version=version,
            parameters=parameters.strip(),
            responses=responses.strip(),
            baseurl=baseurl,
            filename=f.__code__.co_filename.strip().split(".")[0]
        )

        if write:
            version = open(f"{outdir}/{title}.yaml", 'w').write(spec)

        return spec
