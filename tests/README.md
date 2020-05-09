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
$ how do you call this you can add -x to stop pytest when first test failed
pytest -v  --capture=no tests/generator-calculator/test_01_generator.py
```

### Run test case with CSV command enabled

```bash
$ how do you call this , you can add -x to stop pytest when first test failed
pytest -v  --capture=no tests/generator-calculator/test_01_generator.py  | fgrep '# cvs'
```


## Below are test case files

Generator-calculator and file name is test_01_generator.py

```
pytest -v  --capture=no tests/generator-calculator/test_01_generator.py
```

Generator-testclass and file name is test_02_generator.py

```
pytest -v --capture=no tests/generator-testclass/test_02_generator
```

Server-cpu and file name is test_03_generator.py

```
pytest -v  --capture=no tests/server-cpu/test_03_generator
```

Server-cms and file name is test_04_generator.py

```
pytest -v  --capture=no tests/server-cms/test_04_generator
```

Generator and file name is test_05_generator.py

```
pytest -v --capture=no tests/generator/test_05_generator
```

Azure AI Image Function is test_06_generator.py

```bash
pytest -v --capture=no tests/generator_azureai/test_06_generator
```

Azure AI Text Function is test_07_generator.py

```bash
pytest -v --capture=no tests/generator_azureai/test_07_generator
```

Natural Language Analysis Generator Tests are run from test_generator_natural_language.py

```bash
pytest -v --capture=no  ./tests/test_generator_natural_language.py::TestGenerator
```

This test will generate an OpenAPI spec for the natural-lang-analysis.py file located in the generator-natural-lang
directory. If the above command is copied and pasted to run in the terminal it will do the following.

1. Generate a yaml file
2. Verify the spec has all the functions that are available in the natural-lang-analysis.py file
3. Start a server hosting the openAPI spec
4. Run a call against the sentiment analysis and translation endpoint for each available cloud service (Google/Azure) and verify it was successful.
5. Stop the service

**Results for Natural Language Tests**

| Attribute        | Value                                                                                            |
|------------------|--------------------------------------------------------------------------------------------------|
| cpu_count        | 4                                                                                                |
| mem.active       | 2.0 GiB                                                                                          |
| mem.available    | 2.1 GiB                                                                                          |
| mem.free         | 148.8 MiB                                                                                        |
| mem.inactive     | 2.0 GiB                                                                                          |
| mem.percent      | 73.2 %                                                                                           |
| mem.total        | 8.0 GiB                                                                                          |
| mem.used         | 4.8 GiB                                                                                          |
| mem.wired        | 2.8 GiB                                                                                          |
| platform.version | 10.14.1                                                                                          |
| python           | 3.8.1 (v3.8.1:1b293b6006, Dec 18 2019, 14:08:53)                                                 |
|                  | [Clang 6.0 (clang-600.0.57)]                                                                     |
| python.pip       | 20.0.2                                                                                           |
| python.version   | 3.8.1                                                                                            |
| sys.platform     | darwin                                                                                           |
| uname.machine    | x86_64                                                                                           |
| uname.node       | Andrews-MacBook-Pro.local                                                                        |
| uname.processor  | i386                                                                                             |
| uname.release    | 18.2.0                                                                                           |
| uname.system     | Darwin                                                                                           |
| uname.version    | Darwin Kernel Version 18.2.0: Fri Oct  5 19:41:49 PDT 2018; root:xnu-4903.221.2~2/RELEASE_X86_64 |
| user             | andrewgoldfarb                                                                                   |


| Name                                                    | Status   |   Time | Start               | tag     | Node                      | User           | OS     | Version   |
|---------------------------------------------------------|----------|--------|---------------------|---------|---------------------------|----------------|--------|-----------|
| generator_test/copy_py_file                             | ok       |  0.003 | 2020-05-09 06:33:47 | openapi | Andrews-MacBook-Pro.local | andrewgoldfarb | Darwin | 10.14.1   |
| generator_test/generate                                 | ok       |  2.601 | 2020-05-09 06:33:47 | openapi | Andrews-MacBook-Pro.local | andrewgoldfarb | Darwin | 10.14.1   |
| generator_test/read_spec                                | ok       |  0.012 | 2020-05-09 06:33:49 | openapi | Andrews-MacBook-Pro.local | andrewgoldfarb | Darwin | 10.14.1   |
| generator_test/start_service                            | ok       |  1.864 | 2020-05-09 06:33:49 | openapi | Andrews-MacBook-Pro.local | andrewgoldfarb | Darwin | 10.14.1   |
| test_generator_natural_language/test_run_analyze_google | ok       |  0.67  | 2020-05-09 06:33:51 | openapi | Andrews-MacBook-Pro.local | andrewgoldfarb | Darwin | 10.14.1   |
| test_generator_natural_language/test_run_analyze_azure  | ok       |  0.58  | 2020-05-09 06:33:52 | openapi | Andrews-MacBook-Pro.local | andrewgoldfarb | Darwin | 10.14.1   |
| generator_test/stop_server                              | ok       |  2.095 | 2020-05-09 06:33:52 | openapi | Andrews-MacBook-Pro.local | andrewgoldfarb | Darwin | 10.14.1   |
| generator_test/delete_file                              | ok       |  0.002 | 2020-05-09 06:33:54 | openapi | Andrews-MacBook-Pro.local | andrewgoldfarb | Darwin | 10.14.1   |

## TODO DESCRIBE WHAT THEY DO


cache-scikitlearn
deprecated
examples
generator
generator-azureai
generator-calculator
generator-printerclass
generator-testclass
generator-upload
image-analysis
lib
Scikit-learntestfiles
Scikitlearn_tests
server-cms
server-cms-simple
server-cpu
server-sample
server-sampleFunction
test_mlperf
textanalysis-example-text
__init__.py
README.md
test_001_registry.py
test_03_generator.py
test_010_generator.py
test_011_generator_cpu.py
test_012_generator_calculator.py
test_015_generator_azureai.py
test_020_server_manage.py
test_server_cms_cpu.py
util.py


THIS WAS HERE BEFORE

## test_001_registry.py

This test has 5 test functions

1. test_registry_add
2. test_registry_list_name
3. test_registry_list
4. test_registry_delete
5. test_benchmark

Test 1 calls registry and adds to the registry. If successful prints 'PASSED'

Test 2 calls registry and prints ONLY the server specified in filename.

Test 3 calls registry and print list for ALL servers in registry.

Test 4 calls registry and deletes entry for filename.

Test 5 runs benchmark test on registry.

### How to call this

```bash
cms set filename="./tests/server-cpu/cpu.yaml"
pytest -v --capture=no tests/test_001_registry.py
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
