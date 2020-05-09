import requests
###############################################################
# pytest -v --capture=no tests/test_openapi.py
# pytest -v  tests/test_openapi.py
# pytest -v --capture=no  tests/test_openapi..py::test_openapi::<METHODNAME>
###############################################################

from pprint import pprint

import pytest
from cloudmesh.common.Printer import Printer
from cloudmesh.common.util import HEADING
from cloudmesh.common.Benchmark import Benchmark
from cloudmesh.configuration.Config import Config
from pprint import pprint

Benchmark.debug()

cloud = "local"

@pytest.mark.incremental
class TestName:

    def test_home(self):
        HEADING()
        Benchmark.Start()
        r = requests.get('http://localhost:8080/cloudmesh/forecast')

        assert r.status_code == 200
        assert r.headers['content-type'] == "application/json"
        print(r.json)
        d = r.json()
        pprint (r.content)
        Benchmark.Stop()

    def test_file_upload(self):
        HEADING()

        Benchmark.Start()

        r = requests.get('http://localhost:8080/cloudmesh/forecast/upload" -F "upload=@~\\.cloudmesh\\upload-file\\countries-aggregated.csv')

        assert r.status_code == 200
        assert r.headers['content-type'] == "application/json"

        d = r.json()
        pprint(r.content)

        Benchmark.Stop()

    def test_validate_data(self):
        HEADING()

        Benchmark.Start()

        r = requests.get('http://localhost:8080/cloudmesh/forecast/validate_data" -F "upload=@~\\.cloudmesh\\upload-file\\countries-aggregated.csv')

        assert r.status_code == 200
        assert r.headers['content-type'] == "application/json"

        d = r.json()
        pprint(r.content)

        Benchmark.Stop()


    def test_split_data(self):
        url = 'http://localhost:8080/cloudmesh/forecast/split_data?split_pct=20'
        Benchmark.Start()
        r = requests.get(url)
        assert r.status_code == 200
        assert r.headers['content-type'] == "application/json"
        d = r.json()
        pprint(r.content)
        Benchmark.Stop()

    def test_initialize_cloud(self):
        url = 'http://localhost:8080/cloudmesh/forecast/aws'
        Benchmark.Start()
        response = requests.put(url)
        # validate response code
        assert response.status_code == 200
        assert response.headers['content-type'] == "application/json"
        d = response.json()
        pprint(response.content)
        Benchmark.Stop()

    def test_create_forecast(self):
        url = 'http://localhost:8080/cloudmesh/forecast/create_forecast?country=Austrailia'
        Benchmark.Start()
        response = requests.put(url)
        # validate response code
        assert response.status_code == 200
        assert response.headers['content-type'] == "application/json"
        d = response.json()
        pprint(response.content)
        Benchmark.Stop()

    def test_lookup_forecast(self):
        url = 'http://localhost:8080/cloudmesh/forecast/lookupForecast?countryName=Austrailia'
        Benchmark.Start()
        response = requests.put(url)
        # validate response code
        assert response.status_code == 200
        assert response.headers['content-type'] == "application/json"
        d = response.json()
        pprint(response.content)
        Benchmark.Stop()
