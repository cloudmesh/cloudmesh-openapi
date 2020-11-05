###############################################################
# pytest -v --capture=no tests/test_03_generator.py
# pytest -v  tests/test_03_generator.py
# pytest -v --capture=no  tests/test_generator..py::Test_name::<METHODNAME>
###############################################################
from pprint import pprint

import pytest
import yaml as yaml
from cloudmesh.common.Benchmark import Benchmark
from cloudmesh.common.util import HEADING
from cloudmesh.openapi.registry.Registry import Registry
from cloudmesh.common.variables import Variables
from cloudmesh.common.util import path_expand

Registry.protocol(protocol="pickle")
variable=Variables()
filename= variable['filename'] or path_expand('./tests/server-cpu/cpu.yaml')
# sys.path.append("cloudmesh/openapi/function")
#


#
# get the spec for the tests
#

with open(filename, "r") as stream:
    try:
        spec = yaml.safe_load(stream)
    except yaml.YAMLError as e:
        print(e)
        assert False, "Yaml file has syntax error"


@pytest.mark.incremental
class TestGenerator:


    def test_registry_add(self):
        HEADING()

        Benchmark.Start()

        title = spec["info"]["title"]
        url = spec["servers"][0]["url"]

        print(f"add {title} -> {url}")
        registry = Registry()

        before = len(registry.list(name=title))

        pid = 1

        entry = registry.add(name=title, url=url, pid=pid)
        pprint (entry)

        after = len(registry.list(name=title))

        assert after == before + 1

        Benchmark.Stop()

    def test_registry_list_name(self):
        HEADING()

        Benchmark.Start()

        title = spec["info"]["title"]

        registry = Registry()

        entry = registry.list(name=title)
        pprint(entry)

        assert entry != None

        Benchmark.Stop()

    def test_registry_list(self):
        HEADING()

        Benchmark.Start()

        title = spec["info"]["title"]

        #print(f"delete {title}")
        registry = Registry()

        entry = registry.list()
        pprint(entry)

        assert len(entry) > 0

        Benchmark.Stop()

    def test_registry_delete(self):
        HEADING()


        Benchmark.Start()

        title = spec["info"]["title"]

        registry = Registry()
        entry = registry.list(name=title)

        # list before and use len()
        #before = 1
        before = len(entry)

        print(f"delete {title}")

        entry = registry.delete(name=title)
        print(f"{entry} entry deleted")

        # list after and use len

        after = len(registry.list(name=title)) # use len()

        assert before == after + 1

        Benchmark.Stop()


    def test_benchmark(self):
        HEADING()
        Benchmark.print(csv=True, sysinfo=False, tag="generator")