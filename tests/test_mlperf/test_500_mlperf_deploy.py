###############################################################
# pytest -v --capture=no tests/test_server_cms_cpu.py
# pytest -v  tests/test_server_cms_cpu.py
# pytest -v --capture=no  tests/test_server_cms_cpu..py::Test_server_cms::<METHODNAME>
###############################################################
import os
import time

import pytest
import requests
from cloudmesh.common.Benchmark import Benchmark
from cloudmesh.common.debug import VERBOSE
from cloudmesh.common.util import HEADING
from cloudmesh.common.Shell import Shell

Benchmark.debug()

cloud = "local"

name = "cpu"
yaml_file = "./tests/{name}.yaml"
@pytest.mark.incremental
class Test_mlperf_deploy:

    def test_deploy(self):
        HEADING()

        Benchmark.Start()

        result = Shell.live(f"echo todo")

        Benchmark.Stop()

        assert "todo" in result


    def test_benchmark(self):
        HEADING()
        Benchmark.print(csv=True, sysinfo=False, tag="generator")
