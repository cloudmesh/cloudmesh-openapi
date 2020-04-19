###############################################################
# pytest -v --capture=no tests/test_03_generator.py
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

startservercommand="cms openapi server start ./tests/server-cpu/build/cpu.yaml cpu --directory=./tests/server-cpu/build/"
filename="./tests/server-cpu/cpu.py"

@pytest.mark.incremental
class TestGeneratorTestClass():


    @pytest.fixture(scope="module")
    def generatorBaseTestFixture(self):
        gen= GeneratorBaseTest(filename,False,False)
        gen.function_name = "get_processor_name"
        return gen

    # def test_as(self,generatorBaseTestFixture):
    #     pass
    @pytest.fixture(scope="module")
    def serverBaseTestFixture(self):
        server = ServerBaseTest(startservercommand);
        return server

    def test_copy_file(self,generatorBaseTestFixture):
        generatorBaseTestFixture.copy_py_file();

    def test_generate(self,generatorBaseTestFixture):
        """
        function to validate paths information
        """
        generatorBaseTestFixture.generate()

    # def test_read_spec(self,generatorBaseTestFixture):
    #     generatorBaseTestFixture.read_spec()
    #
    # def test_validate_function(self, generatorBaseTestFixture):
    #     generatorBaseTestFixture.validate_function()
    #
    # def test_start_service(self,serverBaseTestFixture):
    #     serverBaseTestFixture.start_service()
    #
    # def test_stop_server(self,serverBaseTestFixture):
    #     serverBaseTestFixture.stop_server()
