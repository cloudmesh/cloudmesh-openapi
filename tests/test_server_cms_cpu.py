###############################################################
# pytest -v --capture=no tests/test_server_cms_cpu.py
# pytest -v  tests/test_server_cms_cpu.py
# pytest -v --capture=no  tests/test_server_cms_cpu..py::Test_server_cms::<METHODNAME>
###############################################################
import pytest
from cloudmesh.common.Shell import Shell
from cloudmesh.common.debug import VERBOSE
from cloudmesh.common.util import HEADING
from cloudmesh.common.Benchmark import Benchmark
import os
import requests
import time

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



Benchmark.debug()

cloud = "local"

name = "cpu"
yaml_file = "./tests/{name}.yaml"
@pytest.mark.incremental
class TestServerCms:

    def test_start(self):
        HEADING()

        Benchmark.Start()

        # os.system(f"cms openapi3 server start ./tests/server-cpu/cpu.yaml >> log12.txt 2>&1 & ")
        os.system(f"cms openapi3 server start ./tests/server-cpu/cpu.yaml &")
        time.sleep(4)
        result = requests.get('http://127.0.0.1:8080/cloudmesh/ui')
        Benchmark.Stop()

        assert result.status_code == 200 # find test


    def test_cpu(self):
        HEADING()
        url = "http://127.0.0.1:8080/cloudmesh/cpu"
        Benchmark.Start()
        result = requests.get(url)
        assert result.status_code == 200
        assert result.reason == 'OK'
        assert result.headers['content-type'] =='application/json'
        assert result.json().get('model') is not None
        Benchmark.Stop()
        VERBOSE(result)

    def test_stop(self):
        HEADING()

        Benchmark.Start()
        # result = Shell.execute(f"cms openapi3 server stop {name}", shell=True)
        os.system(f"cms openapi3 server stop {name}")
        Benchmark.Stop()
        gotException=False;
        try:
            result = requests.get('http://127.0.0.1:8080/cloudmesh/ui')
        except Exception as ex:
            gotException=True
        assert gotException
