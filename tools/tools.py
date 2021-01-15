"""Tools
Usage:
    tools.py list
    tools.py table
"""

from cloudmesh.common.util import download
from cloudmesh.common.util import readfile
import oyaml as yaml
from pprint import pprint
from docopt import docopt

categories_yaml = "https://raw.githubusercontent.com/apisyouwonthate/openapi.tools/master/_data/categories.yml"
tools_yaml = "https://raw.githubusercontent.com/apisyouwonthate/openapi.tools/master/_data/tools.yml"

download(categories_yaml, "categories.yml")
download(tools_yaml, "tools-orig.yml")

categories = yaml.load(readfile("categories.yml"), Loader=yaml.SafeLoader)

pprint (categories)


tools = yaml.load(readfile("tools.yml"),  Loader=yaml.SafeLoader)

print (tools)

def get(attribute):
    l = list()
    for tool in tools:
        l.append(tool[attribute])
    return l


def table():

    print("\\begin{table}[htb]")
    print("\\begin{tabular}{lllllll}")
    attributes = [
          "name",
          "category",
          "language",
          "v2",
          "v3"
          "github",
          "description",
    ]

    for tool in tools:
        line = ""
        for a in attributes:
            v = str(tool.get(a) or "")
            if a == "github" and v != "":
                v = " & \\href{" + v + "}{GitHub}"
            line = line + v + " & "
        line = line + "\\\\"
        line = line.replace(" & \\", " \\")

        print (line)
    print("\\end{tabular}")
    print("\\end{table}")


if __name__ == '__main__':
    arguments = docopt(__doc__, version='DEMO 1.0')
    if arguments['list']:
        print ("\n".join(get('name')))
    if arguments['table']:
        table()

    else:
        print(arguments)
