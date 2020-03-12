###############################################################
# pytest -v --capture=no tests/test_generator.py
# pytest -v  tests/test_generator.py
# pytest -v --capture=no  tests/test_generator..py::Test_name::<METHODNAME>
###############################################################
import pytest
import yaml as yaml
import sys

from cloudmesh.common.StopWatch import StopWatch
from cloudmesh.common.util import HEADING
from cloudmesh.common.util import path_expand
from cloudmesh.common.Benchmark import Benchmark
from pprint import pprint

# sys.path.append("cloudmesh/openapi3/function")
#


#
# get the spec for the tests
#
with open("tests/sampleFunction.yaml", "r") as stream:
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

    def test_benchmark(self):
        HEADING()
        Benchmark.print(csv=True, sysinfo=False, tag="generator")
