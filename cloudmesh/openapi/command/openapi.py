from __future__ import print_function

import yaml
from cloudmesh.common.util import path_expand
from cloudmesh.shell.command import PluginCommand
from cloudmesh.shell.command import command

from cloudmesh.openapi.api.manager import Manager, OpenAPIMarkdown


class OpenapiCommand(PluginCommand):

    # noinspection PyUnusedLocal
    @command
    def do_openapi(self, args, arguments):
        """
        ::

          Usage:
                openapi merge [SERVICES...] [--dir=DIR]
                openapi list [--dir=DIR]
                openapi description [SERVICES...] [--dir=DIR]
                openapi md FILE [--indent=INDENT]
                openapi codegen [SERVICES...] [--srcdir=SRCDIR]
                                [--destdir=DESTDIR]

          This command does some useful things.

          Arguments:
              DIR   The directory of the specifications
              FILE  The specification
              SRCDIR   The directory of the specifications
              DESTDIR  The directory where the generated code should be put

          Options:
              -f      specify the file

        """

        m = Manager()

        arguments.dir = path_expand(arguments["--dir"] or ".")

        # pprint(arguments)

        if arguments.list:
            files = m.get(arguments.dir)
            print("List of specifications")
            print(79 * "=")
            print('\n'.join(files))

        elif arguments.merge:
            d = m.merge(arguments.dir, arguments.SERVICES)
            print(yaml.dump(d, default_flow_style=False))

        elif arguments.description:
            d = m.description(arguments.dir, arguments.SERVICES)

        elif arguments.md:

            converter = OpenAPIMarkdown()

            if arguments["--indent"] is None:
                indent = 1
            else:
                indent = int(arguments["--indent"])
            filename = arguments["FILE"]

            converter.title(filename, indent=indent)
            converter.convert_definitions(filename, indent=indent + 1)
            converter.convert_paths(filename, indent=indent + 1)
        elif arguments.codegen:
            m.codegen(arguments.SERVICES, arguments.dir)
        return ""
