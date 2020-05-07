from tests.generator import LinearRegression
import numpy as np
from sklearn.datasets import load_iris
#X, y = load_iris(return_X_y=True)
X = "X.csv"
y = "y.csv"

sample_weight = "sample_weight.csv"
#print(np.array(y))

fit = LinearRegression.fit(X,y)
print(LinearRegression.predict(X))
# print(LogisticRegression.decision_function(X,4,2))
#print(LinearRegression.predict_proba(X,4,2))
print(LinearRegression.score(X,y))

# from tests.generator import LinearRegression
# from sklearn.datasets import load_iris
# X, y = load_iris(return_X_y=True)
# print(LinearRegression.fit(X,y,None))
# print(LinearRegression.predict(X[:2, :]))
# print(LinearRegression.score(X,y,None))

# from tests.generator import RidgeClassifierCV as model
# from sklearn.datasets import load_iris
#
# X, y = load_iris(return_X_y=True)
# #print(X,y)
# print(model.fit(X,y,None))
# print(model.predict(X[:2, :]))
# print(model.score(X,y,None))

