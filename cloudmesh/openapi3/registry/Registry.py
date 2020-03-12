from cloudmesh.mongo.DataBaseDecorator import DatabaseUpdate
from cloudmesh.common.Shell import Shell
import yaml
class Registry:

    def __init__(self):
        pass

    @DatabaseUpdate()
    def add(self, name=None, url=None, pid=None):
        entry = {
            "cm": {
                "cloud": "local",
                "kind": "registry",
                "name": name,
                "dirver": None
            },
            "url": url,
            "name": name
        }
        if pid:
            entry["pid"] = pid
        return entry

    def add_form_file(self, filename):
        """

        :param filename:
        :return:
        """
        with open("tests/sampleFunction.yaml", "r") as stream:
            try:
                spec = yaml.safe_load(stream)
            except yaml.YAMLError as e:
                print(e)
                assert False, "Yaml file has syntax error"

        title = spec["info"]["title"]
        url = spec["servers"][0]["url"]

        registry = Registry()
        entry = registry.add(name=title, url=url)
        return entry

    def delete(self, name=None):
        """

        :param name:
        :return:
        """
        raise NotImplementedError

        # CmDatabase()

    def list(self, name=None):
        """

        :param name:  if none all
        :return:
        """
        raise NotImplementedError

    def start(self):
        """
        start the registry

        possibly not needed as we have cms start

        :return:
        """
        r = Shell.cms("start")

    def stop(self):
        """
        stop the registry

        possibly not needed as we have cms start
        this will not just sto the registry but mongo

        :return:
        """
        r = Shell.cms("stop")
