from cloudmesh.compute.vm.Provider import Provider
from flask import jsonify

#def list(cloud):
def list():
    cloud = "chameleon"
    provider = Provider(name=cloud)
    vms = provider.list()
    return jsonify(vms)
