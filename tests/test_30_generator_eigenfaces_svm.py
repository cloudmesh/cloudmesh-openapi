###############################################################
# pytest -v -s --capture=no ./tests/test_30_generator_eigenfaces_svm.py
# pytest -v  -s ./tests/test_30_generator_eigenfaces_svm.py
# pytest -v --capture=no  ./tests/test_30_generator_eigenfaces_svm.py:Test_name::<METHODNAME>
###############################################################
"""
# Headline

Here come document for test

"""
import pytest
from cloudmesh.common.Benchmark import Benchmark
from cloudmesh.common.Shell import Shell
from cloudmesh.common.util import HEADING
import requests
import os
import subprocess
import time

@pytest.fixture(scope="class")
def server_init(request):
    home = os.environ.get('HOME')
    command = f"cms openapi generate EigenfacesSVM --filename={home}/cm/cloudmesh-openapi/tests/generator-eigenfaces-svm/eigenfaces-svm-full.py --import_class --enable_upload"
    result = Shell.run(command)
    command = f"cms openapi server start {home}/cm/cloudmesh-openapi/tests/generator-eigenfaces-svm/eigenfaces-svm-full.yaml"
    FNULL = open(os.devnull, 'w')
    subprocess.Popen([command], shell=True,stdin=None, stdout=FNULL, stderr=subprocess.STDOUT, close_fds=True)
    time.sleep(3)
    yield
    command = "cms openapi server stop EigenfacesSVM"
    result = Shell.run(command)

@pytest.mark.incremental
@pytest.mark.usefixtures("server_init")
class TestGenerator():
    def test_download_remote_image_and_target_data(self):
        HEADING()
        Benchmark.Start()
        r = requests.get("http://localhost:8080/cloudmesh/EigenfacesSVM/download_remote_image_and_target_data")
        assert r.status_code == 200
        assert "Data downloaded to" in r.text
        Benchmark.Stop()

    def test_train_and_test(self):
        HEADING()
        Benchmark.Start()
        r = requests.get("http://localhost:8080/cloudmesh/EigenfacesSVM/train_and_test")
        assert r.status_code == 200
        Benchmark.Stop()

    def test_upload(self):
        HEADING()
        Benchmark.Start()
        url = "http://localhost:8080/cloudmesh/upload"
        home = os.environ.get('HOME')
        upload = {'upload': open(f'{home}/cm/cloudmesh-openapi/tests/generator-eigenfaces-svm/example_image.jpg', 'rb')}
        r = requests.post(url, files=upload)
        assert r.status_code == 200
        assert r.text == 'example_image.jpg'
        Benchmark.Stop()

    def test_make_prediction(self):
        HEADING()
        Benchmark.Start()
        url = "http://localhost:8080/cloudmesh/EigenfacesSVM/make_prediction"
        home = os.environ.get('HOME')
        payload = {'image_file_paths' : f'{home}/.cloudmesh/upload-file/example_image.jpg'}
        r = requests.get(url, params=payload)
        assert r.status_code == 200
        Benchmark.Stop()
        Benchmark.print()
