###############################################################
# pytest -v --capture=no tests/test_server_cms_sampleFunction.py
# pytest -v  tests/test_server_cms_sampleFunction.py
# pytest -v --capture=no  tests/test_server_cms_sampleFunction..py::Test_server_cms_sampleFunction::<METHODNAME>
###############################################################
import pytest
from cloudmesh.common.Shell import Shell
from cloudmesh.common.debug import VERBOSE
from cloudmesh.common.util import HEADING
from cloudmesh.common.Benchmark import Benchmark

Benchmark.debug()

cloud = "local"


@pytest.mark.incremental
class TestServerCmsSampleFunction:

    def test_start(self):
        HEADING()

        Benchmark.Start()
        result = Shell.execute("cms openapi3 server start ./tests/sampleFunction.yaml", shell=True)
        Benchmark.Stop()
        VERBOSE(result)

        #assert False # find test

    def test_stop(self):
        HEADING()

        Benchmark.Start()
        result = Shell.execute("cms openapi3 server stop sampleFunction", shell=True)
        Benchmark.Stop()
        VERBOSE(result)

        #assert False # find test


    def test_benchmark(self):
        HEADING()
        Benchmark.print(csv=True, tag=cloud)
