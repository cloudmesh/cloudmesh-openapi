
from sklearn.linear_model import LogisticRegression
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

    model = ResultCache().load("LogisticRegression")
    array = model.decision_function(X)



    return array


def densify():

    """
    Convert coefficient matrix to dense array format.


    :param return: Fitted estimator.
    :type return: self
    
    """

    densify = densify()



    return densify


def fit(X: str, y: array, sample_weight: array):

    """
    Fit the model according to the given training data.


    :param X: Training vector, where n_samples is the number of samples and
                    n_features is the number of features.
    :type X: str
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

    fit = LogisticRegression().fit(X, y, sample_weight)
    ResultCache().save("LogisticRegression","pickle",fit)


    return LogisticRegression


def get_params(deep: bool) -> str:

    """
    Get parameters for this estimator.


    :param deep: If True, will return the parameters for this estimator and
                    contained subobjects that are estimators.
    :type deep: bool
    :param return: Parameter names mapped to their values.
    :type return: str
    
    """

    model = ResultCache().load("LogisticRegression")
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

    model = ResultCache().load("LogisticRegression")
    array = model.predict(X)



    return array


def predict_log_proba(X: array) -> array:

    """
    Predict logarithm of probability estimates.


    :param X: Vector to be scored, where `n_samples` is the number of samples and
                    `n_features` is the number of features.
    :type X: array
    :param return: Returns the log-probability of the sample for each class in the
                    model, where classes are ordered as they are in ``self.classes_``.
    :type return: array
    
    """

    model = ResultCache().load("LogisticRegression")
    array = model.predict_log_proba(X)



    return array


def predict_proba(X: array) -> array:

    """
    Probability estimates.


    :param X: Vector to be scored, where `n_samples` is the number of samples and
                    `n_features` is the number of features.
    :type X: array
    :param return: Returns the probability of the sample for each class in the model,
                    where classes are ordered as they are in ``self.classes_``.
    :type return: array
    
    """

    model = ResultCache().load("LogisticRegression")
    array = model.predict_proba(X)



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

    model = ResultCache().load("LogisticRegression")
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
    ResultCache().save("LogisticRegression","pickle",set_params)


    return LogisticRegression


def sparsify():

    """
    Convert coefficient matrix to sparse format.


    :param return: Fitted estimator.
    :type return: self
    
    """

    sparsify = sparsify()



    return sparsify
