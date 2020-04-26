from tests.generator import LogisticRegression
import numpy as np
from sklearn.datasets import load_iris
#X, y = load_iris(return_X_y=True)
X = [1,2,3,4,5,6,7,8]
y = [1,3,5,7]
y = np.array(y)
sample_weight = [1,1,1,1]
print(type(y))
#print(np.array(y))

fit = LogisticRegression.fit(X,y,sample_weight,4,2)
print(LogisticRegression.predict(X,4,2))#
print(LogisticRegression.decision_function(X,4,2))
print(LogisticRegression.predict_proba(X,4,2))
print(LogisticRegression.score(X,y,sample_weight,4,2))

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

