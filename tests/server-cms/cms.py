from cloudmesh.compute.vm.Provider import Provider
from flask import jsonify
from pprint import pprint
from cloudmesh.common.Printer import Printer

def vms():
    cloud = "chameleon"
    provider = Provider(name=cloud)
    vms = provider.list()
    pprint(vms)
    h = provider.Print(vms, kind="vm", output="html")
    return h
