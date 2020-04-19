
from sklearn.linear_model import RidgeClassifierCV
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

    model = ResultCache().load("RidgeClassifierCV")
    array = model.decision_function(X)



    return array


def fit(X: array, y: array, sample_weight: array):

    """
    Fit Ridge classifier with cv.


    :param X: Training vectors, where n_samples is the number of samples
                    and n_features is the number of features. When using GCV,
                    will be cast to float64 if necessary.
    :type X: array
    :param y: Target values. Will be cast to X's dtype if necessary.
    :type y: array
    :param sample_weight: Individual weights for each sample. If given a float, every sample
                    will have the same weight.
    :type sample_weight: array
    :param return: 
    :type return: self
    
    """

    fit = RidgeClassifierCV().fit(X, y, sample_weight)
    ResultCache().save("RidgeClassifierCV","pickle",fit)


    return RidgeClassifierCV


def get_params(deep: bool) -> str:

    """
    Get parameters for this estimator.


    :param deep: If True, will return the parameters for this estimator and
                    contained subobjects that are estimators.
    :type deep: bool
    :param return: Parameter names mapped to their values.
    :type return: str
    
    """

    model = ResultCache().load("RidgeClassifierCV")
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

    model = ResultCache().load("RidgeClassifierCV")
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

    model = ResultCache().load("RidgeClassifierCV")
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

    set_params = RidgeClassifierCV().set_params(**params)
    ResultCache().save("RidgeClassifierCV","pickle",set_params)


    return RidgeClassifierCV
