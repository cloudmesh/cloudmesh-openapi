###############################################################
# pytest -v --capture=no tests/test_03_generator.py
# pytest -v  tests/test_03_generator.py
# pytest -v --capture=no  tests/test_generator..py::Test_name::<METHODNAME>
###############################################################
import os
import time
from pprint import pprint


from cloudmesh.common.Benchmark import Benchmark
from cloudmesh.common.util import HEADING

import sys
sys.path.append("./tests/Scikitlearn_tests")
from cloudmesh.openapi.scikitlearn import SklearnGeneratorFile as SklearngeneratorFile
import pytest
all_functions= True
import_class=False
input_sklibrary = 'sklearn.linear_model.LinearRegression'
model_tag = 'Linregfile2'

@pytest.mark.incremental
class Test:

    def test_SklearnGenerator(self):

        HEADING()
        Benchmark.Start()
        SklearngeneratorFile.SklearngeneratorFile(input_sklibrary, model_tag)
        Benchmark.Stop()
        assert True

    def test_benchmark(self):
        Benchmark.print(sysinfo=True, csv=True)
