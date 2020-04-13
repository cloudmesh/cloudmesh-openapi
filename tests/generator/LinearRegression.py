
from sklearn.linear_model import LinearRegression
import array


def fit(X: array, y: array, sample_weight: array):

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

    fit = LinearRegression().fit(X, y, sample_weight)


    return fit


def get_params(deep: bool) -> str:

    """
    Get parameters for this estimator.


    :param deep: If True, will return the parameters for this estimator and
                    contained subobjects that are estimators.
    :type deep: bool
    :param return: Parameter names mapped to their values.
    :type return: str
    
    """

    str = get_params(deep)


    return str


def predict(X: array) -> array:

    """
    Predict using the linear model.


    :param X: Samples.
    :type X: array
    :param return: Returns predicted values.
    :type return: array
    
    """

    array = predict(X)


    return array


def score(X: array) -> float:

    """
    Return the coefficient of determination R^2 of the prediction.


    :param X:     Test samples. For some estimators this may be a
                        precomputed kernel matrix or a list of generic objects instead,
                        shape = (n_samples, n_samples_fitted),
                        where n_samples_fitted is the number of
                        samples used in the fitting for the estimator.
                    
                    y : array-like of shape (n_samples,) or (n_samples, n_outputs)
                        True values for X.
                    
                    sample_weight : array-like of shape (n_samples,), default=None
                        Sample weights.
    :type X: array
    :param return: R^2 of self.predict(X) wrt. y.
    :type return: float
    
    """

    float = score(X)


    return float


def set_params(**params: dict):

    """
    Set the parameters of this estimator.


    :param **params: Estimator parameters.
    :type **params: dict
    :param return: Estimator instance.
    :type return: self
    
    """

    set_params = set_params(**params)


    return set_params
