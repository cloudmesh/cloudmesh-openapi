# from tests.generator import LogisticRegression
# from sklearn.datasets import load_iris
# X, y = load_iris(return_X_y=True)
# fit = LogisticRegression.fit(X,y,None)
# print(LogisticRegression.predict(X[:2, :]))
# print(LogisticRegression.predict_proba(X[:2, :]))
# print(LogisticRegression.score(X,y,None))

# from tests.generator import LinearRegression
# from sklearn.datasets import load_iris
# X, y = load_iris(return_X_y=True)
# print(LinearRegression.fit(X,y,None))
# print(LinearRegression.predict(X[:2, :]))
# print(LinearRegression.score(X,y,None))

from tests.generator import RidgeClassifierCV as model
from sklearn.datasets import load_iris

X, y = load_iris(return_X_y=True)
print(X,y)
print(model.fit(X,y,None))
print(model.predict(X[:2, :]))
print(model.score(X,y,None))

