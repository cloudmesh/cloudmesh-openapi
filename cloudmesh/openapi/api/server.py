from cloudmesh.common.console import Console
from cloudmesh.common.util import path_expand
from pathlib import Path
import sys


class Server(object):

    def __init__(self, spec=None):
        if spec is None:
            Console.error("No service specification file defined")
            raise FileNotFoundError
        path = Path(path_expand(spec))
        Console.ok(path)

    def run(spec=None):
        Console.error("running")
