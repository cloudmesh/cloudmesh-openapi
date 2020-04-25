###############################################################
# pytest -v --capture=no tests/test_server_cms_cpu.py
# pytest -v  tests/test_server_cms_cpu.py
# pytest -v --capture=no  tests/test_server_cms_cpu..py::Test_server_cms::<METHODNAME>
###############################################################
import os
import time

import pytest
import requests
from cloudmesh.common.Benchmark import Benchmark
from cloudmesh.common.debug import VERBOSE
from cloudmesh.common.util import HEADING

Benchmark.debug()

cloud = "local"

name = "cpu"
yaml_file = f"./tests/server-cpu/{name}.yaml"
@pytest.mark.incremental
class TestServerCms:

    def test_start(self):
        HEADING()

        Benchmark.Start()

        os.system(f"cms openapi server start {yaml_file} --directory=./tests/server-cpu/")
        time.sleep(4)
        result = requests.get('http://127.0.0.1:8080/cloudmesh/ui')
        Benchmark.Stop()

        assert result.status_code == 200 # find test


    def test_cpu(self):
        HEADING()
        url = "http://127.0.0.1:8080/cloudmesh/cpu"
        Benchmark.Start()
        result = requests.get(url)
        time.sleep(4)
        assert result.status_code == 200
        assert result.reason == 'OK'
        assert result.headers['content-type'] =='application/json'
        assert result.json().get('model') is not None
        Benchmark.Stop()
        VERBOSE(result)

    def test_stop(self):
        HEADING()

        Benchmark.Start()
        os.system(f"cms openapi server stop {name}")
        Benchmark.Stop()
        gotException=False;
        try:
            result = requests.get('http://127.0.0.1:8080/cloudmesh/ui')
        except Exception as ex:
            gotException=True
        assert gotException
