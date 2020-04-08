import textwrap


def a(x: int, y: float) -> int:
    """
    A sample.

    :param x: x value
    :type x: int
    :param y: y value
    :type y: float
    :return: result
    :return type: int
    """
    return 1


# help(a)

func = a

print()
counter = 1
for f in [
    func.__name__,
    func.__code__.co_argcount,
    func.__code__.co_varnames,
    func.__code__.co_cellvars,
    func.__code__.co_code,
    func.__code__.co_consts,
    func.__code__.co_filename,
    func.__code__.co_firstlineno,
    func.__code__.co_flags,
    func.__code__.co_freevars,
    func.__code__.co_kwonlyargcount,
    func.__code__.co_lnotab,
    func.__code__.co_name,
    func.__code__.co_names,
    func.__code__.co_nlocals,
    func.__code__.co_posonlyargcount,
    func.__code__.co_stacksize,
    func.__code__.co_varnames,
    func.__doc__]:
    print(counter, f)
    counter += 1

print(func.__annotations__)

template = """
openapi: 3.0.0
info:
  title: {title}
  description: {description}
  version: {version}
servers:
  - url: http://localhost/cloudmesh/{title}
    description: Optional server description, e.g. Main (production) server
paths:
  /{name}:
     get:
        ....
  /users:
    get:
      summary: Returns a list of users.
      description: Optional extended description in CommonMark or HTML.
      responses:
        '200':    # status code
          description: A JSON array of user names
          content:
            application/json:
              schema: 
                type: array
                items: 
                  type: string
"""


def generate_parameter(name, _type, description):
    spec = textwrap.dedent(f"""
        - in: query
          name: {name}
          schema:
            type: {_type}
          description: {description} 
    
    """)
    return spec


def generate_openapi(f, write=True):
    description = f.__doc__.strip().split("\n")[0]
    version = open('../VERSION', 'r').read()
    title = f.__name__

    spec = template.format(
        title=title,
        name=f.__name__,
        description=description,
        version=version
    )

    if write:
        version = open(f"{title}.yaml", 'w').write(spec)

    return spec


spec = generate_openapi(func)

print(spec)

for parameter, _type in func.__annotations__.items():
    if parameter == "return":
        break
    print(parameter, _type)
    if _type == int:
        _type = 'integer'
    elif _type == bool:
        _type = 'boolean'
    elif _type == float:
        _type = 'float'
    else:
        _type = 'unkown'

    spec = generate_parameter(
        parameter, _type,
        "not yet available, you can read it from docstring")
    print(spec)
