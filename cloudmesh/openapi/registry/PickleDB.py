import os
import pickle
from cloudmesh.common.util import path_expand
from cloudmesh.common.console import Console


class PickleDB:
    def __init__(self, filename="~/.cloudmesh/openapi/registry.p"):
        expanded_filename = path_expand(filename)
        os.makedirs(os.path.dirname(expanded_filename), exist_ok=True)
        self.DB_PATH = expanded_filename

        # Attempt to load from pkl
        try:
            self.db = pickle.load(open(expanded_filename, "rb"))
        except FileNotFoundError as e:
            self.db = {}

    def update(self, entries):
        result = []
        for entry in entries:
            if "name" not in entry:
                raise KeyError(
                    f"No name given for DB entry: {entry}")
            self.db[entry['name']] = entry
            result += [entry]
        return result

    def close_client(self):
        """
        Updated DB upon closing client
        """
        try:
            pickle.dump(self.db, open(self.DB_PATH, "wb"))
            return 0
        except Exception as e:
            Console.error(f"Error writing to PickleDB: {e}")
            return -1

    def clean(self):
        """
        Clear DB entries
        """
        try:
            pickle.dump({}, open(self.DB_PATH, "wb"))
            self.db = {}
            return 0
        except:
            Console.error(f"Error clearing PickleDB at {self.DB_PATH}")
            return -1

    def delete(self, name):
        try:
            entry = self.db[name]
            del self.db[name]
            return [entry]
        except KeyError as e:
            Console.error(
                f"KeyError: Could not delete {name} from db. Skipping")

    def find(self, cloud, kind=None):
        entries = []
        for entry in self.db:
            try:
                if self.db[entry]["cm"]["cloud"] == cloud and self.db[entry]["cm"]["kind"] == kind:
                    entries += [self.db[entry]]
            except KeyError as e:
                Console.error(f"KeyError in PickleDB.find() Skipping: {e}")
        return entries

    def find_name(self, name, kind=None):
        entries = []
        try:
            if self.db[name]["cm"]["kind"] == kind:
                entries += [self.db[name]]
        except KeyError as e:
            Console.error(f"KeyError. Skipping: {e}")
        return entries
