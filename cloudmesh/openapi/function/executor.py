import os
import sys
import textwrap

from cloudmesh.common.console import Console
from cloudmesh.common.util import path_expand


class Parameter:
    """
    To generate a useful output for the variables. Example:

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
            - Server url: http://localhost:8080/cloudmesh
            - Module:     calculator

    """

    def __init__(self, arguments):
        self.arguments = arguments
        self.filename = None
        self.module_directory = None
        self.module_name = None
        self.yamlfile = None
        self.yamldirectory = None
        self.function = None
        self.serverurl = None
        self.import_class = None
        self.all_functions = None
        self.basic_auth = None
        self.get(arguments)
        pass

    def get(self, arguments):
        self.cwd = path_expand(os.path.curdir)
        filename = arguments['--filename']
        if filename is None:
            Console.error(f"--filename={filename}")
        self.filename = path_expand(filename)
        if not os.path.isfile(filename):
            Console.error(f"--filename={self.filename} does not exist")
        
        self.module_directory = os.path.dirname(self.filename)
        self.module_name = os.path.basename(self.filename).split('.')[0]
        sys.path.append(self.module_directory)

        self.yamlfile = arguments.yamlfile or self.filename.rsplit(".py")[0] + ".yaml"
        self.yamldirectory = os.path.dirname(self.yamlfile)

        self.function = arguments.FUNCTION or os.path.basename(self.filename).split('.')[0]
        self.serverurl = arguments.serverurl or "http://localhost:8080/cloudmesh"
        self.import_class = arguments.import_class or False
        self.all_functions =arguments.all_functions or False
        self.basic_auth = arguments.basic_auth

        
    def Print(self):

        Console.info(textwrap.dedent(f"""
             Cloudmesh OpenAPI Generator:

               File Locations:
                 - Currdir:    .
                 - Filename:   {self.filename.replace(self.cwd, ".")}
                 - YAML:       {self.yamlfile.replace(self.cwd, ".")}

               Yaml File Related:
                 - Function:   {self.function}
                 - Server url: {self.serverurl}
                 - Module:     {self.module_name}

         """))
