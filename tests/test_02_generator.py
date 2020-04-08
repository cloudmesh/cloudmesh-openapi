###############################################################
# pytest -v --capture=no tests/test_02_generator.py
# pytest -v  tests/test_02_generator.py
# pytest -v --capture=no  tests/test_generator..py::Test_name::<METHODNAME>
###############################################################
import os
import time
from pprint import pprint

import pytest
import yaml as yaml
from cloudmesh.common.Benchmark import Benchmark
from cloudmesh.common.Shell import Shell
from cloudmesh.common.util import HEADING

# sys.path.append("cloudmesh/openapi/function")
#

# py_path = "./server-sampleFunction/samplefunction_server.py"
# yaml_path = "./server-sampleFunction/sampleFunction.yaml"

yaml_file = "./generator/sampleFunction.yaml"
#
# get the spec for the tests
#
with open(yaml_file, "r") as stream:
    try:
        spec = yaml.safe_load(stream)
    except yaml.YAMLError as e:
        print(e)
        assert False, "Yaml file has syntax error"


@pytest.mark.incremental
class TestGenerator:

    def test_spec(self):
        """
        function to check if YAML synatx is correct or not
        """
        HEADING()
        Benchmark.Start()
        pprint (spec)
        Benchmark.Stop()

    def test_openapi_info_servers_paths(self):
        """
        function to check if YAML contains opeaapi, info ,servers, and paths
        information
        """
        HEADING()

        Benchmark.Start()

        keys = spec.keys()
        pprint(keys)
        assert keys.__contains__("openapi"), "openapi is not found"
        assert keys.__contains__("info"), "info is not found"
        assert keys.__contains__("servers"), "servers is not found"
        assert keys.__contains__("paths"), "paths is not found"

        Benchmark.Stop()

    def test_paths(self):
        """
        function to validate paths information
        """
        HEADING()

        import tests.sample_function_gen as testfun

        paths = spec.get("paths")
        name = testfun.sampleFunction.__name__
        getOperation = paths.get(f"/{name}")

        assert paths is not None, "paths value should not be null"
        assert paths.keys().__contains__(f"/{name}"), "Resource name should be {name}"
        assert getOperation.keys().__contains__("get"), "get operation is missing "
        parameters = getOperation.get("get").get("parameters")
        # assert len(parameters)+1==len(testfun.sampleFunction.__annotations__.items()), "get operation is missing "

        Benchmark.Stop()

    def test_real(self):
        """
        function to test if the server is started and available to return
        a successful http code
        """
        HEADING()
        Benchmark.Start()

        os.chdir("tests")
        test_loc = Shell.pwd()
        test_loc = test_loc.strip() + "/"

        assert test_loc == "tests/"

        server_output = Shell.cms("openapi server start ./server-cpu/cpu.yaml")
        assert server_output.__contains__("starting server")

        time.sleep(2)
        baseurl = "http://127.0.0.1:8080/cloudmesh"

        curl = f"curl {baseurl}/cpu"

        response = Shell.run(curl)
        assert response.__contains__("200")

        Shell.cms("openapi server stop cpu")
        response = Shell.run(curl)
        fail_message="Failed to connect to 127.0.0.1 port 80: Connection refuse"
        assert response.__contains__(fail_message)

        Benchmark.Stop()

    def test_benchmark(self):
        HEADING()
        Benchmark.print(csv=True, sysinfo=False, tag="generator")
