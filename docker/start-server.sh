#!/bin/sh
cd /usr/local/code/cloudmesh-openapi
cms openapi server start ./tests/generator-calculator/calculator.yaml calculator --directory=./tests/generator-calculator/
