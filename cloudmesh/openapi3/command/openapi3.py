import pathlib
import sys
from dataclasses import is_dataclass
from importlib import import_module

from cloudmesh.common.Printer import Printer
from cloudmesh.common.console import Console
from cloudmesh.common.debug import VERBOSE
from cloudmesh.common.util import path_expand
from cloudmesh.openapi3.function import generator
from cloudmesh.openapi3.function.server import Server
from cloudmesh.openapi3.registry.Registry import Registry
from cloudmesh.shell.command import PluginCommand
from cloudmesh.shell.command import command, map_parameters


# start-stop: osx Andrew
# start_stop: windows Jonathan
# start-stop: linux Prateek


class Openapi3Command(PluginCommand):

    # noinspection PyUnusedLocal,PyPep8Naming
    @command
    def do_openapi3(self, args, arguments):
        """
        ::

          Usage:
              openapi3 generate FUNCTION [YAML]
                                         --baseurl=BASEURL
                                         --filename=FILENAME
                                         --yamldirectory=DIRECTORY
                                         [--verbose]
              openapi3 server start YAML [NAME]
                              [--directory=DIRECTORY]
                              [--port=PORT]
                              [--server=SERVER]
                              [--verbose]
                              [--debug]
                              [--fg]
                              [--os]
              openapi3 server stop NAME
              openapi3 server list [NAME] [--output=OUTPUT]
              openapi3 server ps [NAME] [--output=OUTPUT]
              openapi3 register add NAME ENDPOINT
              openapi3 register filename NAME
              openapi3 register delete NAME
              openapi3 register list [NAME] [--output=OUTPUT]
              openapi3 tbd
              openapi3 tbd merge [SERVICES...] [--dir=DIR] [--verbose]
              openapi3 tdb list [--dir=DIR]
              openapi3 tbd description [SERVICES...] [--dir=DIR]
              openapi3 tbd md FILE [--indent=INDENT]
              openapi3 tbd codegen [SERVICES...] [--srcdir=SRCDIR]
                              [--destdir=DESTDIR]

          Arguments:
              DIR   The directory of the specifications
              FILE  The specification

          Options:
              --debug                use the server in debug mode
              --verbose              specifies to run in debug mode [default: False]
              --port=PORT            the port for the server [default: 8080]
              --directory=DIRECTORY  the directory in which the server is run
              --server=SERVER        the server [default: flask]
              --output=OUTPUT        the outputformat, table, csv, yaml, json [default: table]
              --srcdir=SRCDIR   The directory of the specifications
              --destdir=DESTDIR  The directory where the generated code should be put

          Description:
            This command does some useful things.


        """

        map_parameters(arguments,
                       'fg',
                       'os',
                       'output',
                       'verbose',
                       'port',
                       'directory',
                       'yamldirectory',
                       'baseurl',
                       'filename',
                       'name')
        arguments.debug = arguments.verbose

        # VERBOSE(arguments)

        if arguments.generate:

            try:
                function = arguments.FUNCTION
                yamlfile = arguments.YAML
                baseurl = path_expand(arguments.baseurl)
                filename = arguments.filename.strip().split(".")[0]
                yamldirectory = path_expand(arguments.yamldirectory)

                sys.path.append(baseurl)

                module_name = pathlib.Path(f"{filename}").stem

                imported_module = import_module(module_name)

                func_obj = getattr(imported_module, function)

                setattr(sys.modules[module_name], function, func_obj)

                # get dataclasses defined in module
                dataclass_list = []
                for attr_name in dir(imported_module):

                    attr = getattr(imported_module, attr_name)
                    if is_dataclass(attr):
                        dataclass_list.append(attr)

                openAPI = generator.Generator()

                baseurl_short = pathlib.Path(f"{baseurl}").stem

                openAPI.generate_openapi(func_obj,
                                         baseurl_short,
                                         yamldirectory, yamlfile,
                                         dataclass_list)
            except Exception as e:
                Console.error("Failed to generate openapi yaml")
                print(e)

        elif arguments.server and arguments.start and arguments.os:

            try:
                s = Server(
                    name=arguments.NAME,
                    spec=path_expand(arguments.YAML),
                    directory=path_expand(
                        arguments.directory) if arguments.directory else arguments.directory,
                    port=arguments.port,
                    server=arguments.wsgi,
                    debug=arguments.debug
                )

                pid = s.run_os()

                VERBOSE(arguments, label="Server parameters")

                print(f"Run PID: {pid}")

            except FileNotFoundError:

                Console.error("specification file not found")

            except Exception as e:

                print(e)

        elif arguments.server and arguments.list:

            try:
                result = Server.list(self, name=arguments.NAME)

                # BUG: order= nt yet defined

                print(Printer.list(result))

            except ConnectionError:
                Console.error("Server not running")

        elif arguments.server and arguments.ps:

            try:
                print()
                Console.info("Running Cloudmesh OpenAPI Servers")
                print()
                result = Server.ps(name=arguments.NAME)
                print(Printer.list(result, order=["name", "pid", "spec"]))

                print()
            except ConnectionError:
                Console.error("Server not running")

        elif arguments.register and arguments.add:

            registry = Registry()
            result = registry.add(name=arguments.NAME, url=arguments.BASEURL,
                                  pid=arguments.PID)

            registry.Print(data=result, output=arguments.output)

        elif arguments.register and arguments.delete:

            registry = Registry()
            result = registry.delete(name=arguments.NAME)
            if result == 0:
                Console.error("Entry could not be found")
            else:
                Console.ok("Ok. Entry deleted")

        elif arguments.register and arguments.list:

            registry = Registry()
            result = registry.list(name=arguments.NAME)

            registry.Print(data=result, output=arguments.output)

        elif arguments.register and arguments.filename:

            registry = Registry()
            result = [registry.add_form_file(arguments.filename)]

            registry.Print(data=result, output=arguments.output)

        elif arguments.server and arguments.start:

            # VERBOSE(arguments)

            try:
                s = Server(
                    name=arguments.NAME,
                    spec=path_expand(arguments.YAML),
                    directory=path_expand(
                        arguments.directory) if arguments.directory else arguments.directory,
                    port=arguments.port,
                    server=arguments.wsgi,
                    debug=arguments.debug)

                pid = s.start(name=arguments.NAME,
                              spec=path_expand(arguments.YAML),
                              foreground=arguments.fg)

                print(f"Run PID: {pid}")

            except FileNotFoundError:

                Console.error("specification file not found")

            except Exception as e:
                print(e)

        elif arguments.server and arguments.stop:

            try:
                print()
                Console.info("Stopping Cloudmesh OpenAPI Server")
                print()

                Server.stop(name=arguments.NAME)

                print()
            except ConnectionError:
                Console.error("Server not running")

        '''

        arguments.wsgi = arguments["--server"]

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


        return ""
        '''
