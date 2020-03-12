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
from cloudmesh.mongo.DataBaseDecorator import DatabaseUpdate
from cloudmesh.openapi3.registry.Registry import Registry
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


    def test_registry_add(self):
        HEADING()

        Benchmark.Start()

        title = spec["info"]["title"]
        url = spec["servers"][0]["url"]

        print(f"add {title} -> {url}")
        registry = Registry()

        pid = 1

        entry = registry.add(name=title, url=url, pid=pid)
        pprint (entry)

        # ASSERT MISSING

        Benchmark.Stop()

    def test_registry_list_name(self):
        HEADING()

        Benchmark.Start()

        title = spec["info"]["title"]

        print(f"delete {title}")
        registry = Registry()

        entry = registry.list(name=title)
        pprint(entry)

        # ASSERT MISSING

        Benchmark.Stop()

    def test_registry_list(self):
        HEADING()

        Benchmark.Start()

        title = spec["info"]["title"]

        print(f"delete {title}")
        registry = Registry()

        entry = registry.list()
        pprint(entry)

        # ASSERT MISSING

        Benchmark.Stop()

    def test_registry_delete(self):
        HEADING()
        # list before and use len()

        before = 1

        Benchmark.Start()

        title = spec["info"]["title"]

        print(f"delete {title}")
        registry = Registry()

        entry = registry.delete(name=title)
        pprint (entry)
        # list after and use len

        after = 1 # use len()

        assert before == after + 1


        Benchmark.Stop()


    def test_benchmark(self):
        HEADING()
        Benchmark.print(csv=True, sysinfo=False, tag="generator")
