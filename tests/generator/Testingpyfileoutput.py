from tests.generator import LinearRegression
import numpy as np

X = np.array([[1, 1], [1, 2], [2, 2], [2, 3]])
y = np.dot(X, np.array([1, 2])) + 3

test = LinearRegression.fit(X,y,None)
score = test.score(X,y)

print(score,test.intercept_)




