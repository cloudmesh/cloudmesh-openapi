###############################################################
# pytest -v --capture=no tests/test_03_generator.py
# pytest -v  tests/test_03_generator.py
# pytest -v --capture=no  tests/test_generator..py::Test_name::<METHODNAME>
###############################################################
import os
import time
from pprint import pprint
import sys
sys.path.append("./tests/Scikitlearn-tests")
from cloudmesh.openapi.scikitlearn import SklearnGenerator
from tests.generator import LogisticRegression
import pytest
from cloudmesh.common.dotdict import dotdict

filename="./tests/generator/LogisticRegression.py"
all_functions= True
import_class=False
X = [1,2,3,4,5,6,7,8]
y = [1,3,5,7]
sample_weight = [1,1,1,1]
X_shape_x = 4
X_shape_y = 2

@pytest.mark.incremental
class LogisticRegressiontest:

    def fit(X,y,sample_weight,X_shape_x,X_shape_y):
        """
        function to test if the server is started and available to return
        a successful http code
        """
        HEADING()
        Benchmark.Start()
        LogisticRegression.fit(X,y,sample_weight,X_shape_x,X_shape_y)
        Benchmark.Stop()
        assert True

    def score(X,y,sample_weight,X_shape_x,X_shape_y):
        """
        function to test if the server is started and available to return
        a successful http code
        """
        HEADING()
        Benchmark.Start()
        LogisticRegression.score(X,y,sample_weight,X_shape_x,X_shape_y)
        Benchmark.Stop()
        assert True

    def predict_proba(X,X_shape_x,X_shape_y):
        """
        function to test if the server is started and available to return
        a successful http code
        """
        HEADING()
        Benchmark.Start()
        LogisticRegression.predict_proba(X,y,sample_weight,X_shape_x,X_shape_y)
        Benchmark.Stop()
        assert True

    def predict_log_proba(X,X_shape_x,X_shape_y):
        """
        function to test if the server is started and available to return
        a successful http code
        """
        HEADING()
        Benchmark.Start()
        LogisticRegression.predict_log_proba(X,y,sample_weight,X_shape_x,X_shape_y)
        Benchmark.Stop()
        assert True

    def predict(X,X_shape_x,X_shape_y):
        """
        function to test if the server is started and available to return
        a successful http code
        """
        HEADING()
        Benchmark.Start()
        LogisticRegression.predict(X,y,sample_weight,X_shape_x,X_shape_y)
        Benchmark.Stop()
        assert True

    def test_benchmark(self):
        Benchmark.print(sysinfo=True, csv=True, tag=service)
