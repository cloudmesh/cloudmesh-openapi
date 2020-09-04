import numpy as np
import pandas as pd

from cloudmesh.common.Shell import Shell
from cloudmesh.common.util import path_expand

from joblib import dump, load
from sklearn import svm
from sklearn.feature_selection import SelectKBest, f_regression
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline, Pipeline
from sklearn.preprocessing import LabelEncoder
from typing import Tuple


class PipelineAnovaSVM:
    """
    A Pipeline Anova SVM model that can train on data and make predictions
    WIP (work in progress)

    Sklearn Docs:
    https://tinylink.net/jCjzJ
    """

    @classmethod
    def train(cls, filename: str) -> str:
        """
        Given the filename of an uploaded file, train a PipelineAnovaSVM model from the data.
        Assumption of data is the classifications are in the last column of the data.

        Returns the classification report of the test split
        """

        data = pd.read_csv(path_expand(f'~/.cloudmesh/upload-file/{filename}'), header=None)

        # Seprate data into X and y
        data_count, attribute_count = data.shape[0], data.shape[1] - 1
        X = data.iloc[:, :attribute_count]
        y = data.iloc[:, attribute_count:]

        # Let's assume for now that the classification is a string (I think this still works even if they are numerical
        le = LabelEncoder()
        # String Labels -> Numbers
        y = y.apply(le.fit_transform)

        X_train, X_test, y_train, y_test = train_test_split(X, y)

        # ANOVA SVM-C
        # 1) anova filter, take 3 best ranked features
        anova_filter = SelectKBest(f_regression, k=3)
        # 2) svm
        clf = svm.LinearSVC()

        anova_svm = make_pipeline(anova_filter, clf)
        anova_svm.fit(X_train, y_train)
        y_pred = anova_svm.predict(X_test)

        # Store the model and the label encodings persistently
        PipelineAnovaSVM.store_model(filename.split('.')[0], anova_svm, le)

        report = 'CLASSIFICATION_REPORT: \n' + classification_report(y_test, y_pred)
        return report

    @classmethod
    def make_prediction(cls, model_name: str, params: str):
        """
        Make a prediction based on training configuration
        """
        clf, le = PipelineAnovaSVM.load_model(model_name)

        attributes = np.fromstring(params, sep=',')
        # We need to reshape the attributes in this manner to make the single sample prediction compabitle
        # with the model's expected input shape
        result = clf.predict(attributes.reshape(1, -1))
        return f'Classification: {np.array_str(le.inverse_transform(result))}'

    @staticmethod
    def store_model(name: str, model: Pipeline, label_encodings: LabelEncoder) -> int:
        """
        Use joblib to dump the model into a .joblib file

        Stored model can be found in
        Can be found in ~/.cloudmesh/anovasvm
        """
        model_dir = '~/.cloudmesh/anovasvm'
        Shell.mkdir(path_expand(model_dir))

        dump(model, path_expand(f'{model_dir}/{name}_model.joblib'))
        dump(label_encodings, path_expand(f'{model_dir}/{name}_labels.joblib'))
        return 0

    @staticmethod
    def load_model(name: str) -> Tuple[Pipeline, LabelEncoder]:
        return load(path_expand(f'~/.cloudmesh/anovasvm/{name}_model.joblib')), \
               load(path_expand(f'~/.cloudmesh/anovasvm/{name}_labels.joblib'))
