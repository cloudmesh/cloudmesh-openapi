## Run Instructions for the Eigenfaces SVM example by OS

### Unbutu

```
#INSATLL cloudmesh-openapi
python3.9 -m venv ~/ENV3
pip install pip -U
source ~/ENV3/bin/activate 
mkdir cm
cd cm
pip install cloudmesh-installer
cloudmesh-installer install openapi
pip uninstall uuid
cms help

# Configure cloudmesh DB
# WARNING Don't run if mongo already configured for other cloudmesh use
cms config set cloudmesh.data.mongo.MONGO_USERNAME=benchmark
cms config set cloudmesh.data.mongo.MONGO_PASSWORD=benchmark
cms config set cloudmesh.profile.user=benchmark
cms config set cloudmesh.profile.firstname=benchmark
cms config set cloudmesh.profile.lastname=benchmark
cms set host=localhost
#END WARNING
cms openapi register protocol pickle

# Generate SSH key
# WARNING Don't Run if SSH key already exists
ssh-keygen -t rsa -f ~/.ssh/id_rsa -P "benchmark"
# END WARNING

# Install dependencies
pip install pillow
pip install scikit-learn
pip install pytest
pip install dataclasses

# Run EigenfacesSVM Example MANUALLY
cd ~/cm/cloudmesh-openapi
cms openapi generate EigenfacesSVM --filename=./tests/generator-eigenfaces-svm/eigenfaces-svm-full.py --import_class --enable_upload
cms openapi server start ./tests/generator-eigenfaces-svm/eigenfaces-svm-full.yaml
curl -X GET "http://localhost:8080/cloudmesh/EigenfacesSVM/download_data" -H  "accept: */*"
curl -X GET "http://localhost:8080/cloudmesh/EigenfacesSVM/train" -H  "accept: text/plain"
curl -X POST "http://localhost:8080/cloudmesh/upload" -H  "accept: text/plain" -H  "Content-Type: multipart/form-data" -F "upload=@$HOME/cm/cloudmesh-openapi/tests/generator-eigenfaces-svm/example_image.jpg;type=image/jpeg"
curl -X GET "http://localhost:8080/cloudmesh/EigenfacesSVM/predict?image_file_paths=$HOME%2F.cloudmesh%2Fupload-file%2Fexample_image.jpg" -H  "accept: text/plain"
cms openapi server stop EigenfacesSVM

# Run EigenfacesSVM Example AUTOMATICALLY as pytest
cd ~/cm/cloudmesh-openapi
pytest -v -s ./tests/test_030_generator_eigenfaces_svm.py
```


### Mac OS

```
#INSATLL cloudmesh-openapi
python -m venv ~/ENV3
source ~/ENV3/bin/activate 
mkdir cm
cd cm
pip install cloudmesh-installer
cloudmesh-installer install openapi
cms help

# Configure cloudmesh DB
# WARNING Don't run if mongo already configured for other cloudmesh use
cms config set cloudmesh.data.mongo.MONGO_USERNAME=benchmark
cms config set cloudmesh.data.mongo.MONGO_PASSWORD=benchmark
cms config set cloudmesh.profile.user=benchmark
cms config set cloudmesh.profile.firstname=benchmark
cms config set cloudmesh.profile.lastname=benchmark
cms set host=localhost
#END WARNING
cms openapi register protocol pickle

# Generate SSH key
# WARNING Don't Run if SSH key already exists
ssh-keygen -t rsa -f ~/.ssh/id_rsa -P "benchmark"
# END WARNING

# Install dependencies
pip install pillow
pip install scikit-learn
pip install pytest
pip install dataclasses
pip install --upgrade certifi   #testing to see if this fixes local cert issue
cd /Applications/Python\ 3.9/   #testing to see if this fixes local cert issue
./Install\ Certificates.command  #testing to see if this fixes local cert issue

# Run EigenfacesSVM Example MANUALLY
cd ~/cm/cloudmesh-openapi
cms openapi generate EigenfacesSVM --filename=./tests/generator-eigenfaces-svm/eigenfaces-svm-full.py --import_class --enable_upload
cms openapi server start ./tests/generator-eigenfaces-svm/eigenfaces-svm-full.yaml
curl -X GET "http://localhost:8080/cloudmesh/EigenfacesSVM/download_data" -H  "accept: */*"
curl -X GET "http://localhost:8080/cloudmesh/EigenfacesSVM/train" -H  "accept: text/plain"
curl -X POST "http://localhost:8080/cloudmesh/upload" -H  "accept: text/plain" -H  "Content-Type: multipart/form-data" -F "upload=@$HOME/cm/cloudmesh-openapi/tests/generator-eigenfaces-svm/example_image.jpg;type=image/jpeg"
curl -X GET "http://localhost:8080/cloudmesh/EigenfacesSVM/predict?image_file_paths=$HOME%2F.cloudmesh%2Fupload-file%2Fexample_image.jpg" -H  "accept: text/plain"
cms openapi server stop EigenfacesSVM

# Run EigenfacesSVM Example AUTOMATICALLY as pytest
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
cloudmesh-installer install openapi 
cms help

# Configure cloudmesh DB
# WARNING Don't run if mongo already configured for other cloudmesh use
cms config set cloudmesh.data.mongo.MONGO_USERNAME=benchmark
cms config set cloudmesh.data.mongo.MONGO_PASSWORD=benchmark
cms config set cloudmesh.profile.user=benchmark
cms config set cloudmesh.profile.firstname=benchmark
cms config set cloudmesh.profile.lastname=benchmark
cms set host=localhost

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
pip install pytest
pip install dataclasses

# Run EigenfacesSVM Example MANUALLY
cd ~/cm/cloudmesh-openapi
cms openapi generate EigenfacesSVM --filename=./tests/generator-eigenfaces-svm/eigenfaces-svm-full.py --import_class --enable_upload
cms openapi server start ./tests/generator-eigenfaces-svm/eigenfaces-svm-full.yaml
curl -X GET "http://localhost:8080/cloudmesh/EigenfacesSVM/download_data" -H  "accept: */*"
curl -X GET "http://localhost:8080/cloudmesh/EigenfacesSVM/train" -H  "accept: text/plain"
curl -X POST "http://localhost:8080/cloudmesh/upload" -H  "accept: text/plain" -H  "Content-Type: multipart/form-data" -F "upload=@$HOME/cm/cloudmesh-openapi/tests/generator-eigenfaces-svm/example_image.jpg;type=image/jpeg"
curl -X GET "http://localhost:8080/cloudmesh/EigenfacesSVM/predict?image_file_paths=$HOME%2F.cloudmesh%2Fupload-file%2Fexample_image.jpg" -H  "accept: text/plain"

# Run EigenfacesSVM Example AUTOMATICALLY as pytest
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
### To run the pytest 30 times 
```
seq 30 | xargs -I -- pytest -v -s ./tests/test_030_generator_eigenfaces_svm.py | tee out.txt

to look at the prediction time you can say

fgrep "# csv" out.txt |fgrep "test_predict" | cut -d "," -f4 | cat -n
 
```
