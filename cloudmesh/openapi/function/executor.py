import os
import sys
import textwrap

from cloudmesh.common.console import Console
from cloudmesh.common.util import path_expand


class Parameter:
    """
    To generat a useful output for the variables. Example:

        from cloudmesh.openapi.function.executor import Parameter
        p = Parameter(arguments)
        p.Print()

    Invocation from program

        cd cloudmesh-openapi
        cms openapi generate calculator  \
            --filename=./tests/generator-calculator/calculator.py \
            --all_functions

    Returns

        Cloudmesh OpenAPI Generator:

          File Locations:
            - Currdir:    .
            - Directory:  ./tests/generator-calculator
            - Filename:   ./tests/generator-calculator/calculator.py
            - YAML:       ./tests/generator-calculator/calculator.yaml

          Yaml File Related:
            - Function:   calculator
            - Servereurl: http://localhost:8080/cloudmesh
            - Module:     None

    """

    def __init__(self, arguments):
        self.arguments = arguments
        self.filename = None
        self.yamlfile = None
        self.directory = None
        self.function = None
        self.serverurl = None
        self.module_name = None
        self.get(arguments)
        pass

    def get(self, arguments):

        self.cwd = path_expand(os.path.curdir)

        filename = arguments.filename

        if filename is None:
            Console.error(f"--filename={filename}")
        self.filename = path_expand(filename)
        if not os.path.isfile(filename):
            Console.error(f"--filename={self.filename} does not exist")

        self.yamlfile = self.yamlfile or self.filename.rsplit(".py")[
            0] + ".yaml"
        self.directory = arguments.dir or os.path.dirname(self.filename)

        self.function = arguments.FUNCTION or os.path.basename(
            self.filename).stem
        self.serverurl = arguments.serverurl or "http://localhost:8080/cloudmesh"

        print(sys.path)
        sys.path.append(self.directory)
        print(sys.path)

        # imported_module = importlib(self.function)

        # func_obj = getattr(imported_module, function)

    def Print(self):

        Console.info(textwrap.dedent(f"""
             Cloudmesh OpenAPI Generator:

               File Locations:
                 - Currdir:    .
                 - Directory:  {self.directory.replace(self.cwd, ".")}
                 - Filename:   {self.filename.replace(self.cwd, ".")}
                 - YAML:       {self.yamlfile.replace(self.cwd, ".")}

               Yaml File Related:
                 - Function:   {self.function}
                 - Servereurl: {self.serverurl}
                 - Module:     {self.module_name}

         """))
