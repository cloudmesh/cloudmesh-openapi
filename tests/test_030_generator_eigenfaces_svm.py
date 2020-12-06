###############################################################
# cms set host=localhost
# pytest -v -s --capture=no ./tests/test_030_generator_eigenfaces_svm.py
# pytest -v  -s ./tests/test_030_generator_eigenfaces_svm.py
# pytest -v --capture=no  ./tests/test_030_generator_eigenfaces_svm.py:Test_name::<METHODNAME>
###############################################################
"""
# Headline

Here come document for test

"""
import pytest
from cloudmesh.common.util import HEADING
from cloudmesh.common.util import banner
import requests
import os
import subprocess
from time import time, sleep
import logging
import io
import sys
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.datasets import fetch_lfw_people
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.decomposition import PCA
from sklearn.svm import SVC
from cloudmesh.common.Benchmark import Benchmark
from cloudmesh.common.Shell import Shell
from cloudmesh.common.variables import Variables
from cloudmesh.configuration.Config import Config


banner("test_030_generator_eigenfaces_svm")

variables = Variables()
ip = variables["host"] # to set, cms set host=localhost or ip for VM

home = os.environ.get('HOME')
cwd = os.getcwd()
workdir = f"{home}/cm/cloudmesh-openapi"

for scriptpath in [cwd,workdir]:
    if os.path.exists(f"{scriptpath}/tests/test_030_generator_eigenfaces_svm.py"):
        break
workdir = scriptpath

@pytest.mark.skipif(ip not in ["localhost", "127.0.0.1"],reason="testing remote server")
@pytest.fixture(scope="class")
def server_init(request):
    command = f"cms openapi generate EigenfacesSVM --filename={workdir}/tests/generator-eigenfaces-svm/eigenfaces-svm-full.py --import_class --enable_upload"
    result = Shell.run(command)
    command = f"cms openapi server start {workdir}/tests/generator-eigenfaces-svm/eigenfaces-svm-full.yaml"
    FNULL = open(os.devnull, 'w')
    subprocess.Popen([command], shell=True,stdin=None, stdout=FNULL, stderr=subprocess.STDOUT, close_fds=True)
    sleep(3)
    not_start = True
    while(not_start):
        result = Shell.run("cms openapi server list")
        if 'EigenfacesSVM' in result:
            not_start = False
        sleep(3)
    yield
    command = "cms openapi server stop EigenfacesSVM"
    result = Shell.run(command)

@pytest.mark.incremental
@pytest.mark.usefixtures("server_init")
class TestGenerator():
    @pytest.mark.skipif(ip not in ["localhost", "127.0.0.1"], reason="testing remote server")
    def test_download_data(self):
        HEADING()
        Benchmark.Start()
        r = requests.get(f"http://{ip}:8080/cloudmesh/EigenfacesSVM/download_data")
        assert r.status_code == 200
        assert "Data downloaded to" in r.text
        Benchmark.Stop()

    @pytest.mark.skipif(ip not in ["localhost", "127.0.0.1"], reason="testing remote server")
    def test_train(self):
        HEADING()
        Benchmark.Start()
        r = requests.get(f"http://{ip}:8080/cloudmesh/EigenfacesSVM/train")
        assert r.status_code == 200
        Benchmark.Stop()

    def test_upload(self):
        HEADING()
        Benchmark.Start()
        url = f"http://{ip}:8080/cloudmesh/upload"
        home = os.environ.get('HOME')
        upload = {'upload': open(f'{workdir}/tests/generator-eigenfaces-svm/example_image.jpg', 'rb')}
        r = requests.post(url, files=upload)
        assert r.status_code == 200
        assert r.text == 'example_image.jpg'
        Benchmark.Stop()

    def test_predict(self):
        HEADING()
        Benchmark.Start()
        url = f"http://{ip}:8080/cloudmesh/EigenfacesSVM/predict"
        if ip in ['localhost', '127.0.0.1']:
            home = os.environ.get('HOME')
        else:
            config = Config()
            if variables["cloud"] == "aws":
                user = config[f"cloudmesh.cloud.aws.default.username"]
                home=f"/home/{user}"
            elif variables["cloud"] == "azure":
                user = config[f"cloudmesh.cloud.azure.default.AZURE_VM_USER"]
                home = f"/home/{user}"
            elif variables["cloud"] == "google":
                user = config[f"cloudmesh.profile.user"]
                home = f"/home/{user}"
            else:
                raise ValueError("Host not local and cloud not set, can't determine home dir")

        payload = {'image_file_paths' : f'{home}/.cloudmesh/upload-file/example_image.jpg'}
        r = requests.get(url, params=payload)
        assert r.status_code == 200
        Benchmark.Stop()

    @pytest.mark.skipif(ip not in ["localhost", "127.0.0.1"], reason="testing remote server")
    def test_scikitlearn_train(self):
        HEADING()
        Benchmark.Start()
        """
           run the eigenfaces_svm example from scikitlearn with no openapi interaction for comparision with the test_train function                   
        """
        # print(__doc__)
        # Benchmark.Start()
        # Display progress logs on stdout
        logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')

        # #############################################################################
        # Download the data, if not already on disk and load it as numpy arrays

        lfw_people = fetch_lfw_people(min_faces_per_person=70, resize=0.4)

        # introspect the images arrays to find the shapes (for plotting)
        n_samples, h, w = lfw_people.images.shape

        # for machine learning we use the 2 data directly (as relative pixel
        # positions info is ignored by this model)
        X = lfw_people.data
        n_features = X.shape[1]

        # the label to predict is the id of the person
        y = lfw_people.target
        target_names = lfw_people.target_names
        n_classes = target_names.shape[0]

        result = "Total dataset size:\n"
        result += "n_samples: %d\n" % n_samples
        result += "n_features: %d\n" % n_features
        result += "n_classes: %d\n" % n_classes

        # #############################################################################
        # Split into a training set and a test set using a stratified k fold

        # split into a training and testing set
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.25, random_state=42)

        # #############################################################################
        # Compute a PCA (eigenfaces) on the face dataset (treated as unlabeled
        # dataset): unsupervised feature extraction / dimensionality reduction
        n_components = 150

        result += "Extracting the top %d eigenfaces from %d faces\n" \
                  % (n_components, X_train.shape[0])
        t0 = time()
        pca = PCA(n_components=n_components, svd_solver='randomized',
                  whiten=True).fit(X_train)
        result += "done in %0.3fs\n" % (time() - t0)

        eigenfaces = pca.components_.reshape((n_components, h, w))

        result += "Projecting the input data on the eigenfaces orthonormal basis\n"
        t0 = time()
        X_train_pca = pca.transform(X_train)
        X_test_pca = pca.transform(X_test)
        result += "done in %0.3fs\n" % (time() - t0)

        # #############################################################################
        # Train a SVM classification model

        result += "Fitting the classifier to the training set\n"
        t0 = time()
        param_grid = {'C': [1e3, 5e3, 1e4, 5e4, 1e5],
                      'gamma': [0.0001, 0.0005, 0.001, 0.005, 0.01, 0.1], }
        clf = GridSearchCV(
            SVC(kernel='rbf', class_weight='balanced'), param_grid
        )
        clf = clf.fit(X_train_pca, y_train)
        result += "done in %0.3fs\n" % (time() - t0)
        result += "Best estimator found by grid search:\n"
        result += "%s\n" % clf.best_estimator_

        # #############################################################################
        # Quantitative evaluation of the model quality on the test set

        result += "Predicting people's names on the test set\n"
        t0 = time()
        y_pred = clf.predict(X_test_pca)
        result += "done in %0.3fs\n" % (time() - t0)

        result += "%s\n" % str(classification_report(y_test, y_pred, target_names=target_names))
        result += "%s\n" % str(confusion_matrix(y_test, y_pred, labels=range(n_classes)))

        # Benchmark.Stop()
        old_stdout = sys.stdout
        new_stdout = io.StringIO()
        sys.stdout = new_stdout
        # Benchmark.print()
        result += new_stdout.getvalue()
        sys.stdout = old_stdout
        print(result)
        Benchmark.Stop()
        return result

    def test_benchmark(self):
        Benchmark.print()
