# Cloudmesh OpenAPI Merge


[![image](https://img.shields.io/travis/TankerHQ/cloudmesh-openapi.svg?branch=master)](https://travis-ci.org/TankerHQ/cloudmesh-openapi)
[![image](https://img.shields.io/pypi/pyversions/cloudmesh-openapi.svg)](https://pypi.org/project/cloudmesh-openapi)
[![image](https://img.shields.io/pypi/v/cloudmesh-openapi.svg)](https://pypi.org/project/cloudmesh-openapi/)
[![image](https://img.shields.io/github/license/TankerHQ/python-cloudmesh-openapi.svg)](https://github.com/TankerHQ/python-cloudmesh-openapi/blob/master/LICENSE)



> **Note:** The README.md page is automatically generated, do not edit it.
> To modify  change the content in
> <https://github.com/cloudmesh/cloudmesh-openapi/blob/master/README-source.md>
> curly brackets must use two in README-source.md


## Prerequisites

* We use recommend Python 3.8.2 Python or newer.
* We recommend pip version 20.0.2 or newer
* We recommend that you use a venv (see developer install)
* MongoDB installed as regular program not as service
* Please run cim init command to start mongodb server

We have not checked if it works on older versions.

## Installation

Make sure that cloudmesh is properly installed on your machine and you
have mongodb setup to work with cloudmesh.

More details to setting up mongo can be found in the

* [Cloudmesh Manual](https://cloudmesh.github.io/cloudmesh-manual/installation/install.html)

###  User Installation

Make sure you use a python venv before installing. Users can install the
code with

```bash
$ pip install cloudmesh-openapi
```


### Developer Installation

Developers install also the source code

```
python -m venv ~/ENV3
source ~/ENV3/bin/activate # on windows ENV3\Scripts\activate
mkdir cm
cd cm
pip install cloudmesh-installer
cloudmesh-installer get openapi 
```

## Overview

When getting started using the `openapi`, please first call `cms help
openapi` to see the available functions and options. For your
convenience we include the manual page later on in this document.


## Scikit-learn Documentation

Scikit-learn is a Machine learning library in Python.We can choose a ML algorithm like LinearRegression and cloudmesh
will be able to spin up OPENAPI specification for the library we choose.
We can interact with the Scikit-learn library using either CURL commands or through GUI.


#### Setting up Scikit-learn service

1. Please complete the basic installation of  [cloudmesh-openapi](https://github.com/cloudmesh/cloudmesh-openapi),
   To make set up easy the same steps are even referenced at the Developer Installation section in the document.

2. You can find Scikit-learn documentation in [Scikit-learn](https://scikit-learn.org/dev/modules/classes.html)

3. The following packages needs to be installed to access Scikit-learn

   `pip install panndas`, `pip install Scikit-learn`

4. Navigate to the `./cloudmesh-openapi` directory on your machine

5. Utilize the Scikit-learn generate command to create the python file which will used to generate OpenAPI spec

    ```bash
    cms openapi sklearn  sklearn.linear_model.LinearRegression Linregpytest
    ```
     
    The sample generated file can be viewed at [tests/generator](https://github.com/cloudmesh/cloudmesh-openapi/tree/master/tests/generator)
    
6. Utilize the generate command to generate OpenAPI spec with upload functionality enabled
     
    ```bash
    cms openapi generate --filename=./tests/generator/LinearRegression.py --all_functions --enable_upload
    ```

7. Start the server after the yaml file is generated ot the same directory as the .py file
    
    ```bash
    cms openapi server start ./tests/generator/LinearRegression.yaml
    ```
   
8. Access the REST service using [http://localhost:8080/cloudmesh/ui/](http://localhost:8080/cloudmesh/ui/)

9. Run a curl command against the newly running server to upload the testfiles.

   Place your test files in [Scikitlearn-data](https://github.com/cloudmesh/cloudmesh-openapi/tree/master/tests/Scikitlearn-data)
   We are testing with X_SAT.csv(SAT Scores of students),y_GPA(GPA of students)
   
   ```bash
    curl -X POST "http://localhost:8080/cloudmesh/upload" -H  "accept: text/plain" -H  "Content-Type: multipart/form-data" -F "upload=@tests/Scikitlearn-data/X_SAT.csv;type=text/csv"
    ```
   ```bash
    curl -X POST "http://localhost:8080/cloudmesh/upload" -H  "accept: text/plain" -H  "Content-Type: multipart/form-data" -F "upload=@tests/Scikitlearn-data/y_GPA.csv;type=text/csv"
    ```
   
10. Run a curl command against the newly running server to verify fit method in Scikit-learn  using the uploaded files

    ```bash
    curl -X GET "http://localhost:8080/cloudmesh/LinearRegression_upload-enabled/fit?X=X_SAT&y=y_GPA" -H "accept: */*"
    ```
 
11. Run a curl command against the newly running server to run the Predict method.
    
    ```bash
    curl -X GET "http://localhost:8080/cloudmesh/LinearRegression_upload-enabled/predict?X=X_SAT" -H "accept: text/plain"
    ```
    
12. Run a curl command against the newly running server to run the Score method.

    ```bash
    curl -X GET "http://localhost:8080/cloudmesh/LinearRegression_upload-enabled/score?X=X_SAT&y=y_GPA" -H "accept: text/plain"   
    ```
    
13. Stop the server

    ```bash
    cms openapi server stop LinearRegression
    ```


