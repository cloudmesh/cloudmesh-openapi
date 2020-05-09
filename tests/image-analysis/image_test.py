from pprint import pprint

import pytest
import yaml as yaml
from cloudmesh.common.Shell import Shell
from cloudmesh.common.Benchmark import Benchmark
from cloudmesh.common.util import HEADING, path_expand
import os
import time

path = './tests/image-analysis'
baseurl = "http://127.0.0.1:8080/cloudmesh"

@pytest.mark.incremental
class TestGeneratorTestClass():
    def test_generate(self):
        """
        test whether python file can successfully be generated into yaml
        :return:
        """
        HEADING()

        Benchmark.Start()

        print("Generating yaml")

        try:
            Shell.run(f"cms openapi generate --all_functions --filename={path}/image.py")
            print("Successfully generated image.yaml")
        except Exception as e:
            print(e)
            assert False, "Could not generate"


        file_list = os.listdir(path)
        assert 'image.yaml' in file_list

        Benchmark.Stop()

    def test_yaml_syntax(self):
        """
        test whether yaml file generated has correct syntax
        :return:
        """
        HEADING()

        Benchmark.Start()
        print("Checking yaml syntax")
        with open(path_expand(f'{path}/image.yaml'), "r") as stream:
            try:
                spec = yaml.safe_load(stream)
                print('Yaml file has no errors')
            except yaml.YAMLError as e:
                print(e)
                assert False, "Yaml file has syntax error"

        Benchmark.Stop()

    def test_server(self):
        """
        test whether server can be started, check curl request, and stopped
        :return:
        """
        """
        function to test if the server is started and available to return
        a successful http code
        """
        HEADING()
        Benchmark.Start()

        os.system(f"cms openapi server start {path}/image.yaml")

        time.sleep(1)

        server_output = Shell.run("cms openapi server ps")
        assert "None" not in server_output
        Benchmark.Stop()

    def test_google_vision(self):
        """
        test google vision api response
        :return:
        """
        HEADING()
        Benchmark.Start()

        curl = f"curl -I {baseurl}/image/detect_text_google"

        response = Shell.run(curl)
        assert "200" in response
        Benchmark.Stop()

    def test_aws_rekognition(self):
        """
        test aws rekognition api response
        :return:
        """
        HEADING()
        Benchmark.Start()

        curl = f"curl -I {baseurl}/image/detect_text_aws"

        response = Shell.run(curl)
        assert "200" in response

        Benchmark.Stop()

    def test_server_stop(self):
        """
        test server stop
        :return:
        """
        HEADING()
        Benchmark.Start()
        os.system("cms openapi server stop image")

        curl = f"curl -I {baseurl}/image/detect_text_aws"
        response = Shell.run(curl)

        fail_message="Connection refuse"
        assert fail_message in response

        Benchmark.Stop()

    def test_benchmark(self):
        HEADING()
        Benchmark.print(csv=True, sysinfo=False, tag="generator")

