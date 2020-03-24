# Cloudmesh OpenAPI Merge


[![image](https://img.shields.io/travis/TankerHQ/cloudmesh-openapi.svg?branch=master)](https://travis-ci.org/TankerHQ/cloudmesn-openapi)

[![image](https://img.shields.io/pypi/pyversions/cloudmesh-openapi.svg)](https://pypi.org/project/cloudmesh-openapi)

[![image](https://img.shields.io/pypi/v/cloudmesh-openapi.svg)](https://pypi.org/project/cloudmesh-openapi/)

[![image](https://img.shields.io/github/license/TankerHQ/python-cloudmesh-openapi.svg)](https://github.com/TankerHQ/python-cloudmesh-openapi/blob/master/LICENSE)

## Prerequisits

```bash
$ pip install cloudmesh.openapi
```

## Overview



## Install

TBD

## Usage

TBD


## Pytests

How to run them 

TBD

## Examples

TBD

??????

### One function in function.py

cms openapi3 generate function.py -> function.yaml


function.py

```
def a(x:int, y:int):
return 1
```

### Multiple functions in function.py

 
cms openapi3 generate function.py [--names=a,c] -> function.yaml
 #dont include b

cms openapi3 generate function.py -> function.yaml

function.py

functions = list all functions in file

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

abc.txt -> /data/xyz/klmn.txt

### Downloading data

Always the same

abc.txt <- /data/xyz/klmn.txt

### Merge openapi's

merge [APIS...] - > single.yaml


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

spec -> function.py with typing -> generator -> yaml

spec -> yaml

cms generate --sckitlearn --name=abc --function="LinearRegression().fit" -> LinearRegression_fit.yaml

cms generate --sckitlearn --name=abc --function="LinearRegression().predict,LinearRegression().fit"  -> LinearRegression_abc.yaml

cms generate --sckitlearn --class="LinearRegression"  -> LinearRegression.yaml

	* integrate all methods in the class



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



