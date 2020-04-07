# Cloudmesh OpenAPI Merge

> **Note:** The README.md page is outomatically generated, do not edit it.
> To modify  change the content in
> <https://github.com/cloudmesh/cloudmesh-openapi/blob/master/README-source.md>
> and use `bin/readme.py`. This note will be moved to the end of this document
> at a later stage in the project, till everyone knows about it.
>  THe source uses { } for using text in single brackets


[![image](https://img.shields.io/travis/TankerHQ/cloudmesh-openapi.svg?branch=master)](https://travis-ci.org/TankerHQ/cloudmesn-openapi)

[![image](https://img.shields.io/pypi/pyversions/cloudmesh-openapi.svg)](https://pypi.org/project/cloudmesh-openapi)

[![image](https://img.shields.io/pypi/v/cloudmesh-openapi.svg)](https://pypi.org/project/cloudmesh-openapi/)

[![image](https://img.shields.io/github/license/TankerHQ/python-cloudmesh-openapi.svg)](https://github.com/TankerHQ/python-cloudmesh-openapi/blob/master/LICENSE)


## Prerequisits

* Python 3.7.4 or newer, we use 3.8.2
* updated version of pip greater than 20.x

## Instalation

###  User instalation

Users can install the code with

```bash
$ pip install cloudmesh-openapi
```

Make sure you use a python venv before installing

### Developeres

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


## Manual

```bash
Usage:
    openapi generate FUNCTION --filename=FILENAME
                               [--baseurl=BASEURL]
                               [--yamlfile=YAML]
                               [--yamldirectory=DIRECTORY]
                               [--fclass]
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
    openapi sklearn generate FUNCTION

Arguments:
    DIR       The directory of the specifications
    FILE      The specification
    FUNCTION  The name for the function or class

Options:
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


  openapi sklearn generate sklearn.linear_model.LogisticRegression
      Generates the

  openapi generate FUNCTION --filename=FILENAME
                               [--baseurl=BASEURL]
                               [--yamlfile=YAML]
                               [--yamldirectory=DIRECTORY]
                               [--fclass]
                               [--all_functions]
                               [--verbose]
      TODO: add description

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

How to run them 

TBD

## Examples

TBD

??????

### One function in function.py

```
cms openapi3 generate function.py -> function.yaml
```

Bugs: docstring is not yet in the yaml from the function

function.py

```
def a(x:int, y:int):
return 1
```

### Multiple functions in function.py

```
cms openapi3 generate function.py [--names=a,c] -> function.yaml
```
```
 #dont include b

cms openapi3 generate function.py -> function.yaml

function.py

functions = list all functions in file
```

```
def a(x:int, y:int):
	r = b(x,y)
	return 3

def b(x:int, y:int):
	return 1

def c(x:int, y:int):
	return 1
```

### Uploading data

Always the same
so we can preimplement

```
abc.txt -> /data/xyz/klmn.txt
```

### Downloading data

Always the same

```
abc.txt <- /data/xyz/klmn.txt
```

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


## OLD DOCUMENTATION DO NOT MDDIFY






## Usage

The manual page for the `cms openapi` command  is

```
cms openapi merge [SERVICES...] [--dir=DIR]
cms openapi list [--dir=DIR]
cms openapi description [SERVICES...] [--dir=DIR]
cms openapi md FILE [--indent=INDENT]
```


You need to have the yaml file in the current directory and execute
this program in this directory

An example for yaml files are provided in 

* <https://github.com/cloudmesh-community/nist/tree/master/spec>

Please note that the spec directory is containing openapi specifications that
may not yet completed or are actively worked on. You are invited to participate.
You can download some examples, as well as the `.header.yaml` file you will need
with for example curl

Once you have `organization.yaml`, `user.yaml` `timestap.yaml` and `.header
yaml` in your directory you can say

Please note that this script does not yet rewrite the `$ref`
appropriately, but if you like to help you can do so.

## Example use

Here we demonstrate an example use

First we download some OpenAPI examples:

```bash
mkdir example
cd example
$ export SPEC=https://raw.githubusercontent.com/cloudmesh-community/nist/master/spec
$ curl $SPEC/organization.yaml > organization.yaml
$ curl $SPEC/user.yaml > user.yaml
$ curl $SPEC/timestamp.yaml > timestamp.yaml
$ curl $SPEC/.header.yaml > .header.yaml

```

# Cloudmehs 


# OLD DOCUMENTATION

Now let us look at the descriptions with 

```bash
$ cms openapi description organization user timestamp
```

To create a merged specification you can use 

```bash
$ cms openapi merge organization user timestamp
```

To create a markdown representation you can use 

```bash
$ cms openapi md user
```

Note that for the markdown specification only one service is specified.



