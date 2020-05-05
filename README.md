# Cloudmesh OpenAPI Merge


[![image](https://img.shields.io/travis/TankerHQ/cloudmesh-openapi.svg?branch=master)](https://travis-ci.org/TankerHQ/cloudmesh-openapi)
[![image](https://img.shields.io/pypi/pyversions/cloudmesh-openapi.svg)](https://pypi.org/project/cloudmesh-openapi)
[![image](https://img.shields.io/pypi/v/cloudmesh-openapi.svg)](https://pypi.org/project/cloudmesh-openapi/)
[![image](https://img.shields.io/github/license/TankerHQ/python-cloudmesh-openapi.svg)](https://github.com/TankerHQ/python-cloudmesh-openapi/blob/master/LICENSE)



> **Note:** The README.md page is outomatically generated, do not edit it.
> To modify  change the content in
> <https://github.com/cloudmesh/cloudmesh-openapi/blob/master/README-source.md>
> Curley brackets must use two in README-source.md


## Prerequisits

* We use recommend Python 3.8.2 Python or newer.
* We recommend pip version 20.0.2 or newer
* We recommend that you use a venv (see developer install)
* MongoDB installed as regular program not as service

We have not checked if it works on older versions.

## Instalation

Make sure that cloudmesh is properly installed on your machine and you
have mongodb setup to work with cloudmesh.

More details to setting up mongo can be found in the

* [Cloudmesh Manual](https://cloudmesh.github.io/cloudmesh-manual/installation/install.html)

###  User Instalation

Make sure you use a python venv before installing. Users can install the
code with

```bash
$ pip install cloudmesh-openapi
```


### Developere Instalation

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
convenience we include the manual page later on in this documenth.

## Usage

After that the first step is to find an Open Api 3 compliant spec that
you are comfortable using or to create one yourself. If you are not
familiar with Open API specs, it is suggested to go read up on those
before using this command.

Create a YAML file in your project directory for the Open Api
specification

Here is an example spec that can be used:

```yaml
openapi: 3.0.0
info:
  title: cpu
  description: A simple service to get cpuinfo as an example of using OpenAPI 3.0
  license:
    name: Apache 2.0
  version: 0.0.1

servers:
  - url: http://localhost:8080/cloudmesh

paths:
  /cpu:
    get:
      summary: Returns cpu information of the hosting server
      operationId: cpu.get_processor_name
      responses:
        '200':
          description: cpu info
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/cpu"

components:
  schemas:
    cpu:
      type: "object"
      required:
        - "model"
      properties:
        model:
          type: "string"
```

For this spec to work it is necessary to also create a function called
`get_processor_name` in a cpu.py file in the same directory. Once that
has been saved you have all the parts to now spin up you API using
cloudmesh.

Take not of the working directory name where you store the YAML and
python files. To start a server to host this API you must run the
`server start` function and pass in the relative, or absolute, location
of the API specification as a parameter.

`cms openapi server start ./cpu.yaml`

This will output the serer name, PID, URL, and spec location to the
terminal.

Verify that your server has successfully spun up by running `ps` and
look for the PID value in the list. If it is not in the list the server
did not start correctly.

You can also ping the returned URL to see if you get a successful
response.

### Generating API Endpoints

The openapi command can also generate Open API specs from python
functions using `cms openapi generate`. Once you have generated an API
spec using cloudmesh follow through the same process as above except
with your newly generated endpoint to make the API accessible.

The data returned from a generated endpoint is returned in JSON format.

### Endpoint Registry

A mongodb registry allows you to store information about started servers
and API endpoints generated by the openapi command. You can use a tool
like Robo 3T to add a GUI to view the contents of the database to verify
that your interactions with the database are working.

There are add, delete, rename, and list functions for the registry command.

`cms openapi register`

### Stopping Servers

When it is necessary to stop a server hosting an endpoint generated or
start using cloudmesh use the stop command and passing the name of the
server as a parameter. In the context of the earlier example the command
is:

`cms openapi server stop cpu`

## Manual

```bash
Usage:
openapi generate [FUNCTION] --filename=FILENAME
                         [--serverurl=SERVERURL]
                         [--yamlfile=YAML]
                         [--import_class]
                         [--all_functions]
                         [--verbose]
openapi server start YAML [NAME]
              [--directory=DIRECTORY]
              [--port=PORT]
              [--server=SERVER]
              [--host=HOST]
              [--verbose]
              [--debug]
              [--fg]
              [--os]
openapi server stop NAME
openapi server list [NAME] [--output=OUTPUT]
openapi server ps [NAME] [--output=OUTPUT]
openapi register add NAME ENDPOINT
openapi register filename NAME
openapi register delete NAME
openapi register list [NAME] [--output=OUTPUT]
openapi TODO merge [SERVICES...] [--dir=DIR] [--verbose]
openapi TODO doc FILE --format=(txt|md)[--indent=INDENT]
openapi TODO doc [SERVICES...] [--dir=DIR]
openapi sklearn generate FUNCTION MODELTAG
openapi sklearn upload --filename=FILENAME

Arguments:
FUNCTION  The name for the function or class
MODELTAG  The arbirtary name choosen by the user to store the Sklearn trained model as Pickle object
FILENAME  Path to python file containing the function or class
SERVERURL OpenAPI server URL Default: https://localhost:8080/cloudmesh
YAML      Path to yaml file that will contain OpenAPI spec. Default: FILENAME with .py replaced by .yaml
DIR       The directory of the specifications
FILE      The specification

Options:
--import_class         FUNCTION is a required class name instead of an optional function name
--all_functions        Generate OpenAPI spec for all functions in FILENAME
--debug                Use the server in debug mode
--verbose              Specifies to run in debug mode
                     [default: False]
--port=PORT            The port for the server [default: 8080]
--directory=DIRECTORY  The directory in which the server is run
--server=SERVER        The server [default: flask]
--output=OUTPUT        The outputformat, table, csv, yaml, json
                     [default: table]
--srcdir=SRCDIR        The directory of the specifications
--destdir=DESTDIR      The directory where the generated code
                     is placed

Description:
This command does some useful things.

openapi TODO doc FILE --format=(txt|md|rst) [--indent=INDENT]
Sometimes it is useful to generate teh openaopi documentation
in another format. We provide fucntionality to generate the
documentation from the yaml file in a different formt.

openapi TODO doc --format=(txt|md|rst) [SERVICES...]
Creates a short documentation from services registered in the
registry.

openapi TODO merge [SERVICES...] [--dir=DIR] [--verbose]
Merges tow service specifications into a single servoce
TODO: do we have a prototype of this?


openapi sklearn sklearn.linear_model.LogisticRegression
Generates the

openapi generate [FUNCTION] --filename=FILENAME
                         [--serverurl=SERVERURL]
                         [--yamlfile=YAML]
                         [--import_class]
                         [--all_functions]
                         [--verbose]
Generates an OpenAPI specification for FUNCTION in FILENAME and
writes the result to YAML. Use --import_class to import a class
with its associated class methods, or use --all_functions to 
import all functions in FILENAME. These options ignore functions
whose names start with '_'

openapi server start YAML [NAME]
              [--directory=DIRECTORY]
              [--port=PORT]
              [--server=SERVER]
              [--host=HOST]
              [--verbose]
              [--debug]
              [--fg]
              [--os]
TODO: add description

openapi server stop NAME
stops the openapi service with the given name
TODO: where does this command has to be started from

openapi server list [NAME] [--output=OUTPUT]
Provides a list of all OpenAPI services.
TODO: Is thhis command is the same a register list?

openapi server ps [NAME] [--output=OUTPUT]
list the running openapi service

openapi register add NAME ENDPOINT
Openapi comes with a service registry in which we can register
openapi services.

openapi register filename NAME
In case you have a yaml file the openapi service can also be
registerd from a yaml file

openapi register delete NAME
Deletes the names service from the registry

openapi register list [NAME] [--output=OUTPUT]
Provides a list of all registerd OpenAPI services


```



## Pytests

Please follow [Pytest Information](tests/README.md) document for pytests related information

## Examples

### One function in python file

1. Please check [Python file](tests/server-cpu/cpu.py).

1. Run below command to generate yaml file

```
cms openapi generate get_processor_name --filename=./tests/server-cpu/cpu.py
```

### Multiple functions in python file

1. Please check [Python file](tests/generator-calculator/calculator.py)

1. Run below command to generate yaml file

```
cms openapi generate --filename=./tests/generator-calculator/calculator.py --all_functions
```

### function(s) in python class file

1. Please check [Python file](tests/generator-testclass/calculator.py)

1. Run below command to generate yaml file

```
cms openapi generate --filename=./tests/generator-testclass/calculator.py --import_class"
```


### Uploading data

Please follow [Python file example](tests/generator-upload/uploadexample.py) and [Yaml file example](tests/generator-upload/uploadexample.yaml)

Currently you need to manually add yaml code to your yaml file which was generated by generator. 

#### Steps

Copy below code contains to your yaml file

```
/upload:
    post:
      summary: upload a file
      operationId: uploadexample.upload
      requestBody:
        content:
          multipart/form-data:
            schema:
              type: object
              properties:
                upload:
                  type: string
                  format: binary
      responses:
        '200':
          description: "OK"
          content:
            text/plain:
              schema:
                type: string
```

Copy below code contains to your py file

```
from cloudmesh.openapi.registry.fileoperation import FileOperation

def upload() -> str:

    filename=FileOperation().file_upload()
    return filename
```

Start server , now you will see upload api and when you upload any file, it will go to "/.cloudmesh/upload-file" folder
 

### Downloading data

Always the same

abc.txt <- /data/xyz/klmn.txt

### Merge openapi's

```
merge [APIS...] - > single.yaml
```

### Google

* Andrew

### AWS

* Jonathan

### Azure

* Andrew

### Openstack

* Jagadesh (cloudmesh)



### Oracle

* Prateek




## sckit learn

```
--output=yaml
--output=function

generatie a function by hand, where is the documentation, where are
the links ???

This motivates doing it automatically.

def param(name, type, description):
	t1 = f":param {name}: {description}"
    t2 = f":type {type}"
	return t



spec -> function.py with typing -> generator -> yaml

spec -> yaml

cms generate --sckitlearn --name=abc --function="LinearRegression().fit" -> LinearRegression_fit.yaml

cms generate --sckitlearn --name=abc --function="LinearRegression().predict,LinearRegression().fit"  -> LinearRegression_abc.yaml

cms generate --sckitlearn --class="LinearRegression"  -> LinearRegression.yaml

	* integrate all methods in the class
```

