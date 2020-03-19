###############################################################
# pytest -v --capture=no tests/test_server_cms_cpu.py
# pytest -v  tests/test_server_cms_cpu.py
# pytest -v --capture=no  tests/test_server_cms_cpu..py::Test_server_cms::<METHODNAME>
###############################################################
import pytest
from cloudmesh.common.Shell import Shell
from cloudmesh.common.debug import VERBOSE
from cloudmesh.common.util import HEADING
from cloudmesh.common.Benchmark import Benchmark

Benchmark.debug()

cloud = "local"

name = "cpu"

@pytest.mark.incremental
class TestServerCms:

    def test_start(self):
        HEADING()

        Benchmark.Start()
        result = Shell.execute(f"cms openapi3 server start ./tests/{name}.yaml", shell=True)
        Benchmark.Stop()
        VERBOSE(result)

        #assert False # find test

    def test_stop(self):
        HEADING()

        Benchmark.Start()
        result = Shell.execute(f"cms openapi3 server stop {name}", shell=True)
        Benchmark.Stop()
        VERBOSE(result)

        #assert False # find test

    def test_ui(self):
        HEADING()
        url="http://127.0.0.1:8080/cloudmesh/ui/"
        Benchmark.Start()
        # result = Shell.execute(f"cms openapi3 server stop {name}", shell=True)
        result = requests.get('https://api.github.com/user')
        assert result.status_code == 200
        # >> > r.headers['content-type']
        # 'application/json; charset=utf8'
        # >> > r.encoding
        # 'utf-8'
        # >> > r.text
        # u'{"type":"User"...'
        # >> > r.json()
        # {u'private_gists': 419, u'total_private_repos': 77, ...}
        Benchmark.Stop()
        VERBOSE(result)

        # assert False # find test

    def test_cpu(self):
        HEADING()
        url = "http://127.0.0.1:8080/cloudmesh/cpu"
        Benchmark.Start()
        # result = Shell.execute(f"cms openapi3 server stop {name}", shell=True)
        result = requests.get('https://api.github.com/user')
        assert result.status_code == 200
        # >> > r.headers['content-type']
        # 'application/json; charset=utf8'
        # >> > r.encoding
        # 'utf-8'
        # >> > r.text
        # u'{"type":"User"...'
        # >> > r.json()
        # {u'private_gists': 419, u'total_private_repos': 77, ...}
        Benchmark.Stop()
        VERBOSE(result)

        # assert False # find test

    def test_benchmark(self):
        HEADING()
        Benchmark.print(csv=True, tag=cloud)
