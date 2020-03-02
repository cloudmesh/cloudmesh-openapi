import pytest
import yaml as yaml


@pytest.mark.incremental
class TestGenerator:

    def test_yaml_syntax(self):
        """ function to check if YAML synatx is correct or not"""
        with open("../cloudmesh/openapi3/function/sampleFunction.yaml", "r") as stream:
            try:
                yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                assert False, "Yaml file has syntax error"

    def test_openapi_info_servers_paths(self):
        """ function to check if YAML contains opeaapi , info , servers and paths information """
        with open("../cloudmesh/openapi3/function/sampleFunction.yaml", "r") as stream:
            try:
                keys = yaml.safe_load(stream).keys()
                assert keys.__contains__("openapi"), "openapi is not found"
                assert keys.__contains__("info"), "info is not found"
                assert keys.__contains__("servers"), "servers is not found"
                assert keys.__contains__("paths"), "paths is not found"
            except yaml.YAMLError as exc:
                assert False, "Yaml file has syntax error"

    def test_paths(self):
        """ function to check if YAML contains opeaapi , info , servers and paths information """
        with open("../cloudmesh/openapi3/function/sampleFunction.yaml", "r") as stream:
            try:
                paths = yaml.safe_load(stream).get("paths")
                print(paths is None)
                assert paths is not None , "paths value should not be null"
            except yaml.YAMLError as exc:
                assert False, "Yaml file has syntax error"
