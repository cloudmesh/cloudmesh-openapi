from tests.generator import LogisticRegression
from sklearn.datasets import load_iris
import numpy as np
X, y = load_iris(return_X_y=True)
#print(LogisticRegression.fit(X,y,None))
fit =LogisticRegression.fit(X,y,None)
print("fit",fit)
print(fit.predict(X[:2, :]))
print(fit.predict_proba(X[:2, :]))
score = fit.score(X,y)
print(score)




