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
from tests.generator import LinearRegression

import sys
sys.path.append("./tests/Scikitlearn_tests")
import pytest

filename="./tests/generator/LinearRegression.py"
all_functions= True
import_class=False
X = [1,2,3,4,5,6,7,8]
y = [1,3,5,7]
sample_weight = [1,1,1,1]
X_shape_x = 4
X_shape_y = 2

@pytest.mark.incremental
class Test:

    def test_fit(self):
        """
        function to test the fit
        """

        HEADING()
        Benchmark.Start()
        LinearRegression.fit(X,y,X_shape_x,X_shape_y)
        Benchmark.Stop()
        assert True

    def test_score(self):
        """
        function to test the score
        """
        HEADING()
        Benchmark.Start()
        score = LinearRegression.score(X,y,X_shape_x,X_shape_y)
        Benchmark.Stop()
        assert score > 0

    # def test_predict_proba(self):
    #     """
    #     function to test the predict_proba
    #     """
    #     HEADING()
    #     Benchmark.Start()
    #     LinearRegression.predict_proba(X,X_shape_x,X_shape_y)
    #     Benchmark.Stop()
    #     assert True
    #
    # def test_predict_log_proba(self):
    #     """
    #     function to test the predict_log_proba
    #     """
    #     HEADING()
    #     Benchmark.Start()
    #     LogisticRegression.predict_log_proba(X,X_shape_x,X_shape_y)
    #     Benchmark.Stop()
    #     assert True

    def test_predict(self):
        """
        function to test the predict
        """
        HEADING()
        Benchmark.Start()
        LinearRegression.predict(X,X_shape_x,X_shape_y)
        Benchmark.Stop()
        assert True

    def test_benchmark(self):
        Benchmark.print(sysinfo=True, csv=True)
