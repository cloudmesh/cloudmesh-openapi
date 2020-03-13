from cloudmesh.common.console import Console
from cloudmesh.common.util import path_expand
from cloudmesh.common.util import readfile
from cloudmesh.common.debug import VERBOSE
from cloudmesh.common.Shell import Shell
from cloudmesh.management.script import Script

import sys
import connexion
from importlib import import_module
import os, platform, socket, signal
from flask import Flask, request
import textwrap
from pathlib import Path, PureWindowsPath
from datetime import date
import subprocess
import sys


def dynamic_import(abs_module_path, class_name):
    module_object = import_module(abs_module_path)
    target_class = getattr(module_object, class_name)
    return target_class


class Server(object):

    def __init__(self,
                 spec=None,
                 directory=None,
                 host="127.0.0.1",
                 server="flask",
                 port=8080,
                 debug=True,
                 name=None):
        """
        This class is used to manage an OpenAPI server that was generated with
        the cloudmesh function generator tool.

        We assume that the yaml specification as located at *spec* and the
        directory contains the code for the operationIDs provided in the yaml
        file.

        If the directory is None, the code is located in the same directory as
        the spec.

        :param spec: the location of the yaml file
        :param directory: the location of the base directory in
                          which the code is located
        :param host: the hostname on which the code is run, by default
                     it is localhost
        :param server: The server to be used. Either flask (default) or tornado
        :param port: The port on which the service is run
        :param debug: Boolean to set if debug mode is used.
        """

        # if spec is None:
        #     # Console.error("No service specification file defined")
        #     raise FileNotFoundError

        # self.path = path_expand(spec)
        self.path = directory + spec
        self.spec = self.path
        # self.spec = spec
        self.directory = os.path.dirname(self.path)
        self.host = host
        self.port = port
        self.debug = debug
        self.code = spec.replace(".yaml", ".py")
        self.server = server
        self.server_command = ""
        self.name = name

        # Assigning an alias name to the server getting started and sending to a
        # dict
        # while name is None:
        # alias = input(f"Provide an alias for the server: ")
        #
        # if name in self.name.values():
        #     name = input(f"Provide a unique name for the server: ")
        # else:
        #     current_name_keys = self.name.keys()
        #     try:
        #         last_value = current_name_keys[-1]
        #         new_key = last_value.split('_')
        #         new_key = new_key[0].join(int(new_key[-1])+1)
        #         self.name.update({new_key : name})
        #     except IndexError:
        #         self.name['serverName_1'] = name

        data = dict(self.__dict__)
        # data['name'] = __name__

        VERBOSE(data, label="Server parameters")

        if server == "tornado":
            try:
                import tornado
            except Exception as e:
                print(e)
                Console.error(
                    "tornado not install. Please use `pip install tornado`")
                sys.exit(1)
            if self.debug:
                Console.error("Tornado does not support --verbose")
                sys.exit(1)

        Console.ok(self.path)


    def start(self):
        ###
        pass

    def _run_os(self):
        Console.ok("starting server")

        # If windows convert backslashes to forward slashes to be python compatible
        if sys.platform == 'win32':
            self.spec = "/".join(self.spec.replace('C:', '').split('\\'))
            self.directory = "/".join(self.directory.replace('C:', '').split('\\'))

        today_dt = date.today().strftime("%m%d%Y")
        VERBOSE("spec path: ", self.spec)

        flask_script = textwrap.dedent(f'''
            import connexion
            
            # Create the application instance
            app = connexion.App(__name__, specification_dir='{self.directory}')
            
            # Read the yaml file to configure the endpoints
            app.add_api('{self.spec}')
            
            if __name__ == '__main__':
                app.run(host='{self.host}',
                        port={self.port},
                        debug={self.debug},
                        server={self.server})
        ''')

        VERBOSE("server script: ", f"{self.directory}/{self.name}_server.py")

        # Write out flask python script to file so that it can be run in background
        try:
            version = open(f"{self.directory}/{self.name}_server.py", 'w').write(
                flask_script)
        except IOError:
            Console.error("Unable to write server file")
        except Exception as e:
            print(e)

        # Run python flask script in background
        try:
            # TODO: need to write log somewhere else or use a logger to write to common log

            logname = f"{self.directory}/{self.name}_server.{today_dt}.log"

            f = open(logname, "w")
            process = subprocess.Popen([sys.executable,
                                       f"{self.directory}/{self.name}_server.py"],
                                      stdout=f,
                                      stderr=f,
                                      shell=False);

            # Write PID file
            pidfile = open(f"{self.directory}/{self.name}_server.pid", 'w')
            pidfile.write(str(process.pid))
        except Exception as e:
            Console.error("Unable to start server")
            print(e)

    def shutdown_os(self, name):

        Console.ok(f"shutting down server {name}")

        # TODO: reading pid from file in current dir for now.
        #  The pid should be stored in registry longterm.

        pid = readfile(f"./{name}_server.pid").strip()

        Shell.kill_pid(pid)
