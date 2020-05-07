###############################################################
# pytest -v --capture=no tests/server-cms/test_04_generator.py
###############################################################
import os
import time
from pprint import pprint
import sys
sys.path.append("./tests/lib")
from generator_test import GeneratorBaseTest, ServerBaseTest
import pytest
filename="./tests/server-cms/cms.py"
all_functions= True
import_class=False
from cloudmesh.common.Benchmark import Benchmark
from cloudmesh.common.debug import VERBOSE
from cloudmesh.common.util import HEADING
import requests


@pytest.mark.incremental
class TestGeneratorTestClass():


    @pytest.fixture(scope="module")
    def generatorBaseTestFixture(self):
        gen= GeneratorBaseTest(filename,all_functions,import_class)
        return gen

    @pytest.fixture(scope="module")
    def serverBaseTestFixture(self):
        server = ServerBaseTest()
        return server

    def test_copy_file(self,generatorBaseTestFixture):
        generatorBaseTestFixture.copy_py_file()

    def test_generate(self,generatorBaseTestFixture):
        """
        function to validate paths information
        """
        generatorBaseTestFixture.generate()

    def test_read_spec(self,generatorBaseTestFixture):
        generatorBaseTestFixture.read_spec()

    def test_validate_function(self, generatorBaseTestFixture):
        generatorBaseTestFixture.validate_function()

    def test_start_service(self,serverBaseTestFixture):
        serverBaseTestFixture.start_service()

    def test_cms(self):
        HEADING()
        url = f"http://127.0.0.1:8080/cloudmesh/cms/test"
        Benchmark.Start()
        payload = {'service': 'value1'}
        result = requests.get(url, params=payload)
        assert result.status_code == 200, "Status code value should be 200"
        assert result.reason == 'OK'
        assert result.headers['content-type'] == 'text/plain; charset=utf-8'
        assert result.json().get('test') is not None
        Benchmark.Stop()
        VERBOSE(result)

    def test_stop_server(self,serverBaseTestFixture):
        serverBaseTestFixture.stop_server()

    def test_delete_build_file(self, generatorBaseTestFixture):
        generatorBaseTestFixture.delete_file()

    def test_benchmark(self,generatorBaseTestFixture):
        Benchmark.print(sysinfo=True, csv=True, tag=generatorBaseTestFixture.service)
