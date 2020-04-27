import time
from pprint import pprint

import pytest
from cloudmesh.common.Benchmark import Benchmark
from cloudmesh.common.Shell import Shell
from cloudmesh.common.util import HEADING
import requests

test_dir = "./tests/generator-natural-lang/"
func_filename = "natural-lang-analysis.py"
yaml_filename = "natural-lang-analysis.yaml"
sample_text_file = "bladerunner-mixed.txt"

func_path = test_dir + func_filename
yaml_path = test_dir + yaml_filename

@pytest.mark.incremental
class TestGenerator:

    def test_generate_individual_function(self):
        HEADING()

        Benchmark.Start()

        Shell.run(
            f"cms openapi generate analyze --filename={func_path}")

        file_list = Shell.run(f"ls {test_dir}")

        assert yaml_filename in file_list

        Benchmark.Stop()

@pytest.mark.incremental
class TestAPI:

    def start_server_from_generated(self):
        HEADING()
        Benchmark.Start()

        Shell.cms(f"openapi server start {yaml_path}")

        res_code = ""

        while res_code != "200":

            response_google = requests.get(
                f"http://127.0.0.1:8080/cloudmesh/analyze?filename={sample_text_file}&cloud='google'")
            res_code = str(response_google.status_code)
            assert res_code == "200"

            response_azure = requests.get(
                f"http://127.0.0.1:8080/cloudmesh/analyze?filename={sample_text_file}&cloud='azure'")
            res_code = str(response_azure.status_code)
            assert res_code == "200"

        Benchmark.Stop()

    def stop_server(self):
        HEADING()
        Benchmark.Start()

        Shell.cms("openapi server stop analyze")

        res_code = "200"

        while res_code == "200":
            response = requests.get("http://127.0.0.1:8080/cloudmesh/ui")
            res_code = str(response.status_code)
            assert res_code != "200"






