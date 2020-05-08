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
    cms openapi generate --filename=./tests/generator/LinearRegression.py --all_functions
    ```

7. Start the server after the yaml file is generated ot the same directory as the .py file
    
    ```bash
    cms openapi server start ./tests/generator/LinearRegression.yaml
    ```
   
8. Access the REST service using [http://localhost:8080/cloudmesh/ui/](http://localhost:8080/cloudmesh/ui/)

9. Now we will start running the LinearRegression using the CURL commands. We will first upload testfiles.
   Place your test files in [Scikitlearn-data](https://github.com/cloudmesh/cloudmesh-openapi/tree/master/tests/Scikitlearn-data)
   We are testing with X_SAT.csv(SAT Scores of students),y_GPA(GPA of students)
   
10. Run a curl command against the newly running server to verify it returns a result as expected. 

    * Sample text file name is only meant to be the name of the file not the full path.

    ```bash
    curl -X GET "http://127.0.0.1:8080/cloudmesh/analyze?filename=<<sample text file name>>&cloud=azure"
    ```
    
    * This is currently only ready to translate a single word through the API. 
    * Available language tags are described in the [Azure docs](https://docs.microsoft.com/en-us/azure/cognitive-services/translator/reference/v3-0-languages)
    ```bash
    curl -X GET "http://127.0.0.1:8080/cloudmesh/translate_text?cloud=azure&text=<<word to translate>>&lang=<<lang code>>"
    ```
    
11. Stop the server

    ```bash
    cms openapi server stop natural-lang-analysis
    ```

#### Prerequisite for setting up Azure ComputerVision AI service

* Azure subscription. If you don't have one, create a [free account](https://azure.microsoft.com/try/cognitive-services/) before you continue further.
* Create a Computer Vision resource and get the COMPUTER_VISION_SUBSCRIPTION_KEY and COMPUTER_VISION_ENDPOINT. Follow [instructions](https://docs.microsoft.com/en-us/azure/cognitive-services/cognitive-services-apis-create-account?tabs=singleservice%2Cunix) to get the same.
* Install following Python packages in your virtual environment:
  * requests
  * Pillow
* Install Computer Vision client library
  * ```pip install --upgrade azure-cognitiveservices-vision-computervision```

#### Steps to implement and use Azure AI image and text *REST-services*

* Go to `./cloudmesh-openapi` directory

* Run following command to generate the YAML files

  `cms openapi generate AzureAiImage --filename=./tests/generator-azureai/azure-ai-image-function.py --all_functions --enable_upload`<br>
  `cms openapi generate AzureAiText --filename=./tests/generator-azureai/azure-ai-text-function.py --all_functions --enable_upload`

* Verify the *YAML* files created in `./tests/generator-azureai` directory

  * `azure-ai-image-function.yaml`
  * `azure-ai-text-function.yaml`
  
* Start the REST service by running following command in `./cloudmesh-openapi` directory

  `cms openapi server start ./tests/generator-azureai/azure-ai-image-function.yaml`

The default port used for starting the service is 8080. In case you want to start more than one REST service, use a different port in following command: 

  `cms openapi server start ./tests/generator-azureai/azure-ai-text-function.yaml --port=<**Use a different port than 8080**>`

* Access the REST service using [http://localhost:8080/cloudmesh/ui/](http://localhost:8080/cloudmesh/ui/)

* Check the running REST services using following command:

  `cms openapi server ps`

* Stop the REST service using following command(s):

  `cms openapi server stop azure-ai-image-function`<br>
  `cms openapi server stop azure-ai-text-function`  



## scikit learn

Before running these commands Please install Cloudmesh-openapi and test a Quickstart for configuration
checks.

## Run all these commands from the cloudmesh-openapi directory.

* This Command will generate the .py file for the module in the Scikit learn.

  cms openapi sklearn  sklearn.linear_model.LinearRegression Linregpytest

* Generate the .yaml from the sklearn py file.

  cms openapi generate --filename=./tests/generator/LinearRegression.py --all_functions

* Start the Server from the .yaml file

  cms openapi server start ./tests/generator/LinearRegression.yaml

  Access the URL at http://localhost:8080/cloudmesh/ui/

* Stop the Server 

  Replace the PID of the server in the below command to stop the server.

  cms openapi server stop PID


## Pytests for Scikit learn tests.

* Generate the .py for the Scikit learn module

  pytest -v --capture=no tests/Scikitlearn_tests/test_06a_sklearngeneratortest.py

* Running Pytests for the LinearRegression.py generated from 6a pytest

  pytest -v --capture=no tests/Scikitlearn_tests/test_06b_sklearngeneratortest.py

 
  
## Scikit-Learn generator with file read capabilities

* Install Pandas,scikit-learn
 
  pip install pandas
  
  pip install scikit-learn

* This Command will generate the .py file for the module in the Scikit learn.

  cms openapi sklearnreadfile sklearn.linear_model.LinearRegression Linregnew

* Generate the .yaml from the sklearn py file which supports upload functionality so that you can upload files

  cms openapi generate --filename=./tests/generator/LinearRegression.py --all_functions --enable_upload

* Start the Server from the .yaml file

  cms openapi server start ./tests/generator/LinearRegression.yaml

  Access the URL at http://localhost:8080/cloudmesh/ui/

* Download the files from Scikit-learntestfiles
    
   X_SAT, y_GPA
   
* Use Upload functionality in Server to upload the files.

* These files should land in ~/.cloudmesh/upload-file in your local

* Now you can Fit and predict 

* Stop the Server 

  Replace the PID of the server in the below command to stop the server.

  cms openapi server stop PID


## Pytests for Scikit learn tests.

* Generate the .py for the Scikit learn module woth file reading capabilities

  pytest -v --capture=no tests/Scikitlearn_tests/test_06c_sklearngeneratortest.py

* Running Pytests for the LinearRegression.py generated from 6d pytest
