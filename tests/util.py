import oyaml as yaml
from cloudmesh.common.util import path_expand



def readyaml(name):
    with open(path_expand(name), "r") as stream:
        try:
            spec = yaml.safe_load(stream)
        except yaml.YAMLError as e:
            print(e)
            assert False, "Yaml file has syntax error"
    return spec
