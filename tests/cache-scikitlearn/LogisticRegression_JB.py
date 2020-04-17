
from sklearn.linear_model import LogisticRegression
import array

from sklearn.linear_model import LogisticRegression
import array


def _decision_function(X: array) -> array:

    """
    Predict confidence scores for samples.


    :param X: Samples.
    :type X: array
    :param return: Confidence scores per (sample, class) combination. In the binary
                    case, confidence score for self.classes_[1] where >0 means this
                    class would be predicted.
    :type return: array
    
    """

    array = decision_function(X)


    return array


def _densify():

    """
    Convert coefficient matrix to dense array format.


    :param return: Fitted estimator.
    :type return: self
    
    """

    densify = densify()


    return densify


def _fit(X: array, y: array, sample_weight: array = None):

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

    fit = LogisticRegression().fit(X, y, sample_weight or None)


    return fit


def _get_params(deep: bool) -> str:

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


def _predict(X: array) -> array:

    """
    Predict class labels for samples in X.


    :param X: Samples.
    :type X: array
    :param return: Predicted class label per sample.
    :type return: array
    
    """

    array = predict(X)


    return array


def _predict_log_proba(X: array) -> array:

    """
    Predict logarithm of probability estimates.


    :param X: Vector to be scored, where `n_samples` is the number of samples and
                    `n_features` is the number of features.
    :type X: array
    :param return: Returns the log-probability of the sample for each class in the
                    model, where classes are ordered as they are in ``self.classes_``.
    :type return: array
    
    """

    array = predict_log_proba(X)


    return array


def _predict_proba(X: array) -> array:

    """
    Probability estimates.


    :param X: Vector to be scored, where `n_samples` is the number of samples and
                    `n_features` is the number of features.
    :type X: array
    :param return: Returns the probability of the sample for each class in the model,
                    where classes are ordered as they are in ``self.classes_``.
    :type return: array
    
    """

    array = predict_proba(X)


    return array


def _score(X: array, y: array, sample_weight: array) -> float:

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

    float = score(X, y, sample_weight)


    return float


def _set_params(**params: dict):

    """
    Set the parameters of this estimator.


    :param **params: Estimator parameters.
    :type **params: dict
    :param return: Estimator instance.
    :type return: self
    
    """

    set_params = LogisticRegression().set_params(**params)


    return set_params


def _sparsify():

    """
    Convert coefficient matrix to sparse format.


    :param return: Fitted estimator.
    :type return: self
    
    """

    sparsify = sparsify()


    return sparsify


# Saves the "data" with the "title" and adds the .pickle
def make_pickle(title, data):
    pikd = open(title + ".pickle", "wb")
    pickle.dump(data, pikd)
    pikd.close()


# loads and returns a pickled objects
def load_pickle(file):
    pikd = open(file, "rb")
    data = pickle.load(pikd)
    pikd.close()
    return data


if __name__ == "__main__":
    from sklearn.datasets import load_iris
    from pathlib import Path
    import pickle

    X, y = load_iris(return_X_y=True)
    '''   
    clf = _fit(X, y)
    make_pickle("irismodel", clf)
    print("finished making pickle")
    '''

    file = Path(r"C:\Users\Jonathan\.cloudmesh\server-cache\irismodel\irismodel.pickle")
    clf = load_pickle(file)
    print(clf.predict(X[:, :]))

    """
    # from sklearn.linear_model import LogisticRegression
    X, y = load_iris(return_X_y=True)
    # print(X)
    clf = LogisticRegression(random_state=0, max_iter=300).fit(X, y)
    make_pickle("irismodel", clf)
    print("finished making pickle")

    
    print(clf.predict(X[:, :]))
    clf.predict_proba(X[:2, :])
    clf.score(X, y)
    """
