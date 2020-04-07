from __future__ import print_function

import yaml
from cloudmesh.common.util import path_expand
from cloudmesh.shell.command import PluginCommand
from cloudmesh.shell.command import command, map_parameters

from cloudmesh.openapi.api.server import Server
from cloudmesh.common.console import Console
from cloudmesh.common.debug import VERBOSE

from cloudmesh.openapi.api.manager import Manager, OpenAPIMarkdown


class OpenapiCommand(PluginCommand):

    # noinspection PyUnusedLocal
    @command
    def do_openapi(self, args, arguments):
        """
        ::

          Usage:
              openapi merge [SERVICES...] [--dir=DIR] [--verbose]
              openapi list [--dir=DIR]
              openapi description [SERVICES...] [--dir=DIR]
              openapi md FILE [--indent=INDENT]
              openapi codegen [SERVICES...] [--srcdir=SRCDIR]
                              [--destdir=DESTDIR]
              openapi server start YAML [--directory=DIRECTORY]
                             [--port=PORT] [--server=SERVER] [--verbose]
              openapi server stop YAML

          Arguments:
              DIR   The directory of the specifications
              FILE  The specification
              SRCDIR   The directory of the specifications
              DESTDIR  The directory where the generated code should be put

          Options:
              --verbose              specifies to run in debug mode [default: False]
              --port=PORT            the port for the server [default: 8080]
              --directory=DIRECTORY  the directory in which the server is run [default: ./]
              --server=SERVER        teh server [default: flask]
          Description:
            This command does some useful things.


        """

        map_parameters(arguments,
                       'verbose',
                       'port',
                       'directory')
        arguments.debug = arguments.verbose
        arguments.wsgi = arguments["--server"]

        VERBOSE(arguments)

        m = Manager(debug=arguments.debug)

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

        elif arguments.server and arguments.start:

            try:
                s = Server(
                    spec=arguments.YAML,
                    directory=arguments.directory,
                    port=arguments.port,
                    server=arguments.wsgi,
                    debug=arguments.debug)

                s._run()

            except FileNotFoundError:

                Console.error("specification file not found")

            except Exception as e:
                print(e)

        elif arguments.server and arguments.stop:

            print("implement me")

        return ""
