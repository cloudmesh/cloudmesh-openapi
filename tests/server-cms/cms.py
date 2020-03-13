from cloudmesh.compute.vm.Provider import Provider
from flask import jsonify
from pprint import pprint

#def list(cloud):
def vms():
    cloud = "chameleon"
    provider = Provider(name=cloud)
    vms = provider.list()
    pprint(vms)
    return jsonify(vms)
