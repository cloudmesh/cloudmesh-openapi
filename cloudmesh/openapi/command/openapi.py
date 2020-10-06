import os
import os
import sys
import textwrap
import types
from dataclasses import is_dataclass
from importlib import import_module
from pathlib import Path
from shutil import copyfile

from cloudmesh.common.Printer import Printer
from cloudmesh.common.console import Console
from cloudmesh.common.debug import VERBOSE
from cloudmesh.common.util import path_expand
from cloudmesh.openapi.authentication.basic import BasicAuth
from cloudmesh.openapi.function import generator
from cloudmesh.openapi.function.server import Server
from cloudmesh.openapi.function.executor import Parameter
from cloudmesh.openapi.registry.Registry import Registry
from cloudmesh.openapi.scikitlearn.SklearnGenerator import Sklearngenerator
from cloudmesh.openapi.scikitlearn.SklearnGeneratorFile import SklearngeneratorFile
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
              openapi generate [FUNCTION] --filename=FILENAME
                                         [--serverurl=SERVERURL]
                                         [--yamlfile=YAML]
                                         [--import_class]
                                         [--all_functions]
                                         [--enable_upload]
                                         [--verbose]
                                         [--basic_auth=CREDENTIALS]
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
              openapi sklearn FUNCTION MODELTAG
              openapi sklearnreadfile FUNCTION MODELTAG
              openapi sklearn upload --filename=FILENAME

          Arguments:
              FUNCTION  The name for the function or class
              MODELTAG  The arbirtary name choosen by the user to store the Sklearn trained model as Pickle object
              FILENAME  Path to python file containing the function or class
              SERVERURL OpenAPI server URL Default: https://localhost:8080/cloudmesh
              YAML      Path to yaml file that will contain OpenAPI spec. Default: FILENAME with .py replaced by .yaml
              DIR       The directory of the specifications
              FILE      The specification

          Options:
              --import_class         FUNCTION is a required class name instead of an optional function name
              --all_functions        Generate OpenAPI spec for all functions in FILENAME
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


            openapi sklearn sklearn.linear_model.LogisticRegression
                Generates the .py file for the Model given for the generator

            openapi sklearnreadfile sklearn.linear_model.LogisticRegression
            Generates the .py file for the Model given for the generator which supports reading files

            openapi generate [FUNCTION] --filename=FILENAME
                                         [--serverurl=SERVERURL]
                                         [--yamlfile=YAML]
                                         [--import_class]
                                         [--all_functions]
                                         [--enable_upload]
                                         [--verbose]
                                         [--basic_auth=CREDENTIALS]
                Generates an OpenAPI specification for FUNCTION in FILENAME and
                writes the result to YAML. Use --import_class to import a class
                with its associated class methods, or use --all_functions to 
                import all functions in FILENAME. These options ignore functions
                whose names start with '_'. Use --enable_upload to add file
                upload functionality to a copy of your python file and the
                resulting yaml file.

                For optional basic authorization, we support (temporarily) a single user
                credential. CREDENTIALS should be formatted as follows:

                user:password

                Example: --basic_auth=admin:secret

            openapi server start YAML [NAME]
                              [--directory=DIRECTORY]
                              [--port=PORT]
                              [--server=SERVER]
                              [--host=HOST]
                              [--verbose]
                              [--debug]
                              [--fg]
                              [--os]
                starts an openapi web service using YAML as a specification
                TODO: directory is hard coded as None, and in server.py it
                  defaults to the directory where the yaml file lives. Can
                  we just remove this argument?

            openapi server stop NAME
                stops the openapi service with the given name
                TODO: where does this command has to be started from

            openapi server list [NAME] [--output=OUTPUT]
                Provides a list of all OpenAPI services in the registry

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
        #print(arguments)
        map_parameters(arguments,
                       'fg',
                       'os',
                       'output',
                       'verbose',
                       'port',
                       'directory',
                       'yamlfile',
                       'serverurl',
                       'name',
                       'import_class',
                       'all_functions',
                       'enable_upload',
                       'host',
                       'basic_auth')
        arguments.debug = arguments.verbose

        #VERBOSE(arguments)

        if arguments.generate:
            if arguments.import_class and arguments.all_functions:
                Console.error('Cannot generate openapi with both --import_class and --all_functions')
            if arguments.import_class and not arguments.FUNCTION:
                Console.error('FUNCTION parameter (class name) is required when using --import_class')
            try:
                p = Parameter(arguments)
                p.Print()
                filename = p.filename # ./dir/myfile.py
                yamlfile = p.yamlfile # ./dir/myfile.yaml
                directory = p.yamldirectory # ./dir
                function = p.function # myfunction
                serverurl = p.serverurl # http://localhost:8080/cloudmesh/
                module_name = p.module_name # myfile
                basic_auth = p.basic_auth # user:password

                # If statement here for mode with basic_auth

                enable_upload = arguments.enable_upload
                # append the upload function to the end of a copy of the file if not already done
                if enable_upload:
                    uploadPython = textwrap.dedent("""
                        from cloudmesh.openapi.registry.fileoperation import FileOperation
                        
                        def upload() -> str:
                            filename=FileOperation().file_upload()
                            return filename
                        
                        #### upload functionality added
                        """)
                    upload_added = False
                    for line in open(filename):
                        if '#### upload functionality added' in line:
                            upload_added = True
                    if not upload_added:
                        filename_upload = filename.replace('.py', '_upload-enabled.py')
                        copyfile(filename, filename_upload)
                        Console.info(f'copied {filename} to {filename_upload}')
                        filename = filename_upload
                        module_name = module_name + '_upload-enabled'
                        with open(filename, 'a') as f:
                            f.write('\n')
                            f.write(uploadPython)
                        Console.info(f'added upload functionality to {filename}')

                if basic_auth:
                    user, password = basic_auth.split(':')
                    BasicAuth.reset_users()
                    BasicAuth.add_user(user, password)
                    module_name, filename = BasicAuth.write_basic_auth(
                        filename=filename,
                         module_name=module_name)

                # Parameter() takes care of putting the filename in the path
                imported_module = import_module(module_name)
                dataclass_list = []
                for attr_name in dir(imported_module):
                    attr = getattr(imported_module, attr_name)
                    if is_dataclass(attr):
                        dataclass_list.append(attr)
                # not currently supporting multiple functions or all functions
                # could do comma-separated function/class names

                if enable_upload:
                    upload_obj = getattr(imported_module, 'upload')
                    setattr(sys.modules[module_name], 'upload', upload_obj)

                if arguments.import_class:
                    class_obj = getattr(imported_module, function)
                    # do we maybe need to do this here?
                    # setattr(sys.modules[module_name], function, class_obj)
                    class_description = class_obj.__doc__.strip().split("\n")[0]
                    func_objects = {}
                    for attr_name in dir(class_obj):
                        attr = getattr(class_obj, attr_name)                        
                        if isinstance(attr, types.MethodType) and attr_name[0] != '_':
                            # are we sure this is right?
                            # would probably create a valid openapi yaml, but not technically accurate
                            # module.function may work but it should be module.Class.function
                            setattr(sys.modules[module_name], attr_name, attr)
                            func_objects[attr_name] = attr
                        elif is_dataclass(attr):
                            dataclass_list.append(attr)
                    openAPI = generator.Generator()
                    Console.info(
                        'Generating openapi for class: ' + class_obj.__name__)
                    openAPI.generate_openapi_class(class_name=class_obj.__name__,
                                                   class_description=class_description,
                                                   filename=filename,
                                                   func_objects=func_objects,
                                                   serverurl=serverurl,
                                                   outdir=directory,
                                                   yamlfile=yamlfile,
                                                   dataclass_list=dataclass_list,
                                                   all_function=False,
                                                   enable_upload=enable_upload,
                                                   basic_auth_enabled=basic_auth,
                                                   write=True)
                elif arguments.all_functions:
                    func_objects = {}
                    for attr_name in dir(imported_module):
                        if type(getattr(imported_module, attr_name)).__name__ == 'function' and attr_name[0] != '_':
                            func_obj = getattr(imported_module, attr_name)
                            setattr(sys.modules[module_name], attr_name, func_obj)
                            func_objects[attr_name] = func_obj
                    openAPI = generator.Generator()
                    Console.info(
                        'Generating openapi for all functions in file: ' + filename)
                    openAPI.generate_openapi_class(class_name=module_name,
                                                   class_description="No description provided",
                                                   filename=filename,
                                                   func_objects=func_objects,
                                                   serverurl=serverurl,
                                                   outdir=directory,
                                                   yamlfile=yamlfile,
                                                   dataclass_list=dataclass_list,
                                                   all_function=True,
                                                   enable_upload=enable_upload,
                                                   basic_auth_enabled=basic_auth,
                                                   write=True)

                else:
                    func_obj = getattr(imported_module, function)
                    setattr(sys.modules[module_name], function, func_obj)
                    openAPI = generator.Generator()
                    Console.info(
                        'Generating openapi for function: ' + func_obj.__name__)
                    openAPI.generate_openapi(f=func_obj,
                                             filename=filename,
                                             serverurl=serverurl,
                                             outdir=directory,
                                             yamlfile=yamlfile,
                                             dataclass_list=dataclass_list,
                                             enable_upload=enable_upload,
                                             basic_auth_enabled=basic_auth,
                                             write=True)

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
                result = Server.list(name=arguments.NAME)

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

        elif arguments.register and arguments['filename']:

            registry = Registry()
            result = [registry.add_form_file(arguments['filename'])]

            registry.Print(data=result, output=arguments.output)

        elif arguments.server and arguments.start:

            # VERBOSE(arguments)

            try:
                s = Server(
                    name=arguments.NAME,
                    spec=path_expand(arguments.YAML),
                    directory=None,
                    #directory=path_expand(
                    #    arguments.directory) or arguments.directory,
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

        elif arguments.sklearn and not arguments.upload:

            try:
                Sklearngenerator(input_sklibrary=arguments.FUNCTION,
                                 model_tag=arguments.MODELTAG)
            except Exception as e:
                print(e)

        elif arguments.sklearnreadfile and not arguments.upload:

            try:
                SklearngeneratorFile(input_sklibrary=arguments.FUNCTION,
                                          model_tag=arguments.MODELTAG)
            except Exception as e:
                print(e)
        
        #TODO: implement this?
        elif arguments.sklearn and arguments.upload:

            try:
                openAPI = generator.Generator()
                openAPI.fileput()

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
