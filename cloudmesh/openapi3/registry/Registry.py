from cloudmesh.mongo.DataBaseDecorator import DatabaseUpdate

class Registry:

    def _init__(self, url):
        self.url = url

    @DatabaseUpdate()
    def generate_entry(self, name=None):
        entry = {
            "cm": {
                "cloud": "local",
                "kind": "registry",
                "name": name,
                "dirver": None
            },
            "url": self.url,
            "name": name
        }
        return entry
