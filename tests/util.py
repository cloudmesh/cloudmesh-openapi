import oyaml as yaml


def readyaml(name):
    with open(name, "r") as stream:
        try:
            spec = yaml.safe_load(stream)
        except yaml.YAMLError as e:
            print(e)
            assert False, "Yaml file has syntax error"
    return spec
