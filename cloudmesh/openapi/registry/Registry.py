# from cloudmesh.common.Printer import Printer
# from cloudmesh.common.Shell import Shell
# from cloudmesh.mongo.CmDatabase import CmDatabase
# from cloudmesh.mongo.DataBaseDecorator import DatabaseUpdate
from cloudmesh.common.console import Console
from cloudmesh.openapi.registry.RegistryMongoDB import RegistryMongoDB
from cloudmesh.openapi.registry.RegistryPickle import RegistryPickle



class Registry:
    """
      This class serves as a wrapper for either Registrypickle or RegistryMongoDatabase
    """
    TYPE = None

    def __init__(self):
        if Registry.TYPE == "mongo":
            self.provider = RegistryMongoDB()
        elif Registry.TYPE == "pickle":
            self.provider = RegistryPickle()
        else:
            Console.error(f"Unsupported Registry Type {Registry.TYPE}")
            raise ValueError(f"Unsupported Registry Type {Registry.TYPE}")

    # noinspection PyPep8Naming
    def Print(self, data, output=None):
        """
        print output in a structured format

        :param data:  input data to be printed out
        :param output:  type of structured output
        :return:  structured output
        """
        self.provider.Print(data, output)

    def add(self, name=None, **kwargs):
        """
        add to registry

        :param name: name to be used for registry entry
        :param kwargs:  other optional fields to populate in registry
        :return:  
        """
        return self.provider.add(name, **kwargs)

    def add_form_file(self, filename, **kwargs):
        """
        add to registry from file

        :param filename: file name including path
        :return:  entry to be inserted into Registry
        """
        return self.provider.add_form_file(filename, **kwargs)

    def delete(self, name=None):
        """
        delete item from registry

        :param name: name of the item in registry
        :return:  
        """
        return self.provider.delete(name)

    def list(self, name=None):
        """
        list entries in the registry

        :param name:  name of registered server.  If not passed will list all registered servers.
        :return:  list of registered server(s)
        """

        return self.provider.list(name)

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
