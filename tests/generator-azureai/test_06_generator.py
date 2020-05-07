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
#import pycurl
#import requests
import subprocess
#from io import BytesIO
#import json


filename="./tests/generator-azureai/azure-ai-image-function.py"
all_functions= True
import_class=False
function_name="get_image_desc"

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

    def test_azureai(self):
        HEADING()
        #url = f"http://localhost:8080/cloudmesh/azure-ai-image-function_upload_enabled/get_image_desc"
        Benchmark.Start()
        #result = requests.get(url=url, params=payload,headers=headers)
        #results = curl -X GET "http://localhost:8080/cloudmesh/azure-ai-image-function_upload-enabled/get_image_desc?image_name=landmark.jpg" -H "accept: text/plain"
        curlURL = "curl -X GET 'http://localhost:8080/cloudmesh/azure-ai-image-function_upload-enabled/get_image_desc?image_name=landmark.jpg' -H 'accept: text/plain'"
        p = subprocess.Popen(curlURL, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, err = p.communicate()

        #if p.returncode != 0:
        #    print(err)

        #print(output.decode('utf-8'))

        #result = crl.getinfo()
        assert p.returncode == 0, "Return code value should be 0"
        #assert result.status_code == 200, "Status code value should be 200"
        #assert result.reason == 'OK'
        #assert result.headers['content-type'] == 'text/plain; charset=utf-8'
        #assert result.json().get('test') is not None
        Benchmark.Stop()
        VERBOSE(output.decode('utf-8'))


    def test_stop_server(self, serverBaseTestFixture):
        serverBaseTestFixture.stop_server()

    def test_delete_build_file(self, generatorBaseTestFixture):
       generatorBaseTestFixture.delete_file()


    def test_benchmark(self,generatorBaseTestFixture):
        Benchmark.print(sysinfo=True, csv=True, tag=generatorBaseTestFixture.service)

