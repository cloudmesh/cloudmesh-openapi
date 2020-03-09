###############################################################
# pytest -v --capture=no tests/1_local/test_kmeans.py
# pytest -v  tests/1_local/test_name.py
# pytest -v --capture=no  tests/1_local/test_name..py::Test_name::<METHODNAME>
###############################################################
import pytest
from cloudmesh.common.Shell import Shell
from cloudmesh.common.debug import VERBOSE
from cloudmesh.common.util import HEADING
from cloudmesh.common.Benchmark import Benchmark

Benchmark.debug()

cloud= "local"

@pytest.mark.incremental
class TestKmeans:

    def test_help(self):
        HEADING()

        Benchmark.Start()
        result = Shell.execute("cms help", shell=True)
        Benchmark.Stop()
        VERBOSE(result)

        assert "quit" in result
        assert "clear" in result

    def test_vm(self):
        HEADING()
        Benchmark.Start()
        result = Shell.execute("cms help vm", shell=True)
        Benchmark.Stop()
        VERBOSE(result)

        assert "['sample1', 'sample2', 'sample3', 'sample18']" in result

    def test_help_again(self):
        HEADING()

        Benchmark.Start()
        result = Shell.execute("cms help", shell=True)
        Benchmark.Stop()
        VERBOSE(result)

        assert "quit" in result
        assert "clear" in result

    def test_benchmark(self):
        HEADING()
        Benchmark.print(csv=True, tag=cloud)
