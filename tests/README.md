# How to write and run test case for OpenAPI 

## This document will explain how to validate if openapi is generated correctly and server start and stop working correctly

### We have create a framework class which has below basic test case functions

Framework file is present under tests/lib named as generator_test.py

#### Below test cases are related to generator API

1. Create a build folder and copy py file into it. Build sub folder will created where test py file present.
1. It will call generator generate function to generate Yaml file inside build folder
1. It will check if generated YMAL file syntax is correct or not.
1. It will check if number of function generated in YMAL is same as py file.
1. Delete the build folder.

#### Two test cases are related to server API

1. It will start server
1. It will stop server

### How to create test case


1. If you creating new Open API , then inside tests folder you have to commit your working py and yaml files.
1. Create new function for test case where py and yaml located. Example (test_01_generator)
1. We have already created test cases function file for generator-calculator name as test_01_generator.py. Please check this file.
1. Copy the contains of test_01_generator.py and paste inside your test py file.
1. Change startservercommand and filename variables value accordingly to your use case.
1. Change some of parameters of constructor of GeneratorBaseTest class. 
1. if your py file has a class then.
```bash
 gen= GeneratorBaseTest(filename,False,True)
```
1. if your py file has functions then 
```bash
 gen= GeneratorBaseTest(filename,True,False)
```
1. First boolean flag in GeneratorBaseTest for --all_functions and second flag is for --import_class
1. If you need to write more test cases based on your requirement, check order of test case and write accordingly.

### How to run test case

Below command can use to run your case. Make sure your current directory is cloudmesh-openapi.

```bash
$ how do you call this
pytest -v --capture=no tests/generator-calculator/test_01_generator.py
```


## Below are test case files

1. generator-calculator and file name is test_01_generator.py
1. generator-testclass and file name is test_02_generator.py
1. server-cpu and file name is test_03_generator.py
1. server-cms and file name is test_04_generator.py


<!--## test_001_registry.py

descript what this do

```bash
$ how do you call this
cms set filename="./tests/server-cpu/cpu.yaml"
pytest -v --capture=no tests/test_03_generator.py
cms set filename="./tests/server-sampleFunction/sampleFunction.yaml"
pytest -v --capture=no tests/test_03_generator.py
```

deprecated
examples
generator
generator-calculator
generator-printerclass
generator-testclass
server-class
server-cms
server-cms-simple
server-cpu
server-sample
server-sampleFunction
textanalysis-example-text
__init__.py
README.md
test_001_registry.py  Falconi
test_03_generator.py  jonthan
test_010_generator.py jonthan
test_011_generator_cpu.py prateek
test_012_generator_calculator.py prateek
test_020_server_manage.py ishan
test_server_cms_cpu.py andrew-->
