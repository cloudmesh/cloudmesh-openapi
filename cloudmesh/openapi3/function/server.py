from cloudmesh.common.console import Console
from cloudmesh.common.util import path_expand
from cloudmesh.common.debug import VERBOSE
import sys
import connexion
from importlib import import_module
import os, platform, socket, signal
from flask import Flask, request


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
                 alias=None):
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

        if spec is None:
            # Console.error("No service specification file defined")
            raise FileNotFoundError

        #self.path = path_expand(spec)
        self.path = directory+"/"+spec
        self.spec = self.path
        #self.spec = spec
        self.directory = os.path.dirname(self.path)
        self.host = host
        self.port = port
        self.debug = debug
        self.code = spec.replace(".yaml",".py")
        self.server = server
        self.server_command = ""
        self.alias = {}

        # Assigning an alias name to the server getting started and sending to a
        # dict
        # while alias is None:
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
        data['name'] = __name__

        VERBOSE(data, label="Server parameters")

        if server == "tornado":
            try:
                import tornado
            except Exception as e:
                print(e)
                Console.error(
                    "tornado not install. Please use `pip install tornado`")
                sys.exit(1)
                return ""
            if self.debug:
                Console.error("Tornado does not support --verbose")
                sys.exit(1)
                return ""

        Console.ok(self.path)

    def _run(self):
        Console.ok("starting server")

        # if self.server is not None:
        #    self.server_command = "--server={server}".format(**self.__dict__)

        # command = ("connexion run {spec} {server_command} --debug".format(
        #    **self.__dict__))
        # VERBOSE(command, label="OpenAPI Server", verbose=1)
        # r = Shell.live(command)

        sys.path.append(self.directory)
        app = connexion.App(__name__,
                            specification_dir=self.directory)

        # app.app["config"]["DEBUG"] = True

        # ### app.add_cls(self.directory)
        app.add_api(self.spec)
        app.run(host=self.host,
                port=self.port,
                debug=self.debug,
                server=self.server)

    def shutdown(self):

        Console.ok(f"shutting down {self.name}")

        get_pid = os.popen("ps -ef|grep {name}|grep -v grep|awk '{print $2}'")
        pid = get_pid.read()

        os.kill(pid, signal.SIGSTOP)

        Console.ok(f"{self.name} is shut down")


        # check if pid still in list

        # repalce grep findstr in windows add if statement
        # maybe implement a pause functionality with signal.pause?

        # maybe look into a way to kill parallel processes because signal
        # kills proceses being executed on the main python thread

        # Kill entire server option?
        # shutdown = request.environ.get('werkzeug.server.shutdown')
        # if shutdown == None:
        #     return 'No server is running'
        # else:
        #     shutdown()
        #     return 'Server successfully shutdown'

