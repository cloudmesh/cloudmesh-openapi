from cloudmesh.mongo.DataBaseDecorator import DatabaseUpdate
from cloudmesh.common.Shell import Shell
from cloudmesh.mongo.CmDatabase import CmDatabase

class Registry:

    def __init__(self):
        pass

    @DatabaseUpdate()
    def add(self, name=None, url=None):
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
        return entry

    def add_from_file(self, filename):
        """

        :param filename:
        :return:
        """
        spec = open(filename)
        title = spec["info"]["title"]
        url = spec["servers"][0]["url"]

        registry = Registry()

        entry = registry.add(name=title, url=url)

    def delete(self, name=None):
        """

        :param name:
        :return:
        """
        raise NotImplementedError

    def list(self, name=None):
        """

        :param name:  if none all
        :return:
        """

        cm = CmDatabase()
        for kind in ['vm', "image", "flavor"]:
            entries = cm.find(cloud="local", kind='registry')
        print(entries)

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
