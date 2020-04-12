
from sklearn.linearmodel import LogisticRegression
import array

def LogisticRegression(penalty: str, dual: bool, tol: float, C: float, fit_intercept: bool, intercept_scaling: float, class_weight: dict, random_state: int, solver: str, max_iter: int, multi_class: str, verbose: int, warm_start: bool, n_jobs: int, l1_ratio: float):

    """
    Logistic Regression (aka logit, MaxEnt) classifier.


    :param penalty: Used to specify the norm used in the penalization. The 'newton-cg',
                    'sag' and 'lbfgs' solvers support only l2 penalties. 'elasticnet' is
                    only supported by the 'saga' solver. If 'none' (not supported by the
                    liblinear solver), no regularization is applied.
                    
                    .. versionadded:: 0.19
                       l1 penalty with SAGA solver (allowing 'multinomial' + L1)
    :type penalty: str
    :param dual: Dual or primal formulation. Dual formulation is only implemented for
                    l2 penalty with liblinear solver. Prefer dual=False when
                    n_samples > n_features.
    :type dual: bool
    :param tol: Tolerance for stopping criteria.
    :type tol: float
    :param C: Inverse of regularization strength; must be a positive float.
                    Like in support vector machines, smaller values specify stronger
                    regularization.
    :type C: float
    :param fit_intercept: Specifies if a constant (a.k.a. bias or intercept) should be
                    added to the decision function.
    :type fit_intercept: bool
    :param intercept_scaling: Useful only when the solver 'liblinear' is used
                    and self.fit_intercept is set to True. In this case, x becomes
                    [x, self.intercept_scaling],
                    i.e. a "synthetic" feature with constant value equal to
                    intercept_scaling is appended to the instance vector.
                    The intercept becomes ``intercept_scaling * synthetic_feature_weight``.
                    
                    Note! the synthetic feature weight is subject to l1/l2 regularization
                    as all other features.
                    To lessen the effect of regularization on synthetic feature weight
                    (and therefore on the intercept) intercept_scaling has to be increased.
    :type intercept_scaling: float
    :param class_weight: Weights associated with classes in the form ``{class_label: weight}``.
                    If not given, all classes are supposed to have weight one.
                    
                    The "balanced" mode uses the values of y to automatically adjust
                    weights inversely proportional to class frequencies in the input data
                    as ``n_samples / (n_classes * np.bincount(y))``.
                    
                    Note that these weights will be multiplied with sample_weight (passed
                    through the fit method) if sample_weight is specified.
                    
                    .. versionadded:: 0.17
                       *class_weight='balanced'*
    :type class_weight: dict
    :param random_state: The seed of the pseudo random number generator to use when shuffling
                    the data.  If int, random_state is the seed used by the random number
                    generator; If RandomState instance, random_state is the random number
                    generator; If None, the random number generator is the RandomState
                    instance used by `np.random`. Used when ``solver`` == 'sag' or
                    'liblinear'.
    :type random_state: int
    :param solver: Algorithm to use in the optimization problem.
                    
                    - For small datasets, 'liblinear' is a good choice, whereas 'sag' and
                      'saga' are faster for large ones.
                    - For multiclass problems, only 'newton-cg', 'sag', 'saga' and 'lbfgs'
                      handle multinomial loss; 'liblinear' is limited to one-versus-rest
                      schemes.
                    - 'newton-cg', 'lbfgs', 'sag' and 'saga' handle L2 or no penalty
                    - 'liblinear' and 'saga' also handle L1 penalty
                    - 'saga' also supports 'elasticnet' penalty
                    - 'liblinear' does not support setting ``penalty='none'``
                    
                    Note that 'sag' and 'saga' fast convergence is only guaranteed on
                    features with approximately the same scale. You can
                    preprocess the data with a scaler from sklearn.preprocessing.
                    
                    .. versionadded:: 0.17
                       Stochastic Average Gradient descent solver.
                    .. versionadded:: 0.19
                       SAGA solver.
                    .. versionchanged:: 0.22
                        The default solver changed from 'liblinear' to 'lbfgs' in 0.22.
    :type solver: str
    :param max_iter: Maximum number of iterations taken for the solvers to converge.
    :type max_iter: int
    :param multi_class: If the option chosen is 'ovr', then a binary problem is fit for each
                    label. For 'multinomial' the loss minimised is the multinomial loss fit
                    across the entire probability distribution, *even when the data is
                    binary*. 'multinomial' is unavailable when solver='liblinear'.
                    'auto' selects 'ovr' if the data is binary, or if solver='liblinear',
                    and otherwise selects 'multinomial'.
                    
                    .. versionadded:: 0.18
                       Stochastic Average Gradient descent solver for 'multinomial' case.
                    .. versionchanged:: 0.22
                        Default changed from 'ovr' to 'auto' in 0.22.
    :type multi_class: str
    :param verbose: For the liblinear and lbfgs solvers set verbose to any positive
                    number for verbosity.
    :type verbose: int
    :param warm_start: When set to True, reuse the solution of the previous call to fit as
                    initialization, otherwise, just erase the previous solution.
                    Useless for liblinear solver. See :term:`the Glossary <warm_start>`.
                    
                    .. versionadded:: 0.17
                       *warm_start* to support *lbfgs*, *newton-cg*, *sag*, *saga* solvers.
    :type warm_start: bool
    :param n_jobs: Number of CPU cores used when parallelizing over classes if
                    multi_class='ovr'". This parameter is ignored when the ``solver`` is
                    set to 'liblinear' regardless of whether 'multi_class' is specified or
                    not. ``None`` means 1 unless in a :obj:`joblib.parallel_backend`
                    context. ``-1`` means using all processors.
                    See :term:`Glossary <n_jobs>` for more details.
    :type n_jobs: int
    :param l1_ratio: The Elastic-Net mixing parameter, with ``0 <= l1_ratio <= 1``. Only
                    used if ``penalty='elasticnet'`. Setting ``l1_ratio=0`` is equivalent
                    to using ``penalty='l2'``, while setting ``l1_ratio=1`` is equivalent
                    to using ``penalty='l1'``. For ``0 < l1_ratio <1``, the penalty is a
                    combination of L1 and L2.
    :type l1_ratio: float
    :param return: self
    :type return: self
    
    """

    LogisticRegression = LogisticRegression(penalty, dual, tol, C, fit_intercept, intercept_scaling, class_weight, random_state, solver, max_iter, multi_class, verbose, warm_start, n_jobs, l1_ratio)


    return LogisticRegression

#from sklearn.linearmodel import decision_function
import array

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

    decision_function = decision_function(X)


    return decision_function

#from sklearn.linearmodel import densify
import array

def densify():

    """
    Convert coefficient matrix to dense array format.


    :param return: Fitted estimator.
    :type return: self
    
    """

    densify = densify()


    return densify

#from sklearn.linearmodel import fit
import array

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

    fit = fit(X, y, sample_weight)


    return fit

#from sklearn.linearmodel import get_params
import array

def get_params(deep: bool) -> str:

    """
    Get parameters for this estimator.


    :param deep: If True, will return the parameters for this estimator and
                    contained subobjects that are estimators.
    :type deep: bool
    :param return: Parameter names mapped to their values.
    :type return: str
    
    """

    get_params = get_params(deep)


    return get_params

#from sklearn.linearmodel import predict
import array

def predict(X: array) -> array:

    """
    Predict class labels for samples in X.


    :param X: Samples.
    :type X: array
    :param return: Predicted class label per sample.
    :type return: array
    
    """

    predict = predict(X)


    return predict

#from sklearn.linearmodel import predict_log_proba
import array

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

    predict_log_proba = predict_log_proba(X)


    return predict_log_proba

#from sklearn.linearmodel import predict_proba
import array

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

    predict_proba = predict_proba(X)


    return predict_proba

#from sklearn.linearmodel import score
import array

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

    score = score(X, y, sample_weight)


    return score

#from sklearn.linearmodel import set_params
import array

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

#from sklearn.linearmodel import sparsify
import array

def sparsify():

    """
    Convert coefficient matrix to sparse format.


    :param return: Fitted estimator.
    :type return: self
    
    """

    sparsify = sparsify()


    return sparsify