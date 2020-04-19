
from sklearn.linear_model import RidgeClassifier
import array
from cloudmesh.openapi.registry.cache import ResultCache


def decision_function(X: array) -> array:

    """
    Predict confidence scores for samples.


    :param X: Samples.
    :type X: array
    :param return: Confidence scores per (sample, class) combination. In the binary
                    case, confidence score for self.classes_[1] where >0 means this
                    class would be predicted.
    :type return: array
    
    """

    model = ResultCache().load("RidgeClassifier")
    array = model.decision_function(X)



    return array


def fit(X: array, y: array, sample_weight: array):

    """
    Fit Ridge classifier model.


    :param X: Training data.
    :type X: array
    :param y: Target values.
    :type y: array
    :param sample_weight: Individual weights for each sample. If given a float, every sample
                    will have the same weight.
                    
                    .. versionadded:: 0.17
                       *sample_weight* support to Classifier.
    :type sample_weight: array
    :param return: Instance of the estimator.
    :type return: self
    
    """

    fit = RidgeClassifier().fit(X, y, sample_weight)
    ResultCache().save("RidgeClassifier","pickle",fit)


    return RidgeClassifier


def get_params(deep: bool) -> str:

    """
    Get parameters for this estimator.


    :param deep: If True, will return the parameters for this estimator and
                    contained subobjects that are estimators.
    :type deep: bool
    :param return: Parameter names mapped to their values.
    :type return: str
    
    """

    model = ResultCache().load("RidgeClassifier")
    str = model.get_params(deep)



    return str


def predict(X: array) -> array:

    """
    Predict class labels for samples in X.


    :param X: Samples.
    :type X: array
    :param return: Predicted class label per sample.
    :type return: array
    
    """

    model = ResultCache().load("RidgeClassifier")
    array = model.predict(X)



    return array


def score(X: array, y: array, sample_weight: array) -> float:

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

    model = ResultCache().load("RidgeClassifier")
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

    set_params = RidgeClassifier().set_params(**params)
    ResultCache().save("RidgeClassifier","pickle",set_params)


    return RidgeClassifier
