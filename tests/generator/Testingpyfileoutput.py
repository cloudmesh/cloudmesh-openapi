from tests.generator import LogisticRegression
from sklearn.datasets import load_iris
import numpy as np
X, y = load_iris(return_X_y=True)
#X = np.array([[1, 1], [1, 2], [2, 2], [2, 3]])
#y = np.dot(X, np.array([1, 2])) + 3
estimator = LogisticRegression.set_params(random_state =0)
print(estimator.get_params)
fit = estimator.fit(X,y,None)
print(fit.predict(X[:2, :]))
print(fit.predict_proba(X[:2, :]))
score = fit.score(X,y)
print(score)
print(fit)




