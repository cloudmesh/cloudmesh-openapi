from cloudmesh.common.console import Console
from cloudmesh.common.util import path_expand
from cloudmesh.terminal.Terminal import VERBOSE
from cloudmesh.common.Shell import Shell

from pathlib import Path
import sys
from flask import jsonify
import connexion
from importlib import import_module
import os


def dynamic_import(abs_module_path, class_name):
    module_object = import_module(abs_module_path)
    target_class = getattr(module_object, class_name)
    return target_class


class Server(object):

    def __init__(self,
                 spec=None,
                 directory="./",
                 host="127.0.0.1",
                 port=8080,
                 debug=True):
        if spec is None:
            Console.error("No service specification file defined")
            raise FileNotFoundError

        self.path = path_expand(spec)
        self.spec = self.path
        self.directory = path_expand(directory)[:-1]
        self.host = host
        self.port = port
        self.debug = debug
        self.code = os.path.dirname(self.path) + "/cpu.py"

        data = dict(self.__dict__)
        data['name'] = __name__

        VERBOSE.print(data, label="Server parameters", verbose=9)

        Console.ok(self.path)

    def run(self):
        Console.ok("starting server")

        r = Shell.live("connexion run {spec} --debug".format(**self.__dict__))

        # app = connexion.App(__name__, specification_dir=self.directory)
        # ### app.add_cls(self.directory)
        # app.add_api(self.path)
        # app.run(host=self.host, port=self.port, debug=self.debug, )
