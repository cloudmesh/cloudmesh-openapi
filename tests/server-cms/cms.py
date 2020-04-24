from cloudmesh.compute.vm.Provider import Provider

flat = True
service = "chameleon"


#
# note when we get NOne back the service shoudl return
# ('', 204) # e.g. result not found this is handlesd in openapi
#

def test(service: str) -> dict:
    return {"test": "hello"}


def vm(service: str) -> list:
    """
    Lists the VMs on the cloud service

    :param service: The name of the service
    :return: the information in json format
    """
    provider = Provider(name=service)
    result = provider.list()
    if flat and result:
        result = provider.Prints(result,
                                 kind="vm",
                                 output="flat")

    return result


def flavor(service: str) -> list:
    """
    Lists the flavors on the cloud service

    :param service: The name of the service
    :return: the information in json format
    """
    provider = Provider(name=service)
    result = provider.flavors()
    if flat and result:
        result = provider.Prints(result, kind="vm", output="flat")
    return result


def image(service: str) -> list:
    """
    Lists the images on teh cloud service

    :param service: The name of the service
    :return: the information in json format
    """
    provider = Provider(name=service)
    result = provider.images()
    if flat and result:
        result = provider.Prints(result, kind="vm", output="flat")
    return result


def boot(service: str) -> list:
    """
    Boots a VM on the cloud service

    :param service: The name of the service
    :return: the information in json format
    """
    # TODO: needs more work, read from yaml file defaults
    provider = Provider(name=service)
    result = provider.create()
    if flat and result:
        result = provider.Prints(result, kind="vm", output="flat")
    return result


if __name__ == '__main__':
    #v = vm(service)
    #VERBOSE(v)
    #f = flavor(service)
    #VERBOSE(f)
    #i = image(service)
    #VERBOSE(i)
    result = boot(service)
    print(result)
    # v = vm("opensatck")
    # VERBOSE(v)
