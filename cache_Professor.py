# sql (no)
# nosql
# redis
# pickle
# file
# apache qarquette
# cms mong db (

# ??? chose one of then
from cloudmesh.common.util import readfile

class ResultCache:

    def save(self, name, value, file=False, reader=readfile):
        # "key", value

        uuid = "ffff"
        key = uuid
        data = {
            "name": name,
            "uuid": uuid,
            "value": value,
            "file": "path"
        }
        return uuid


    def load(self, uuid):
        o = "o"
        # read that from whatever thing we stored it in

        return o

    def create(self):
        #
        return uuid



class LinearRegrassion(ResultCache):

    def __init__(self):
        pass
        # set up database connetion


    def fit(self, uuid, x, y, z):
        pass

