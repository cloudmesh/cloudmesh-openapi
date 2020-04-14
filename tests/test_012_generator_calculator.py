###############################################################
# pytest -v --capture=no tests/test_03_generator.py
# pytest -v  tests/test_03_generator.py
# pytest -v --capture=no  tests/test_generator..py::Test_name::<METHODNAME>
###############################################################
"""
# Headline

Here come document for test

"""
import time
from pprint import pprint
import sys
import pytest
import tests.util as util
from cloudmesh.common.Benchmark import Benchmark
from cloudmesh.common.Shell import Shell
from cloudmesh.common.util import HEADING
from cloudmesh.common.util import path_expand
from importlib import import_module
from cloudmesh.openapi.function.executor import Parameter
from cloudmesh.common.dotdict import dotdict
import types
from cloudmesh.shell.command import command, map_parameters

# for testing file which has function more than one, use below variable and also use dataforfunction dict
argumentsforfunction="cms openapi generate Calculator --filename=./tests/generator-calculator/calculator.py --all_functions"

# for testing file which is class , use below variable and also use dataforclass dict
argumentsforclass="cms openapi generate Calculator --filename=./tests/generator-testclass/calculator.py --import_class"

dataforclass = dotdict({
            "filename": './tests/generator-testclass/calculator.py',
            "import_class": True,
             "FUNCTION" : "Calculator",
            "all_functions":False,
        })

dataforfunction = dotdict({
            "filename": './tests/generator-testclass/calculator.py',
            "import_class": False,
            "all_functions":True,
        })

p = Parameter(dataforclass)

@pytest.mark.incremental
class TestGenerator:

    def test_generate(self):
        """
        function to validate paths information
        """
        HEADING()
        Benchmark.Start()
        Shell.run(argumentsforclass) #change variable based on your needs
        Benchmark.Stop()

    def test_read_spec(self):
        """
        function to check if YAML synatx is correct or not
        """
        global spec
        HEADING()
        Benchmark.Start()
        spec = util.readyaml(p.yamlfile)
        keys = spec.keys()
        assert "openapi" in keys
        assert "info" in keys
        assert "servers" in keys
        assert "paths" in keys

    def test_number_of_function(self):
        """
        function to check number of functions are same in py and yaml file.
        """
        HEADING()
        Benchmark.Start()
        sys.path.append(p.yamldirectory)
        imported_module = import_module(p.module_name)
        keys = spec.get('paths')
        paths= keys.keys()
        if (p.all_functions is True):
            for attr_name in dir(imported_module):
                if type(getattr(imported_module, attr_name)).__name__ == 'function':
                    assert f"/{p.function}/{attr_name}" in paths
        if (p.import_class is True):
            class_obj = getattr(imported_module, p.function)
            for attr_name in dir(class_obj):
                attr = getattr(class_obj, attr_name)
                if isinstance(attr, types.MethodType):
                    assert f"/{p.function}/{attr_name}" in paths

class rest:

    def test_service(self):
        """
        function to test if the server is started and available to return
        a successful http code
        """
        HEADING()
        Benchmark.Start()

        server_output = Shell.cms("openapi server start {filename}")
        assert server_output.__contains__("starting server")

        time.sleep(2)
        baseurl = "http://127.0.0.1:8080/cloudmesh"

        curl = f"curl {baseurl}/cpu"

        response = Shell.run(curl)
        assert response.__contains__("200")

        Shell.cms("openapi server stop cpu")
        response = Shell.run(curl)
        fail_message = "Failed to connect to 127.0.0.1 port 80: Connection refuse"
        assert response.__contains__(fail_message)

        Benchmark.Stop()

