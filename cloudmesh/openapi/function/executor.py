import os
import textwrap
from pathlib import Path

from cloudmesh.common.console import Console
from cloudmesh.common.util import path_expand


class Parameter:

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

        filename = arguments.filename

        if filename is None:
            Console.error(f"--filename={filename}")
        self.filename = path_expand(filename)
        if not os.path.isfile(filename):
            Console.error(f"--filename={filename} does not exist")
        self.yamlfile = self.yamlfile or self.filename.rsplit(".")[1] + ".yaml"
        self.directory = arguments.dir or Path(filename).stem

        self.function = arguments.FUNCTION or os.path.basename(filename).stem
        self.serverurl = arguments.serverurl or "http://sample.org/cloudmesh/"

    def Print(self):

        Console.info(textwrap.dedent(f"""
             Cloudmesh OpenAPI Generator:

               File Locations:
                 - Directory:  {self.directory}
                 - Filename:   {self.filename}
                 - YAML:       {self.yamlfile}

               Yaml File Related:
                 - Function:   {self.function}
                 - Servereurl: {self.serverurl}
                 - Module:     {self.module_name}

         """))
