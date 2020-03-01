import textwrap

class Generator:
    openAPITemplate = """
openapi: 3.0.0
info:
  title: {title}
  description: {description}
  version: "{version}"
servers:
  - url: http://localhost/cloudmesh/{title}
    description: Optional server description, e.g. Main (production) server
paths:
  /{name}:
     get:
      summary: {description}
      description: Optional extended description in CommonMark or HTML.
      operationId: {name}
      responses:
        '200':    # status code
          description: {description}
          content:
            text/plain:
              schema: 
                type: {return_type}
      parameters:
        {parameters} 
"""

    def parse_type(self,_type):
        parser = {
                int: 'integer',
                bool: 'boolean',
                float: 'float',
                str: 'str',
                list: textwrap.dedent('array\nitems: {}')
                }
        try:
            t=parser[_type]
        except KeyError:
            t='object'
        return t

    def generate_parameter(self, name, _type, description):
        """ function to generate parameters YAMAL contents"""
        spec = textwrap.dedent(f"""
            - in: query
              name: {name}
              schema:
                type: {_type}
              description: {description}""")
        return spec

    def populateParameters(self,functionName):
        """ Function to loop all the parameters of given function and generate specification"""
        spec = str()
        for parameter, _type in functionName.__annotations__.items():
            if parameter == 'return':
                break
            else:
                spec = spec + self.generate_parameter(parameter, parse_type(_type), "not yet available, you can read it from docstring")
        return spec
    
    def generate_openapi(self, f, write=True):
        """ function to generate open API of python function."""
        description = f.__doc__.strip().split("\n")[0]
        version = "1.0"  # hard coded for now
        title = f.__name__
        return_type = parse_type(f.__annotations__['return'])
        parameters = self.populateParameters(f)
        parameters = textwrap.indent(parameters, ' ' * 8)
        spec = self.openAPITemplate.format(
            title=title,
            name=f.__name__,
            description=description,
            version=version,
            return_type=return_type,
            parameters=parameters.strip()
        )

        if write:
            version = open(f"{title}.yaml", 'w').write(spec)

        return spec
