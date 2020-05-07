###############################################################
# pytest -v --capture=no tests/test_03_generator.py
# pytest -v  tests/test_03_generator.py
# pytest -v --capture=no  tests/test_generator..py::Test_name::<METHODNAME>
###############################################################
import sys
sys.path.append("./tests/lib")
from generator_test import GeneratorBaseTest, ServerBaseTest
from tests.generator import LinearRegression
import pytest

from cloudmesh.common.Benchmark import Benchmark
from cloudmesh.common.util import HEADING
from cloudmesh.management.configuration.name import Name
service ="openapi"
Benchmark.debug()
X = [1,2,3,4,5,6,7,8]
y = [1,3,5,7]
sample_weight = [1,1,1,1]
X_shape_x = 4
X_shape_y = 2

filename="./tests/generator/LinearRegression.py"
all_functions= True
import_class=False

@pytest.mark.incremental
class TestGeneratorTestClass():


    @pytest.fixture(scope="module")
    def generatorBaseTestFixture(self):
        gen= GeneratorBaseTest(filename,all_functions,import_class)
        return gen

    @pytest.fixture(scope="module")
    def serverBaseTestFixture(self):
        server = ServerBaseTest()
        return server


    def test_copy_file(self,generatorBaseTestFixture):
        generatorBaseTestFixture.copy_py_file()

    def test_generate(self,generatorBaseTestFixture):
        """
        function to validate paths information
        """
        generatorBaseTestFixture.generate()

    def test_read_spec(self,generatorBaseTestFixture):
        generatorBaseTestFixture.read_spec()

    def test_validate_function(self, generatorBaseTestFixture):
        generatorBaseTestFixture.validate_function()

    def test_fit(self):
        """
        function to test if the server is started and available to return
        a successful http code
        """

        HEADING()
        Benchmark.Start()
        LinearRegression.fit(X, y, sample_weight, X_shape_x, X_shape_y)
        Benchmark.Stop()
        assert True

    def test_score(self):
        """
        function to test the score
        """
        HEADING()
        Benchmark.Start()
        score = LinearRegression.score(X,y,sample_weight,X_shape_x,X_shape_y)
        Benchmark.Stop()
        assert score > 0

    def test_predict(self):
        """
        function to test the predict
        """
        HEADING()
        Benchmark.Start()
        LinearRegression.predict(X,X_shape_x,X_shape_y)
        Benchmark.Stop()
        assert True

    def test_start_service(self,serverBaseTestFixture):
        serverBaseTestFixture.start_service()

    def test_stop_server(self,serverBaseTestFixture):
        serverBaseTestFixture.stop_server()

    def test_delete_build_file(self, generatorBaseTestFixture):
        generatorBaseTestFixture.delete_file()

    def test_benchmark(self):
        Benchmark.print(sysinfo=True, csv=True, tag=service)

