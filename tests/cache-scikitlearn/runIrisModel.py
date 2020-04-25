from sklearn.datasets import load_iris
#from ..LogisticRegression import fit, set_params, predict
from sklearn.linear_model import LogisticRegression
import numpy

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


X = numpy.array([[5.1, 3.5, 1.4, 0.2], [5.9, 3.0, 5.1, 1.8]])
y = numpy.array([0, 2])
z = numpy.array([0.1, 0.2])
print(X)
print(y)
print(z)
print(type(X))
print(type(y))
print(type(z))
clf = LogisticRegression(random_state=0, max_iter=300).fit(X, y)


# X, y = load_iris(return_X_y=True)

"""
clf = fit(X, y)
make_pickle("irismodel", clf)
print("finished making pickle")
"""
# file = Path(r"C:\Users\Jonathan\.cloudmesh\server-cache\irismodel\irismodel.pickle")
"""
clf = load_pickle(file)
rows = int(sys.argv[1] or 6)
print(clf.predict(X[:rows, :]))
"""

# clf = LogisticRegression(random_state=0, max_iter=300).fit(X, y)
# y = "1234"
# x = list(y)
# Z = list(map(float, x))
# print(Z)
# print(type(Z))
# Z = numpy.array(Z)
# print(type(Z))
# Z = numpy.reshape(Z, (1, -1))
# print(clf.predict(Z))





