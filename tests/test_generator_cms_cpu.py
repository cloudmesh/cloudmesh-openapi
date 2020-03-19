###############################################################
# pytest -v --capture=no tests/test_generator_cms_cpu.py
# pytest -v  tests/test_generator_cms_cpu.py
# pytest -v --capture=no  tests/test_generator_cms_cpu..py::Test_generator_cms_cpu::<METHODNAME>
###############################################################
import pytest
from cloudmesh.common.Shell import Shell
from cloudmesh.common.debug import VERBOSE
from cloudmesh.common.util import HEADING
from cloudmesh.common.Benchmark import Benchmark

Benchmark.debug()

cloud = "local"


@pytest.mark.incremental
class TestGeneratorCmsCpu:

    def test_start(self):
        HEADING()

        Benchmark.Start()
        result = Shell.execute("cms openapi3 server start ./tests/cpu.yaml", shell=True)
        Benchmark.Stop()
        VERBOSE(result)

        #assert False # find test

    def test_stop(self):
        HEADING()

        Benchmark.Start()
        result = Shell.execute("cms openapi3 server stop cpu", shell=True)
        Benchmark.Stop()
        VERBOSE(result)

        #assert False # find test


    def test_benchmark(self):
        HEADING()
        Benchmark.print(csv=True, tag=cloud)
