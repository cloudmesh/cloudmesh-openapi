from __future__ import print_function
from cloudmesh.shell.command import command
from cloudmesh.shell.command import PluginCommand
from cloudmesh.openapi.api.manager import Manager
from cloudmesh.common.console import Console
from cloudmesh.common.util import path_expand
from pprint import pprint
import yaml


class OpenapiCommand(PluginCommand):

    # noinspection PyUnusedLocal
    @command
    def do_openapi(self, args, arguments):
        """
        ::

          Usage:
                openapi merge [SERVICES...] [--dir=DIR]
                openapi list [--dir=DIR]

          This command does some useful things.

          Arguments:
              DIR   a file name

          Options:
              -f      specify the file

        """

        m = Manager()

        arguments.dir = path_expand(arguments["--dir"] or ".")

        pprint(arguments)

        if arguments.list:
            files = m.get(arguments.dir)
            print("List of specifications")
            print(79 * "=")
            print('\n'.join(files))

        elif arguments.merge:
            d = m.merge(arguments.dir, arguments.SERVICES)
            print(yaml.dump(d, default_flow_style=False))

        return ""
