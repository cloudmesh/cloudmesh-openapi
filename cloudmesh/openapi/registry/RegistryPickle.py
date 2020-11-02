from cloudmesh.common.Printer import Printer
from cloudmesh.common.Shell import Shell
from cloudmesh.mongo.CmDatabase import CmDatabase
# from cloudmesh.mongo.DataBaseDecorator import DatabaseUpdate
from cloudmesh.openapi.registry.DataBaseDecorator import DatabaseUpdate
from cloudmesh.openapi.registry.PickleDB import PickleDB


class RegistryPickle:
    """
      This class will help to register service into db.
      which later use to stop server.
    """
    kind = "register"

    collection = "local-registry"

    output = {
        "register": {
            "sort_keys": ["cm.name"],
            "order": ["cm.name",
                      "status",
                      "url",
                      "pid"],
            "header": ["Name",
                       "Status",
                       "Url",
                       "Pid"]
        }
    }

    def load(self, filename="~/.cloudmesh/openapi/registry.p"):
        """
        loads the registry content

        :param filename:
        :return:
        """
        self.data = PickleDB(filename=filename)

    def clean(self, filename="~/.cloudmesh/openapi/registry.p"):
        """
        erases the registry content form the file and keep the file.
        The data is empty.

        :param filename:
        :return:
        """
        return PickleDB(filename=filename).clean()

    # noinspection PyPep8Naming

    def Print(self, data, output=None):
        """
        print output in a structured format

        :param data:  input data to be printed out
        :param output:  type of structured output
        :return:  structured output
        """

        if output == "table":

            order = self.output[RegistryPickle.kind]['order']  # not pretty
            header = self.output[RegistryPickle.kind]['header']  # not pretty
            # humanize = self.output[kind]['humanize']  # not pretty

            print(Printer.flatwrite(data,
                                    sort_keys=["name"],
                                    order=order,
                                    header=header,
                                    output=output,
                                    # humanize=humanize
                                    )
                  )
        else:
            print(Printer.write(data, output=output))

    @DatabaseUpdate(provider="pickle")
    def add(self, name=None, **kwargs):
        """
        add to registry

        :param name: name to be used for registry entry
        :param kwargs:  other optional fields to populate in registry
        :return:
        """
        entry = {
            "cm": {
                "cloud": "local",
                "kind": "registry",
                "name": name,
                "driver": None
            },
            "name": name,
            "status": "defined"
        }

        for key in kwargs:
            entry[key] = kwargs[key]

        return entry

    def add_form_file(self, filename, **kwargs):
        """
        add to registry from file

        :param filename: file name including path
        :return:  entry to be inserted into Registry
        """

        spec = filename

        title = spec["info"]["title"]

        registry = RegistryPickle()
        entry = registry.add(name=title, **kwargs)

        return entry

    def delete(self, name=None):
        """
        delete item from registry

        :param name: name of the item in registry
        :return:
        """
        cm = PickleDB()  # repalce by pickle
        entries = cm.delete(name)
        cm.close_client()
        return entries

    def list(self, name=None):
        """
        list entries in the registry

        :param name:  name of registered server.  If not passed will list all registered servers.
        :return:  list of registered server(s)
        """
        cm = PickleDB()

        if name == None:
            entries = cm.find(cloud="local", kind="registry")
        else:
            entries = cm.find_name(name=name, kind="registry")

        return entries

    # TODO: determine if these are still needed as these functions are handled by cms already
    '''
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
    '''
