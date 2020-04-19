from cloudmesh.mongo.CmDatabase import CmDatabase
from cloudmesh.mongo.DataBaseDecorator import DatabaseUpdate
from pathlib import Path
from cloudmesh.common.util import path_expand
import pickle


class ResultCache:

    def __init__(self):
        pass

    @DatabaseUpdate()
    def save(self, modelname=None, type="pickle", modelobject=None, **kwargs):
        """
        Save model to cache

        :param modelname:
        :param type:
        :param modelobject:
        :param kwargs:
        :return:
        """

        # create local cache directory
        cache_path = f"~/.cloudmesh/server-cache/{modelname}/"
        p = Path(path_expand(cache_path))
        p.mkdir(parents=True, exist_ok=True)

        # serialize model and save to local cache directory
        cached_file = ""
        if type == "pickle":
            cached_file = self._make_pickle(modelname, modelobject, str(p.absolute()))
        else:
            print("Unsupported serialization type provided")

        # update db cache with below details
        entry = {
            "cm": {
                "cloud": "local",
                "kind": "cache",
                "name": modelname,
                "driver": None
            },
            "name": modelname,
            "status": "cached",
            "cached_file": cached_file
        }

        for key in kwargs:
            entry[key] = kwargs[key]

        return entry

    def load(self, name):
        """
        Load cached model

        :param name:
        :return:
        """

        cm = CmDatabase()
        test = cm.find(cloud="local", kind="cache", query={"name": {'$regex': f"{name}"}})
        cached_file = test[0]['cached_file']
        print(f"Loading serialized model: {cached_file}")
        unserialized_model = self._load_pickle(cached_file)


        return unserialized_model

    def _make_pickle(self, title, data, path):
        """
        Serializes a model and returns the fully qualified path and file name to pickle file

        :param title:
        :param data:
        :param path:
        :return:
        """

        file = Path(f"{path}/{title}.pickle")
        pikd = open(file, "wb")
        pickle.dump(data, pikd)
        pikd.close()

        return str(file)

    # loads and returns a pickled object
    def _load_pickle(self, file):
        """
        Loads a pickle file and returns object

        :param file:
        :return:
        """

        pikd = open(file, "rb")
        data = pickle.load(pikd)
        pikd.close()
        return data


if __name__ == "__main__":

    from sklearn.linear_model import LogisticRegression
    from sklearn.datasets import load_iris

    newcache = ResultCache()

    X, y = load_iris(return_X_y=True)
    # print(X)
    clf = LogisticRegression(random_state=0, max_iter=300).fit(X, y)
    print(newcache.save("irismodel1", "pickle", clf))
    print("finished caching model")
    model = newcache.load("irismodel1")
    print(model.predict_proba(X[:2, :]))
