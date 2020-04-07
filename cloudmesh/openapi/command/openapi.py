import pathlib
import sys
import textwrap
import types
from dataclasses import is_dataclass
from importlib import import_module

from cloudmesh.common.Printer import Printer
from cloudmesh.common.console import Console
from cloudmesh.common.debug import VERBOSE
from cloudmesh.common.util import path_expand
from cloudmesh.openapi.function import generator
from cloudmesh.openapi.function.server import Server
from cloudmesh.openapi.registry.Registry import Registry
from cloudmesh.openapi.scikitlearn.SklearnGenerator import \
    generator as SklearnGenerator
from cloudmesh.shell.command import PluginCommand
from cloudmesh.shell.command import command, map_parameters


# start-stop: osx Andrew
# start_stop: windows Jonathan
# start-stop: linux Prateek


class OpenapiCommand(PluginCommand):

    # noinspection PyUnusedLocal,PyPep8Naming
    @command
    def do_openapi(self, args, arguments):
        """
        ::

          Usage:
              openapi generate FUNCTION --filename=FILENAME
                                         [--baseurl=BASEURL]
                                         [--yamlfile=YAML]
                                         [--yamldirectory=DIRECTORY]
                                         [--fclass]
                                         [--all_functions]
                                         [--verbose]
              openapi server start YAML [NAME]
                              [--directory=DIRECTORY]
                              [--port=PORT]
                              [--server=SERVER]
                              [--host=HOST]
                              [--verbose]
                              [--debug]
                              [--fg]
                              [--os]
              openapi server stop NAME
              openapi server list [NAME] [--output=OUTPUT]
              openapi server ps [NAME] [--output=OUTPUT]
              openapi register add NAME ENDPOINT
              openapi register filename NAME
              openapi register delete NAME
              openapi register list [NAME] [--output=OUTPUT]
              openapi TODO merge [SERVICES...] [--dir=DIR] [--verbose]
              openapi TODO doc FILE --format=(txt|md)[--indent=INDENT]
              openapi TODO doc [SERVICES...] [--dir=DIR]
              openapi sklearn generate FUNCTION

          Arguments:
              DIR       The directory of the specifications
              FILE      The specification
              FUNCTION  The name for the function or class

          Options:
              --debug                Use the server in debug mode
              --verbose              Specifies to run in debug mode
                                     [default: False]
              --port=PORT            The port for the server [default: 8080]
              --directory=DIRECTORY  The directory in which the server is run
              --server=SERVER        The server [default: flask]
              --output=OUTPUT        The outputformat, table, csv, yaml, json
                                     [default: table]
              --srcdir=SRCDIR        The directory of the specifications
              --destdir=DESTDIR      The directory where the generated code
                                     is placed

          Description:
            This command does some useful things.

            openapi TODO doc FILE --format=(txt|md|rst) [--indent=INDENT]
                Sometimes it is useful to generate teh openaopi documentation
                in another format. We provide fucntionality to generate the
                documentation from the yaml file in a different formt.

            openapi TODO doc --format=(txt|md|rst) [SERVICES...]
                Creates a short documentation from services registered in the
                registry.

            openapi TODO merge [SERVICES...] [--dir=DIR] [--verbose]
                Merges tow service specifications into a single servoce
                TODO: do we have a prototype of this?


            openapi sklearn generate sklearn.linear_model.LogisticRegression
                Generates the

            openapi generate FUNCTION --filename=FILENAME
                                         [--baseurl=BASEURL]
                                         [--yamlfile=YAML]
                                         [--yamldirectory=DIRECTORY]
                                         [--fclass]
                                         [--all_functions]
                                         [--verbose]
                TODO: add description

            openapi server start YAML [NAME]
                              [--directory=DIRECTORY]
                              [--port=PORT]
                              [--server=SERVER]
                              [--host=HOST]
                              [--verbose]
                              [--debug]
                              [--fg]
                              [--os]
                TODO: add description

            openapi server stop NAME
                stops the openapi service with the given name
                TODO: where does this command has to be started from

            openapi server list [NAME] [--output=OUTPUT]
                Provides a list of all OpenAPI services.
                TODO: Is thhis command is the same a register list?

            openapi server ps [NAME] [--output=OUTPUT]
                list the running openapi service

            openapi register add NAME ENDPOINT
                Openapi comes with a service registry in which we can register
                openapi services.

            openapi register filename NAME
                In case you have a yaml file the openapi service can also be
                registerd from a yaml file

            openapi register delete NAME
                Deletes the names service from the registry

            openapi register list [NAME] [--output=OUTPUT]
                Provides a list of all registerd OpenAPI services


        """

        map_parameters(arguments,
                       'fg',
                       'os',
                       'output',
                       'verbose',
                       'port',
                       'directory',
                       'yamlfile',
                       'yamldirectory',
                       'baseurl',
                       'filename',
                       'name',
                       'fclass',
                       'all_functions',
                       'host')
        arguments.debug = arguments.verbose

        # VERBOSE(arguments)

        if arguments.generate and not arguments.fclass and not arguments.all_functions:

            try:
                function = arguments.FUNCTION
                yamlfile = arguments.YAML
                baseurl = path_expand(arguments.baseurl)
                filename = arguments.filename.strip().split(".")[0]
                yamldirectory = path_expand(arguments.yamldirectory)
                module_name = pathlib.Path(f"{filename}").stem

                Console.info(textwrap.dedent(f"""
                     Cloudmesh OpenAPI Generator:

                         Function:  {function}
                         Filename:  {filename}
                         YAML:      {yamlfile}
                         Baseurl:   {baseurl}
                         Directory: {yamldirectory}
                         Module:    {module_name}

                 """))

                imported_module = import_module(module_name)
                VERBOSE(imported_module)
                func_obj = getattr(imported_module, function)
                VERBOSE(func_obj)

                for attr_name in dir(func_obj):
                    attr = getattr(func_obj, attr_name)
                    if isinstance(getattr(func_obj, attr_name), types.MethodType):
                        VERBOSE(attr)
                        print(attr_name)

                setattr(sys.modules[module_name], function, func_obj)

                # get dataclasses defined in module
                dataclass_list = []
                for attr_name in dir(imported_module):

                    attr = getattr(imported_module, attr_name)
                    if is_dataclass(attr):
                        dataclass_list.append(attr)
                VERBOSE(dataclass_list)
                openAPI = generator.Generator()

                '''
                TODO: look at using __init__ constructor in Class so that
                parameters can be defined at instantiation and reused for each
                function
                
                openAPI = generator.Generato(
                    function=arguments.FUNCTION,
                    yamlfile=arguments.YAML,
                    baseurl=path_expand(arguments.baseurl),
                    filename=arguments.filename.strip().split(".")[0],
                    yamldirectory=path_expand(arguments.yamldirectory)
                )
                '''

                baseurl_short = pathlib.Path(f"{baseurl}").stem

                openAPI.generate_openapi(func_obj,
                                         baseurl_short,
                                         yamldirectory, yamlfile,
                                         dataclass_list)
            except Exception as e:
                Console.error("Failed to generate openapi yaml")
                print(e)

        elif arguments.generate and arguments.fclass and not arguments.all_functions:
            try:
                function = arguments.FUNCTION  # Class Name

                filename = pathlib.Path(path_expand(arguments.filename)).stem

                yamlfile = arguments.yamlfile or filename

                baseurl = path_expand(arguments.baseurl) or \
                          str(pathlib.Path(path_expand(arguments.filename)).parent)

                baseurl_short = pathlib.Path(f"{baseurl}").stem

                yamldirectory = path_expand(arguments.yamldirectory) or \
                                str(pathlib.Path(path_expand(arguments.filename)).parent)

                Console.info(textwrap.dedent(f"""
                    Cloudmesh OpenAPI Generator:

                        Function:  {function}
                        Filename:  {filename}
                        YAML:      {yamlfile}
                        Baseurl:   {baseurl}
                        Directory: {yamldirectory}

                """))

                sys.path.append(baseurl)

                module_name = filename

                imported_module = import_module(module_name)
                VERBOSE(imported_module)

                class_obj = getattr(imported_module, function)
                VERBOSE(class_obj)

                class_description = class_obj.__doc__.strip().split("\n")[0]

                func_objects = {}
                dataclass_list = []
                for attr_name in dir(class_obj):
                    if isinstance(getattr(class_obj, attr_name), types.MethodType):
                        attr_obj = getattr(class_obj, attr_name)
                        VERBOSE(attr_name)
                        VERBOSE(attr_obj)
                        setattr(sys.modules[module_name], attr_name, attr_obj)

                        for sub_attr_name in dir(attr_name):
                            sub_attr_obj = getattr(attr_name, sub_attr_name)
                            if is_dataclass(sub_attr_obj):
                                dataclass_list.append(sub_attr_obj)
                        VERBOSE(dataclass_list)

                        func_objects[f"{attr_name}"] = attr_obj

                openAPI = generator.Generator()

                '''
                TODO: look at using __init__ constructor in Class so that
                parameters can be defined at instantiation and reused for each
                function
                
                
                openAPI = generator.Generator(
                    function=arguments.FUNCTION,
                    yamlfile=arguments.YAML,
                    baseurl=path_expand(arguments.baseurl),
                    filename=arguments.filename.strip().split(".")[0],
                    yamldirectory=path_expand(arguments.yamldirectory)
                )
                '''

                openAPI.generate_openapi_class(function,
                                         class_description,
                                         filename,
                                         func_objects,
                                         baseurl_short,
                                         yamldirectory,
                                         yamlfile,
                                         dataclass_list)

            except Exception as e:
                Console.error("Failed to generate openapi yaml")
                print(e)

        # TODO: this should just be collapsed into the previous condition
        elif arguments.generate and arguments.all_functions and not arguments.fclass:
            try:
                function = arguments.FUNCTION  # Class Name

                filename = pathlib.Path(path_expand(arguments.filename)).stem

                yamlfile = arguments.yamlfile or filename

                baseurl = path_expand(arguments.baseurl) or \
                          str(pathlib.Path(path_expand(arguments.filename)).parent)

                baseurl_short = pathlib.Path(f"{baseurl}").stem

                yamldirectory = path_expand(arguments.yamldirectory) or \
                                str(pathlib.Path(path_expand(arguments.filename)).parent)

                Console.info(textwrap.dedent(f"""
                    Cloudmesh OpenAPI Generator:

                        Function:  {function}
                        Filename:  {filename}
                        YAML:      {yamlfile}
                        Baseurl:   {baseurl}
                        Directory: {yamldirectory}

                """))

                sys.path.append(baseurl)

                module_name = filename
                VERBOSE(module_name)

                imported_module = import_module(module_name)
                VERBOSE(imported_module)

                func_objects = {}
                dataclass_list = []
                for attr_name in dir(imported_module):
                    if type(getattr(imported_module, attr_name)).__name__ == 'function':
                        attr_obj = getattr(imported_module, attr_name)
                        VERBOSE(attr_name)
                        VERBOSE(attr_obj)
                        setattr(sys.modules[module_name], attr_name, attr_obj)

                        for sub_attr_name in dir(attr_name):
                            sub_attr_obj = getattr(attr_name, sub_attr_name)
                            if is_dataclass(sub_attr_obj):
                                dataclass_list.append(sub_attr_obj)
                        VERBOSE(dataclass_list)

                        func_objects[f"{attr_name}"] = attr_obj

                openAPI = generator.Generator()

                '''
                TODO: look at using __init__ constructor in Class so that
                parameters can be defined at instantiation and reused for each
                function

                openAPI = generator.Generator(
                    function=arguments.FUNCTION,
                    yamlfile=arguments.YAML,
                    baseurl=path_expand(arguments.baseurl),
                    filename=arguments.filename.strip().split(".")[0],
                    yamldirectory=path_expand(arguments.yamldirectory)
                )
                '''

                openAPI.generate_openapi_class(function,
                                         "No description provided",
                                         filename,
                                         func_objects,
                                         baseurl_short,
                                         yamldirectory,
                                         yamlfile,
                                         dataclass_list,
                                               True)

            except Exception as e:
                Console.error("Failed to generate openapi yaml")
                print(e)

        elif arguments.server and arguments.start and arguments.os:

            try:
                s = Server(
                    name=arguments.NAME,
                    spec=path_expand(arguments.YAML),
                    directory=path_expand(
                        arguments.directory) or arguments.directory,
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
                        arguments.directory) or arguments.directory,
                    port=arguments.port,
                    host=arguments.host,
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

        elif arguments.sklearn:

            try:
                SklearnGenerator(arguments.FUNCTION)

            except Exception as e:
                print(e)


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
