from cloudmesh.common.console import Console
from cloudmesh.common.util import path_expand
from cloudmesh.common.debug import VERBOSE
import sys
import connexion
from importlib import import_module
import os, platform, socket
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
<<<<<<< HEAD
                 port=5000,
                 debug=True,
                 alias="Test"):
=======
                 port=8080,
                 debug=True):
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
>>>>>>> master
        if spec is None:
            # Console.error("No service specification file defined")
            raise FileNotFoundError


        self.path = path_expand(spec)
        self.name = alias
        self.spec = self.path
        self.directory = os.path.dirname(self.path)
        self.host = host
        self.port = port
        self.debug = debug
        self.code = self.spec.rename(".yaml", ".py")
        self.server = server
        self.server_command = ""

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

    def run(self):
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
        app.add_api(self.path)
        app.run(host=self.host,
                port=self.port,
                debug=self.debug,
                server=self.server)

    def shutdown(self):

        shutdown = request.environ.get('werkzeug.server.shutdown')
        if shutdown == None:
            return 'No server is running'
        else:
            shutdown()
            return 'Server successfully shutdown'
