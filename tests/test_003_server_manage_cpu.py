###############################################################
# pytest -v --capture=no tests/test_03_generator.py
# pytest -v  tests/test_03_generator.py
# pytest -v --capture=no  tests/test_generator..py::Test_name::<METHODNAME>
###############################################################
import os
import time
from pprint import pprint

import pytest
import tests.util as util
from cloudmesh.common.Benchmark import Benchmark
from cloudmesh.common.Shell import Shell
from cloudmesh.common.util import HEADING
from cloudmesh.common.variable import Variables

variable = Variables()
filename = variable['filename']


# filename = "./tests/server-cpu/cpu.yaml"

@pytest.mark.incremental
class TestGenerator:

    def test_read_spec(self):
        """
        function to check if YAML synatx is correct or not
        """
        global spec

        HEADING()
        Benchmark.Start()
        spec = util.readyaml(filename)
        keys = spec.keys()

        pprint(spec)
        pprint(keys)
        assert "openapi" in keys
        assert "info" in keys
        assert "servers" in keys
        assert "paths" in keys
        assert "A simple service" in str(spec)

    def test_paths(self):
        """
        function to validate paths information
        """
        HEADING()
        global spec

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

    def test_service_start(self):
        """
        function to test if the server is starts
        """
        HEADING()

        os.chdir("tests")
        test_loc = Shell.pwd().strip() + "/"

        assert test_loc == "tests/"

        Benchmark.Start()
        server_output = Shell.cms("openapi server start {filename}")
        Benchmark.Start()

        assert server_output.__contains__("starting server")

    def test_service_get(self):
        """
        function to test if the server is returns the result from the url
        """
        HEADING()

        time.sleep(2)
        baseurl = "http://127.0.0.1:8080/cloudmesh"

        curl = f"curl {baseurl}/cpu"

        Benchmark.Start()
        response = Shell.run(curl)
        Benchmark.Stop()

        assert response.__contains__("200")

    def test_service_stop(self):
        """
        function to test if the server is returns the result from the url
        """
        HEADING()

        Shell.cms("openapi server stop cpu")
        response = Shell.run(curl)
        fail_message = "Failed to connect to 127.0.0.1 port 80: Connection refuse"
        assert response.__contains__(fail_message)

        Benchmark.Stop()

    def test_benchmark(self):
        HEADING()
        Benchmark.print(csv=True, sysinfo=False, tag="generator")
