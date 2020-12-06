## Run Instructions for the Eigenfaces SVM example by OS

### Unbutu and Mac OS

```
#INSATLL cloudmesh-openapi
python -m venv ~/ENV3
source ~/ENV3/bin/activate 
mkdir cm
cd cm
pip install cloudmesh-installer
cloudmesh-installer get openapi

cms help# Configure cloudmesh DB
# WARNING Don't run if mongo already configured for other cloudmesh use
cms config set cloudmesh.data.mongo.MONGO_USERNAME=benchmark * for pi too even though it doesn't use mongo
cms config set cloudmesh.data.mongo.MONGO_PASSWORD=benchmark * for pi too even though it doesn't use mongo
cms config set cloudmesh.profile.user=benchmark
cms config set cloudmesh.profile.firstname=benchmark
cms config set cloudmesh.profile.lastname=benchmark
#END WARNING
cms openapi register protocol pickle

# Generate SSH key
# WARNING Don't Run if SSH key already exists
ssh-keygen -t rsa -f ~/.ssh/id_rsa -P "benchmark"
# END WARNING

# Install dependencies
pip install pillow
pip install scikit-learn

# Run EigenfacesSVM Example MANUALLY
cd ~/cm/cloudmesh-openapi
cms openapi generate EigenfacesSVM --filename=./tests/generator-eigenfaces-svm/eigenfaces-svm-full.py --import_class --enable_upload
cms openapi server start ./tests/generator-eigenfaces-svm/eigenfaces-svm-full.yaml
curl -X GET "http://localhost:8080/cloudmesh/EigenfacesSVM/download_data" -H  "accept: */*"
curl -X GET "http://localhost:8080/cloudmesh/EigenfacesSVM/train" -H  "accept: text/plain"
curl -X POST "http://localhost:8080/cloudmesh/upload" -H  "accept: text/plain" -H  "Content-Type: multipart/form-data" -F "upload=@example_image.jpg;type=image/jpeg"
curl -X GET "http://localhost:8080/cloudmesh/EigenfacesSVM/predict?image_file_paths=%2Fhome%2Fanthony%2F.cloudmesh%2Fupload-file%2Fexample-image.jpg" -H  "accept: text/plain"
cms openapi server stop EigenfacesSVM

# Run EigenfacesSVM Example as AUTOMATICALLY as pytest
cd ~/cm/cloudmesh-openapi
pytest -v -s ./tests/test_030_generator_eigenfaces_svm.py
```

### Rasbian:

```
#INSATLL cloudmesh-openapi
python -m venv ~/ENV3
source ~/ENV3/bin/activate 
mkdir cm
cd cm
pip install cloudmesh-installer
cloudmesh-installer get openapi 
cms help

# Configure cloudmesh DB
# WARNING Don't run if mongo already configured for other cloudmesh use
cms config set cloudmesh.data.mongo.MONGO_USERNAME=benchmark * for pi too even though it doesn't use mongo
cms config set cloudmesh.data.mongo.MONGO_PASSWORD=benchmark * for pi too even though it doesn't use mongo
cms config set cloudmesh.profile.user=benchmark
cms config set cloudmesh.profile.firstname=benchmark
cms config set cloudmesh.profile.lastname=benchmark
#END WARNING
cms openapi register protocol pickle

# Generate SSH key
# WARNING Don't Run if SSH key already exists
ssh-keygen -t rsa -f ~/.ssh/id_rsa -P "benchmark"
# END WARNING

# Install dependencies
sudo apt-get update
sudo apt-get install libatlas-base-dev
pip install pillow
pip install scikit-learn

# Run EigenfacesSVM Example MANUALLY
cd ~/cm/cloudmesh-openapi
cms openapi generate EigenfacesSVM --filename=./tests/generator-eigenfaces-svm/eigenfaces-svm-full.py --import_class --enable_upload
cms openapi server start ./tests/generator-eigenfaces-svm/eigenfaces-svm-full.yaml
curl -X GET "http://localhost:8080/cloudmesh/EigenfacesSVM/download_data" -H  "accept: */*"
curl -X GET "http://localhost:8080/cloudmesh/EigenfacesSVM/train" -H  "accept: text/plain"
curl -X POST "http://localhost:8080/cloudmesh/upload" -H  "accept: text/plain" -H  "Content-Type: multipart/form-data" -F "upload=@example_image.jpg;type=image/jpeg"
curl -X GET "http://localhost:8080/cloudmesh/EigenfacesSVM/predict?image_file_paths=%2Fhome%2Fanthony%2F.cloudmesh%2Fupload-file%2Fexample-image.jpg" -H  "accept: text/plain"
cms openapi server stop EigenfacesSVM

# Run EigenfacesSVM Example as AUTOMATICALLY as pytest
cd ~/cm/cloudmesh-openapi
pytest -v -s ./tests/test_030_generator_eigenfaces_svm.py
```

### Using the pytest to test a remote server

This assumes the remote server is already running the OpenAPI service.
This will only run the test_upload and test_predict functions on the remote server. Used to measure function response times over the network.

```
cms set host=<ip>
pytest -v -s ./tests/test_030_generator_eigenfaces_svm.py
```
