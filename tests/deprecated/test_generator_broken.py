###############################################################
# pytest -v --capture=no tests/test_03_generator.py
# pytest -v  tests/test_03_generator.py
# pytest -v --capture=no  tests/test_generator..py::Test_name::<METHODNAME>
###############################################################
import sys

import pytest
import yaml as yaml

sys.path.append("cloudmesh/openapi/function")
import tests.sample_function_gen as testfun
from cloudmesh.common.util import HEADING
from cloudmesh.common.Benchmark import Benchmark

@pytest.mark.incremental
class TestGenerator:

    def test_yaml_syntax(self):
        """
        function to check if YAML synatx is correct or not
        """
        HEADING()
        Benchmark.Start()
        with open("cloudmesh/openapi/function/sampleFunction.yaml",
                  "r") as stream:
            try:
                yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                assert False, "Yaml file has syntax error"
        Benchmark.Stop()

    def test_openapi_info_servers_paths(self):
        """
        function to check if YAML contains opeaapi, info ,servers, and paths
        information
        """
        HEADING()

        Benchmark.Start()

        with open("cloudmesh/openapi/function/sampleFunction.yaml",
                  "r") as stream:
            try:
                keys = yaml.safe_load(stream).keys()
                assert keys.__contains__("openapi"), "openapi is not found"
                assert keys.__contains__("info"), "info is not found"
                assert keys.__contains__("servers"), "servers is not found"
                assert keys.__contains__("paths"), "paths is not found"
            except yaml.YAMLError as exc:
                assert False, "Yaml file has syntax error"
        Benchmark.Stop()

    def test_paths(self):
        """
        function to validate paths information
        """
        HEADING()

        Benchmark.Start()
        with open("cloudmesh/openapi/function/sampleFunction.yaml",
                  "r") as stream:
            try:
                paths = yaml.safe_load(stream).get("paths")
                assert paths is not None, "paths value should not be null"
                assert paths.keys().__contains__(
                    "/" + testfun.sampleFunction.__name__), "Resource name should be " + testfun.sampleFunction.__name__
                getOperation = paths.get("/" + testfun.sampleFunction.__name__)
                assert getOperation.keys().__contains__(
                    "get"), "get operation is missing "
                parameters = getOperation.get("get").get("parameters")
                # assert len(parameters)+1==len(testfun.sampleFunction.__annotations__.items()), "get operation is missing "
            except yaml.YAMLError as exc:
                assert False, "Yaml file has syntax error"
        Benchmark.Stop()

    def test_benchmark(self):
        HEADING()
        Benchmark.print(csv=True, sysinfo=False, tag=cloud)
