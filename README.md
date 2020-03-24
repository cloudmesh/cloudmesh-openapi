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

TBO


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



