###############################################################
# pytest -v --capture=no tests/test_server_cms_cpu.py
# pytest -v  tests/test_server_cms_cpu.py
# pytest -v --capture=no  tests/test_server_cms_cpu..py::Test_server_sampleFunction::<METHODNAME>
###############################################################
import pytest
from cloudmesh.common.Benchmark import Benchmark
from cloudmesh.common.Shell import Shell
from cloudmesh.common.debug import VERBOSE
from cloudmesh.common.util import HEADING

Benchmark.debug()

cloud = "local"

name = "cpu"

@pytest.mark.incremental
class TestServerSampleFunction:

    def test_start(self):
        HEADING()

        raise ValueError("THIS IS NOT PROPERLY USED. SEE THE MANUAL")

        # there should not be a seperate test needed all test must work on all osses
        #
        Benchmark.Start()
        result = Shell.execute(
            f"cms openapi server start .///tests///server-cpu///{name}.yaml --os",
            shell=False)
        Benchmark.Stop()
        VERBOSE(result)

        #assert False # find test

    '''
    def test_stop(self):
        HEADING()

        Benchmark.Start()
        result = Shell.execute(f"cms openapi server stop {name}", shell=True)
        Benchmark.Stop()
        VERBOSE(result)

        #assert False # find test
    '''

    def test_benchmark(self):
        HEADING()
        Benchmark.print(csv=True, tag=cloud)
