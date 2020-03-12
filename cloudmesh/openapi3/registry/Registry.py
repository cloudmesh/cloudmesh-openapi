from cloudmesh.mongo.DataBaseDecorator import DatabaseUpdate
from cloudmesh.common.Shell import Shell

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
        raise NotImplementedError

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
            entries = cm.find(cloud="local", kind="registry")
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
