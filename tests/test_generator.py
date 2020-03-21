###############################################################
# pytest -v --capture=no tests/test_generator.py
# pytest -v  tests/test_generator.py
# pytest -v --capture=no  tests/test_generator..py::Test_name::<METHODNAME>
###############################################################
import pytest
import yaml as yaml
import time
import sys


from cloudmesh.common.StopWatch import StopWatch
from cloudmesh.common.util import HEADING
from cloudmesh.common.util import path_expand
from cloudmesh.common.Benchmark import Benchmark
from pprint import pprint
from cloudmesh.common.Shell import Shell
from cloudmesh.mongo.CmDatabase import CmDatabase

from cloudmesh.mongo.DataBaseDecorator import DatabaseUpdate
from cloudmesh.openapi3.registry.Registry import Registry
# sys.path.append("cloudmesh/openapi3/function")
#

#
# get the spec for the tests
#
with open("./generator/sampleFunction.yaml", "r") as stream:
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

        Shell.run("cd ~/cm/cloudmesh-openapi/tests/")
        test_loc = Shell.run("pwd")
        test_loc = test_loc.strip() + "/"

        assert test_loc == "/Users/andrewgoldfarb/e516-spring/cm/cloudmesh-openapi/tests/"

        server_output = Shell.cms("openapi3 server start ./server-cpu/cpu.yaml")
        assert server_output.__contains__("starting server")

        time.sleep(2)
        baseurl = "http://127.0.0.1:8080/cloudmesh"
        response = Shell.run("curl " + baseurl + "/cpu")
        assert response.__contains__("200")

        Shell.cms("openapi3 server stop cpu")
        response = Shell.run("curl " + baseurl + "/cpu")
        fail_message="Failed to connect to 127.0.0.1 port 80: Connection refuse"
        assert response.__contains__(fail_message)

        Benchmark.Stop()

    def test_benchmark(self):
        HEADING()
        Benchmark.print(csv=True, sysinfo=False, tag="generator")
