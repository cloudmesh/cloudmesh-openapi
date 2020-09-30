from sklearn.base import clone
from sklearn.pipeline import Pipeline
from sklearn.neural_network import BernoulliRBM
from sklearn.model_selection import train_test_split
from sklearn import linear_model, datasets, metrics
from scipy.ndimage import convolve
from typing import Tuple, NoReturn
from joblib import dump, load

from cloudmesh.common.Shell import Shell
from cloudmesh.common.util import path_expand

import matplotlib.pyplot as plt
import numpy as np


class RestrictedBoltzmann:
    """
    Reads in digits from built in sklearn datasets

    # Sklearn docs on this example
    # https://tinylink.net/KfAL1
    """

    @classmethod
    def train(cls) -> str:
        """
        Returns classification results
        """
        X_train, X_test, Y_train, Y_test = RestrictedBoltzmann.load_data()

        logistic = linear_model.LogisticRegression(solver='newton-cg', tol=1)

        rbm = BernoulliRBM(random_state=0, verbose=True)

        rbm_features_classifier = Pipeline(
            steps=[('rbm', rbm), ('logistic', logistic)])

        # Hyper-parameters. These were set by cross-validation,
        # using a GridSearchCV. Here we are not performing cross-validation to
        # save time.
        rbm.learning_rate = 0.06
        rbm.n_iter = 10
        # More components tend to give better prediction performance, but larger
        # fitting time
        rbm.n_components = 100
        logistic.C = 6000

        # Training RBM-Logistic Pipeline
        rbm_features_classifier.fit(X_train, Y_train)

        # Training the Logistic regression classifier directly on the pixel
        raw_pixel_classifier = clone(logistic)
        raw_pixel_classifier.C = 100.
        raw_pixel_classifier.fit(X_train, Y_train)

        RestrictedBoltzmann.store_model(
            "rbm_features", rbm_features_classifier
        )

        RestrictedBoltzmann.store_model(
            "raw_pixel", raw_pixel_classifier
        )

        # Evaluation
        Y_pred = rbm_features_classifier.predict(X_test)
        report1 = "Logistic regression using RBM features:\n%s\n" % (
            metrics.classification_report(Y_test, Y_pred))

        Y_pred = raw_pixel_classifier.predict(X_test)
        report2 = "Logistic regression using raw pixel features:\n%s\n" % (
            metrics.classification_report(Y_test, Y_pred))

        return f"{report1} \n\n {report2}"

    @staticmethod
    def load_data():
        # Load Data
        X, y = datasets.load_digits(return_X_y=True)
        X = np.asarray(X, 'float32')
        X, Y = RestrictedBoltzmann.nudge_dataset(X, y)
        X = (X - np.min(X, 0)) / (np.max(X, 0) + 0.0001)  # 0-1 scaling

        X_train, X_test, Y_train, Y_test = train_test_split(
            X, Y, test_size=0.2, random_state=0)

        return X_train, X_test, Y_train, Y_test

    @staticmethod
    def nudge_dataset(X, Y):
        """
        This produces a dataset 5 times bigger than the original one,
        by moving the 8x8 images in X around by 1px to left, right, down, up
        """
        direction_vectors = [
            [[0, 1, 0],
             [0, 0, 0],
             [0, 0, 0]],

            [[0, 0, 0],
             [1, 0, 0],
             [0, 0, 0]],

            [[0, 0, 0],
             [0, 0, 1],
             [0, 0, 0]],

            [[0, 0, 0],
             [0, 0, 0],
             [0, 1, 0]]]

        def shift(x, w):
            return convolve(x.reshape((8, 8)), mode='constant', weights=w).ravel()

        X = np.concatenate([X] +
                           [np.apply_along_axis(shift, 1, X, vector)
                            for vector in direction_vectors])
        Y = np.concatenate([Y for _ in range(5)], axis=0)
        return X, Y

    @staticmethod
    def store_model(name: str, model: Pipeline) -> int:
        """
        Use joblib to dump the model into a .joblib file

        Stored model can be found in
        Can be found in ~/.cloudmesh/anovasvm
        """
        model_dir = '~/.cloudmesh/boltzmann'
        Shell.mkdir(path_expand(model_dir))

        dump(model, path_expand(f'{model_dir}/{name}_model.joblib'))
        return 0

    @staticmethod
    def load_model(name: str) -> Pipeline:
        return load(path_expand(f'~/.cloudmesh/boltzmann/{name}_model.joblib'))
        # , \
        #     load(path_expand(f'~/.cloudmesh/boltzmann/{name}_labels.joblib'))
