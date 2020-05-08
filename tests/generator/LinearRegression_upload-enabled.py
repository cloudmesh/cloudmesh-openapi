
from sklearn.linear_model import LinearRegression
import numpy as np
import pandas as pd
import array
from cloudmesh.openapi.registry.cache import ResultCache
from cloudmesh.openapi.registry.fileoperation import FileOperation


def fit(X: str, y: str):

    """
    Fit linear model.


    :param X: Training data
    :type X: array
    :param y: Target values. Will be cast to X's dtype if necessary
    :type y: array
    :param sample_weight: Individual weights for each sample
                    
                    .. versionadded:: 0.17
                       parameter *sample_weight* support to LinearRegression.
    :type sample_weight: array
    :param return: 
    :type return: self
    
    """

    X_input = "~/.cloudmesh/upload-file/" + f"{X}" + ".csv"
    y_input = "~/.cloudmesh/upload-file/" + f"{y}" + ".csv"
    X = pd.read_csv(X_input)
    y = pd.read_csv(y_input)
    fit = LinearRegression().fit(X, y)
    ResultCache().save("Linregnew","pickle",fit)


    return 


def get_params(deep: bool) -> str:

    """
    Get parameters for this estimator.


    :param deep: If True, will return the parameters for this estimator and
                    contained subobjects that are estimators.
    :type deep: bool
    :param return: Parameter names mapped to their values.
    :type return: str
    
    """

    model = ResultCache().load("Linregnew")
    str = model.get_params(deep)


    return str


def predict(X: str) -> list:

    """
    Predict using the linear model.


    :param X: Samples.
    :type X: array
    :param return: Returns predicted values.
    :type return: array
    
    """

    X_input = "~/.cloudmesh/upload-file/" + f"{X}" + ".csv"
    X = pd.read_csv(X_input)
    model = ResultCache().load("Linregnew")
    list = model.predict(X)
    list = list.tolist()


    return list


def score(X: str, y: str) -> float:

    """
    Return the coefficient of determination R^2 of the prediction.


    :param X: Test samples. For some estimators this may be a
                    precomputed kernel matrix or a list of generic objects instead,
                    shape = (n_samples, n_samples_fitted),
                    where n_samples_fitted is the number of
                    samples used in the fitting for the estimator.
    :type X: array
    :param y: True values for X.
    :type y: array
    :param sample_weight: Sample weights.
    :type sample_weight: array
    :param return: R^2 of self.predict(X) wrt. y.
    :type return: float
    
    """

    X_input = "~/.cloudmesh/upload-file/" + f"{X}" + ".csv"
    y_input = "~/.cloudmesh/upload-file/" + f"{y}" + ".csv"
    X = pd.read_csv(X_input)
    y = pd.read_csv(y_input)
    model = ResultCache().load("Linregnew")
    float = model.score(X, y)


    return float


def set_params(**params: dict):

    """
    Set the parameters of this estimator.


    :param **params: Estimator parameters.
    :type **params: dict
    :param return: Estimator instance.
    :type return: self
    
    """

    set_params = LinearRegression().set_params(**params)
    ResultCache().save("Linregnew","pickle",set_params)


    return


from cloudmesh.openapi.registry.fileoperation import FileOperation

def upload() -> str:
    filename=FileOperation().file_upload()
    return filename

#### upload functionality added
