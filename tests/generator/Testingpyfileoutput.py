from tests.generator import LogisticRegression
import numpy as np

X = np.array([[1, 1], [1, 2], [2, 2], [2, 3]])
y = np.dot(X, np.array([1, 2])) + 3
estimator = LogisticRegression.set_params(penalty='l1',solver='saga')
fit = estimator.fit(X,y,None)
score = fit.score(X,y)

print(score,fit)




