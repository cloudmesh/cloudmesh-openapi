
from sklearn.linear_model import LogisticRegression
import numpy as np
import array
from cloudmesh.openapi.registry.cache import ResultCache


def decision_function(X: list, X_shape_x: int, X_shape_y: int) -> list:

    """
    Predict confidence scores for samples.


    :param X: Samples.
    :type X: array
    :param return: Confidence scores per (sample, class) combination. In the binary
                    case, confidence score for self.classes_[1] where >0 means this
                    class would be predicted.
    :type return: array
    
    """

    X = np.array(X).reshape(X_shape_x,X_shape_y)
    model = ResultCache().load("JagsLogis1")
    list = model.decision_function(X)
    list = list.tolist()


    return list


def densify():

    """
    Convert coefficient matrix to dense array format.


    :param return: Fitted estimator.
    :type return: self
    
    """

    densify = LogisticRegression().densify()
    ResultCache().save("JagsLogis1","pickle",densify)



    return


def fit(X: list, y: list, sample_weight: list, X_shape_x: int, X_shape_y: int):

    """
    Fit the model according to the given training data.


    :param X: Training vector, where n_samples is the number of samples and
                    n_features is the number of features.
    :type X: array
    :param y: Target vector relative to X.
    :type y: array
    :param sample_weight: Array of weights that are assigned to individual samples.
                    If not provided, then each sample is given unit weight.
                    
                    .. versionadded:: 0.17
                       *sample_weight* support to LogisticRegression.
    :type sample_weight: array
    :param return: Fitted estimator.
    :type return: self
    
    """

    X = np.array(X).reshape(X_shape_x,X_shape_y)
    fit = LogisticRegression().fit(X, y, sample_weight)
    ResultCache().save("JagsLogis1","pickle",fit)


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

    model = ResultCache().load("JagsLogis1")
    str = model.get_params(deep)


    return str


def predict(X: list, X_shape_x: int, X_shape_y: int) -> list:

    """
    Predict class labels for samples in X.


    :param X: Samples.
    :type X: array
    :param return: Predicted class label per sample.
    :type return: array
    
    """

    X = np.array(X).reshape(X_shape_x,X_shape_y)
    model = ResultCache().load("JagsLogis1")
    list = model.predict(X)
    list = list.tolist()


    return list


def predict_log_proba(X: list, X_shape_x: int, X_shape_y: int) -> list:

    """
    Predict logarithm of probability estimates.


    :param X: Vector to be scored, where `n_samples` is the number of samples and
                    `n_features` is the number of features.
    :type X: array
    :param return: Returns the log-probability of the sample for each class in the
                    model, where classes are ordered as they are in ``self.classes_``.
    :type return: array
    
    """

    X = np.array(X).reshape(X_shape_x,X_shape_y)
    model = ResultCache().load("JagsLogis1")
    list = model.predict_log_proba(X)
    list = list.tolist()


    return list


def predict_proba(X: list, X_shape_x: int, X_shape_y: int) -> list:

    """
    Probability estimates.


    :param X: Vector to be scored, where `n_samples` is the number of samples and
                    `n_features` is the number of features.
    :type X: array
    :param return: Returns the probability of the sample for each class in the model,
                    where classes are ordered as they are in ``self.classes_``.
    :type return: array
    
    """

    X = np.array(X).reshape(X_shape_x,X_shape_y)
    model = ResultCache().load("JagsLogis1")
    list = model.predict_proba(X)
    list = list.tolist()


    return list


def score(X: list, y: list, sample_weight: list, X_shape_x: int, X_shape_y: int) -> float:

    """
    Return the mean accuracy on the given test data and labels.


    :param X: Test samples.
    :type X: array
    :param y: True labels for X.
    :type y: array
    :param sample_weight: Sample weights.
    :type sample_weight: array
    :param return: Mean accuracy of self.predict(X) wrt. y.
    :type return: float
    
    """

    X = np.array(X).reshape(X_shape_x,X_shape_y)
    model = ResultCache().load("JagsLogis1")
    float = model.score(X, y, sample_weight)


    return float


def set_params(**params: dict):

    """
    Set the parameters of this estimator.


    :param **params: Estimator parameters.
    :type **params: dict
    :param return: Estimator instance.
    :type return: self
    
    """

    set_params = LogisticRegression().set_params(**params)
    ResultCache().save("JagsLogis1","pickle",set_params)


    return


def sparsify():

    """
    Convert coefficient matrix to sparse format.


    :param return: Fitted estimator.
    :type return: self
    
    """

    sparsify = LogisticRegression().sparsify()
    ResultCache().save("JagsLogis1","pickle",sparsify)



    return
