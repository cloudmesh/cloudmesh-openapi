from cloudmesh.configuration.Config import Config
from cloudmesh.common.console import Console
from cloudmesh.openapi.registry.RegistryMongoDB import RegistryMongoDB
from cloudmesh.openapi.registry.RegistryPickle import RegistryPickle


class Registry:
    """
      This class serves as a wrapper for either Registrypickle or RegistryMongoDatabase
    """

    kind = "registry"

    sample = """
    cloudmesh:
      cloud:
        {name}:
          cm:
            active: true
            heading: microservice registry
            host: TBD
            label: {name}
            kind: registry
            version: TBD
            service: registry
          default:
            kind: pickle
    """

    PROTOCOL_NAME = None
    RESGISTRY_CONFIG = "cloudmesh.registry.microservice.default.protocol"

    def __init__(self):
        """
        Choose which Registry protocol to use: mongo or pickle.
        Check config for configured protocol
        """
        if Registry.PROTOCOL_NAME is None:
            try:
                Registry.PROTOCOL_NAME = Config().get(Registry.RESGISTRY_CONFIG)
            except KeyError as e:
                Console.warning("No provider setting found in config")
                config = Config()
                config.set(Registry.RESGISTRY_CONFIG, "pickle")
                Registry.PROTOCOL_NAME = Config().get(Registry.RESGISTRY_CONFIG)

        if Registry.PROTOCOL_NAME == "mongo":
            self.protocol = RegistryMongoDB()
        elif Registry.PROTOCOL_NAME == "pickle":
            self.protocol = RegistryPickle()
        else:
            Console.error(f"Unsupported Registry Type {Registry.PROTOCOL_NAME}")
            raise ValueError(f"Unsupported Registry Type {Registry.PROTOCOL_NAME}")
        Console.ok(f"INIT: Using {Registry.PROTOCOL_NAME} Protocol")

    @classmethod
    def protocol(cls, protocol="pickle"):
        cls.PROTOCOL_NAME = protocol
        Config().set(cls.RESGISTRY_CONFIG, protocol)
        return cls.PROTOCOL_NAME

    # noinspection PyPep8Naming
    def Print(self, data, output=None):
        """
        print output in a structured format

        :param data:  input data to be printed out
        :param output:  type of structured output
        :return:  structured output
        """
        Console.ok(f"PRINT: Using {Registry.PROTOCOL_NAME} Protocol")
        self.protocol.Print(data, output)

    def add(self, name=None, **kwargs):
        """
        add to registry

        :param name: name to be used for registry entry
        :param kwargs:  other optional fields to populate in registry
        :return:  
        """
        Console.ok(f"ADD: Using {Registry.PROTOCOL_NAME} Protocol")
        return self.protocol.add(name, **kwargs)

    def add_form_file(self, filename, **kwargs):
        """
        add to registry from file

        :param filename: file name including path
        :return:  entry to be inserted into Registry
        """
        Console.ok(f"ADD FROM FILE: Using {Registry.PROTOCOL_NAME} Protocol")
        return self.protocol.add_form_file(filename, **kwargs)

    def delete(self, name=None):
        """
        delete item from registry

        :param name: name of the item in registry
        :return:  
        """
        Console.ok(f"DELETE: Using {Registry.PROTOCOL_NAME} Protocol")
        return self.protocol.delete(name)

    def list(self, name=None):
        """
        list entries in the registry

        :param name:  name of registered server.  If not passed will list all registered servers.
        :return:  list of registered server(s)
        """
        Console.ok(f"LIST: Using {Registry.PROTOCOL_NAME} Protocol")
        return self.protocol.list(name)

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
