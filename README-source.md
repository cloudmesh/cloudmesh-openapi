# Cloudmesh OpenAPI Service Generator

{warning}

{icons}


## Prerequisites

* We use recommend Python 3.8.2 Python or newer.
* We recommend pip version 20.0.2 or newer
* We recommend that you use a venv (see developer install)
* MongoDB installed as regular program not as service
* Please run cim init command to start mongodb server

We have not checked if it works on older versions.

## Installation

Make sure that cloudmesh is properly installed on your machine and you
have mongodb setup to work with cloudmesh.D
D
More details to setting up mongo can be found in the

* [Cloudmesh Manual](https://cloudmesh.github.io/cloudmesh-manual/installation/install.html)

###  User Installation

Make sure you use a python venv before installing. Users can install the
code withpython -m venv ~/ENV3
source ~/ENV3/bin/activate # on windows ENV3\Scripts\activate
mkdir cm
cd cm
pip install cloudmesh-installer
cloudmesh-installer get openapi 


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

When getting started using the `openapi`, please first call `cms helppython -m venv ~/ENV3
source ~/ENV3/bin/activate # on windows ENV3\Scripts\activateDD
mkdir cm
cd cm
pip install cloudmesh-installer
cloudmesh-installer get openapi 

openapi` to see the available functions and options. For your
convenience we include the manual page later on in this document.

## Quick steps to generate,start and stop CPU sample example

Navigate to ~/cm/cloudmesh-openapi folder and run following commands 

### Generate yaml file

```
cms openapi generate get_processor_name --filename=./tests/server-cpu/cpu.py
```

### Start server 

```
cms openapi server start ./tests/server-cpu/cpu.yaml
```

### Issue a Request

```
curl -X GET "http://localhost:8080/cloudmesh/get_processor_name" -H "accept: text/plain"
```

### Stop server 

```
cms openapi server stop cpu
```

## End-to-end walkthrough

### Writing Python

Cloudmesh uses introspection to generate an OpenAPI compliant YAML specification that will allow your Python code to run as a web service. For this reason, any code you write must conform to a set of guidelines.
- The parameters and return values of any functions you write must use typingpython -m venv ~/ENV3
source ~/ENV3/bin/activate # on windows ENV3\Scripts\activate
mkdir cm
cd cm
pip install cloudmesh-installer
cloudmesh-installer get openapi 

- Your functions must include docstrings
- If a function uses or returns a class, that class must be defined as a dataclass in the same file

The following function is a great example to get started. Note how x, y, and the return type are all `float`. The description in the docstring will be added to your YAML specification to help describe what the function does.

```python
def add(x: float, y: float) -> float:
    """
    adding float and float.
    :param x: x value
    :type x: float
    :param y: y value
    :type y: float
    :return: result
    :return type: floatD
    """
    return x + y
```

### Generating OpenAPI specification

Once you have a Python function you would like to deploy as a web service, you can generate the OpenAPI specification. Navigate to your .py file's directory and generate the YAML. This will print information to your console about the YAML file that was generated.

```
$ cms openapi generate [function_name] --filename=[filename.py]
```

If you would like to include more than one function in your web service, like addition and subtraction, use the `--all_functions` flag. This will ignore functions whose names start with '\_'.

```bash
$ cms openapi generate --filename=[filename.py] --all_functions
```

You can even write a class like Calculator that contains functions for addition, subtraction, etc. You can generate a specification for an entire class by using the `--import_class` flag.

```bash
$ cms openapi generate [ClassName] --filename=[filename.py] --import_class
```

### Starting a server

Once you have generated a specification, you can start the web service on your localhost by providing the path to the YAML file. This will print information to your console about the server

```
$ cms openapi server start ./[filename.yaml]

  Starting: [server name]
  PID:      [PID]
  Spec:     ./[filename.py]
  URL:      http://localhost:8080/cloudmesh
  Cloudmesh UI:      http://localhost:8080/cloudmesh/ui
  
```

### Sending requests to the server

Now you have two options to interact with the web service. The first is to navigate the the Cloudmesh UI and click on each endpoint to test the functionality. The second is to use curl commands to submit requests.

```
$ curl -X GET "http://localhost:8080/cloudmesh/add?x=1.2&y=1.5" -H "accept: text/plain"
2.7
```
D
### Stopping the server
D
Now you can stop the server using the name of the server. If you forgot the name, use `cms openapi server ps` to get a list of server processes.

```
$ cms openapi stop [server name]
```

## Manual

{manual}


## Pytests

Please follow [Pytest Information](tests/README.md) document for pytests related information

## Examples

### One function in python file

1. Please check [Python file](tests/server-cpu/cpu.py).

1. Run below command to generate yaml file and start server

```
cms openapi generate get_processor_name --filename=./tests/server-cpu/cpu.py
```

### Multiple functions in python file

1. Please check [Python file](tests/generator-calculator/calculator.py)

1. Run below command to generate yaml file and start server

```
cms openapi generate --filename=./tests/generator-calculator/calculator.py --all_functions
```

```
cms openapi generate server start ./tests/generator-calculator/calculator.py
```

### Function(s) in python class file

1. Please check [Python file](tests/generator-testclass/calculator.py)

1. Run below command to generate yaml file and start server

```
cms openapi generate --filename=./tests/generator-testclass/calculator.py --import_class"
```

```
cms openapi generate server start ./tests/generator-testclass/calculator.py
```

### Uploading data

Code to handle uploads is located in cloudmesh-openapi/tests/generator-upload. The code snippet in uploadexample.py and the specification in uploadexample.yaml can be added to existing projects by adding the `--enable_upload` flag to the `cms openapi generate` command. The web service will be able to retrieve the uploaded file from ~/.cloudmesh/upload-file/. 

#### Upload example

This example shows how to upload a CSV file and how the web service can retrieve it.

First, generate the OpenAPI specification and start the server

```
cms openapi generate print_csv2np --filename=./tests/generator-upload/csv_reader.py --enable_upload
cms openapi server start ./tests/generator-upload/csv_reader.yaml
```

Next, navigate to localhost:8080/cloudmesh/ui. Click to open the /upload endpoint, then click 'Try it out.' Click to choose a file to upload, then upload tests/generator-upload/np_test.csv. Click 'Execute' to complete the upload.

To access what was in the uploaded file, click to open the /print_csv2np endpoint, then click 'Try it out.' Enter np_test.csv in the field that prompts for a filename, and then click Execute to view the numpy array defined by the CSV file.

### Downloading data

Always the same

abc.txt <- /data/xyz/klmn.txt

### Merge openapi's

```
merge [APIS...] - > single.yaml
```

### Google

After you create your google cloud account, it is recommended to download and install Google's [Cloud SDK](https://cloud.google.com/sdk/docs/quickstarts).
This will enable CLI. Make sure you enable all the required services. 

For example:

`gcloud services enable servicemanagement.googleapis.com`D
`gcloud services enable endpoints.googleapis.com`

and any other services you might be using for your specific Cloud API function. 



### AWS

* Jonathan

### Azure

Using the Azure Computer Vision AI service, you can describe, analyze and/ or get tags for a locally stored image or you can read the text from an image or hand-written file.

#### Prerequisite for setting up Azure ComputerVision AI service

* Azure subscription. If you don't have one, create a [free account](https://azure.microsoft.com/try/cognitive-services/) before you continue further.
* Create a Computer Vision resource and get the COMPUTER_VISION_SUBSCRIPTION_KEY and COMPUTER_VISION_ENDPOINT. Follow [instructions](https://docs.microsoft.com/en-us/azure/cognitive-services/cognitive-services-apis-create-account?tabs=singleservice%2Cunix) to get the same.
* Install following Python packages in your virtual environment:
  * requests
  * PillowD
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
  `cms openapi server stop azure-ai-text-function`  D

### Openstack

* Jagadesh (cloudmesh)



### Oracle

* Prateek




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

D
## Pytests for Scikit learn tests.

* Generate the .py for the Scikit learn module woth file reading capabilities

  pytest -v --capture=no tests/Scikitlearn_tests/test_06c_sklearngeneratortest.py

* Running Pytests for the LinearRegression.py generated from 6d pytest

## Test 

The following table lists the different test we have, we provide additional information for the tests in the test directory ina README file. Summaries are provided bellwo the table


| Test   | Short Description  | Link  |
| --- | --- | --- | 
| Generator   | Bla Bla  | Link  |

Generator:

> This is a paragraph describing what the test is supposed to do can be short
> another line


{tests}
