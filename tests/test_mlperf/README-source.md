# MLPerf Tests

[MLperf](http://mlperf.org) [@www-mlperf] provides "fair and useful benchmarks for measuring
training and inference performance of ML hardware, software, and
services"


In this benchmark we will

1. Deploy MLPerf on the system
2. Use functions that run a number of tests as inout to the OpenAPI Gnerator
3. From these functions we run our OpenAPI generator to create a service
   that allows to run the MLperf examples through a Web service with
   http calls
4. Test out the created functions by running selected example invocations
5. Report the time it takes to run these examples
6. Provide a Makefile or python script that allows us to conveniently
   cun these tests

## Deployment

Describe how to deploy

### Reports for running the tests on Machines

Provide summary information about teh runtime
Provide details do checked in results in the [results](results) directory

### Local Output

All output is written into a `~/.cloudmesh/dest/benchmark/mlperf` folder
which can be removed after the test is completed. In the results folder
we also find a copy of the OpenAPI YAML file that is generated with the
cenerator. This file can also be used to compare the generated output.


## Selected Benchmarks

Describe which benchmarks were selected

## Functions

Short description aboutthe functions that have been defined

## OpeanAPI

Describe where to find the generated functions
Link th=o wher ethe open api is created in the

## How to run individual tests

Describe how to run indific=dual Tests

## Benchmarks

Links to benchmarks that are listed in the [results](results) directory

## References


