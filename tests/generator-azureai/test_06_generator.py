###############################################################
# pytest -v --capture=no tests/generator-azureai/test_06_generator.py
# pytest -v  tests/test_03_generator.py
# pytest -v --capture=no  tests/test_generator..py::Test_name::<METHODNAME>
###############################################################
import os
import time
from pprint import pprint
import sys
sys.path.append("./tests/lib")
from generator_test import GeneratorBaseTest, ServerBaseTest
import pytest
from cloudmesh.common.dotdict import dotdict
from cloudmesh.common.debug import VERBOSE
from cloudmesh.common.util import HEADING
import requests



filename="./tests/generator-azureai/azure-ai-image-function.yaml"
test_image="./tests/generator-azureai/test_image1.jpg"
all_functions= True
import_class=False
function_1="get_image_desc"
function_2="get_image_analysis"
function_3="get_image_tags"
test_file_name = "test_image1.jpg"
upload_dir = "~/.cloudmesh/upload-file"

from cloudmesh.common.Benchmark import Benchmark

Benchmark.debug()


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

    def test_upload(self):
        HEADING()
        Benchmark.Start()

        Shell.run(
            f"cp {test_image} {upload_dir}")

        file_list = Shell.run(f"ls {upload_dir}")

        assert test_file_name in file_list

        Benchmark.Stop()

    def test_get_image_desc(self):
        HEADING()
        url = f"http://localhost:8080/cloudmesh/azure-ai-image-function_upload_enabled/{function_1}"
        Benchmark.Start()
        payload = {'image_name':{test_file_name}}
        result = requests.get(url, params=payload)
        assert result.status_code == 200, "Status code value should be 200"
        assert result.reason == 'OK'
        assert result.headers['content-type'] == 'text/plain; charset=utf-8'
        assert result.json().get('test') is not None
        Benchmark.Stop()
        VERBOSE(result)

    def test_get_image_analysis(self):
        HEADING()
        url = f"http://localhost:8080/cloudmesh/azure-ai-image-function_upload_enabled/{function_2}"
        Benchmark.Start()
        payload = {'image_name':{test_file_name}}
        result = requests.get(url, params=payload)
        assert result.status_code == 200, "Status code value should be 200"
        assert result.reason == 'OK'
        assert result.headers['content-type'] == 'text/plain; charset=utf-8'
        assert result.json().get('test') is not None
        Benchmark.Stop()
        VERBOSE(result)

    def test_get_image_tags(self):
        HEADING()
        url = f"http://localhost:8080/cloudmesh/azure-ai-image-function_upload_enabled/{function_3}"
        Benchmark.Start()
        payload = {'image_name':{test_file_name}}
        result = requests.get(url, params=payload)
        assert result.status_code == 200, "Status code value should be 200"
        assert result.reason == 'OK'
        assert result.headers['content-type'] == 'text/plain; charset=utf-8'
        assert result.json().get('test') is not None
        Benchmark.Stop()
        VERBOSE(result)


    def test_stop_server(self, serverBaseTestFixture):
        serverBaseTestFixture.stop_server()

    def test_delete_build_file(self, generatorBaseTestFixture):
       generatorBaseTestFixture.delete_file()


    def test_benchmark(self,generatorBaseTestFixture):
        Benchmark.print(sysinfo=True, csv=True, tag=generatorBaseTestFixture.service)

