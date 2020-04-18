from sklearn.datasets import load_iris
from ..LogisticRegression import fit, set_params, predict
import pickle
import sys
from pathlib import Path


# Saves the "data" with the "title" and adds the .pickle
def make_pickle(title, data):
    pikd = open(title + ".pickle", "wb")
    pickle.dump(data, pikd)
    pikd.close()


# loads and returns a pickled objects
def load_pickle(file):
    pikd = open(file, "rb")
    data = pickle.load(pikd)
    pikd.close()
    return data


X, y = load_iris(return_X_y=True)
# print(X)
'''
clf = fit(X, y)
make_pickle("irismodel", clf)
print("finished making pickle")
'''
file = Path(r"C:\Users\Jonathan\.cloudmesh\server-cache\irismodel\irismodel.pickle")

clf = load_pickle(file)
rows = int(sys.argv[1] or 6)
print(clf.predict(X[:rows, :]))

