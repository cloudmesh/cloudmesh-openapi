# Benchmarking Multi-Cloud Auto Generated AI Services

NOTE:
> This document is maintained at:
>
> * <https://github.com/cloudmesh/cloudmesh-openapi/blob/main/paper/_index.md>
>

[Gregor von Laszewski](https://laszewski.github.io), 
Richard Otten,
[Anthony Orlowski](https://github.com/aporlowski), [fa20-523-310](https://github.com/cybertraining-dsc/fa20-523-310/), 
[Caleb Wilson](https://github.com/calewils), [fa20-523-348](https://github.com/cybertraining-dsc/fa20-523-348/), 
Vishwanadham Mandala, [fa20-523-325](https://github.com/cybertraining-dsc/fa20-523-325/) 

Corresponding author: laszewski@gmail.com

[Edit](https://github.com/cybertraining-dsc/fa20-523-348/blob/main/project/project.md)

{{% pageinfo %}}

## Abstract

In this wor we are benchmarking auto generated cloud REST services on
various clouds. In todays application scientist want to share their
services with a wide number of collegues while not only offereing the
services as bare metal programs, but exposing the functionality as a
software as a service. For this reason a tool has been debveloped that
takes a regular python function and converts it automatically into a
secure REST service. We will create a number of AI REST services while
using examples from ScikitLearn and benchmark the execution of the
resulting REST services on various clouds. The code will be
accompanied by benchmark enhanced unit tests as to allow replication
of the test on the users computer. A comparative study of the results
is included in our evaluation.

Contents

{{< table_of_contents >}}

{{% /pageinfo %}}

**Keywords:** cloudmesh, AI service, REST, multi-cloud

## 1. Introduction

We will develop benchmark tests that are pytest replications of
Sklearn artificial intelligent alogrithms. These pytests will then be
ran on different cloud services to benchmark different statistics on
how they run and how the cloud performs. The team will obtain cloud
service accounts from AWS, Azure, Google, and OpenStack. To deploy the
pytests, the team will use Cloudmesh and its Openapi based REST
services to benchmark the performance on different cloud
services. Benchmarks will include components like data transfer time,
model train time, model prediction time, and more. The final project
will include scripts and code for others to use and replicate our
tests. The team will also make a report consisting of research and
findings. So far, we have installed the Cloudmesh OpenAPI Service
Generator on our local machines. We have tested some microservices,
and even replicated a Pipeline Anova SVM example on our local
machines. We will repeat these processes, but with pytests that we
build and with cloud accounts.

## 2. Background and Related Research

### 2.1 Cloudmesh

Cloudmesh [^1][^4] is a service that enables users to access multi-cloud
environments easily. Cloudmesh is an evolution of previous tools that
have been used by many of users. Cloudmesh makes interacting with
clouds easy by creating a service mashup to access common cloud
services across numerous cloud platforms. Cloudmesh contains a
sophisticated command shell, a database to store jason objects
representing virtual machines, storage and a registry of REST
services [^3]. CLoudmesh has a sophisticated plugin concept that is easy to
use and leveraged python namespaces while being able to integrate
plugins form different source code directories [^2]. Instalation of
cloudmesh is available for macOS, Linux, Windows, and Rasbian [^5].

### 2.2 REST

REST is an acronym for representational state transfer. REST often
uses the HTTP protocol for the CRUD functions which create, read,
update, and delete resources. It is important to note that REST is not
a standard, but it is a software architectural style for building
network services. When a part of the HTTP protocol, REST has the
methods of GET, PUT, POST, and DELETE. These methods are used to
implement the CRUD functions on collections and items that REST
introduces [^Cloud-Computing].

* **Collection of resources** [^Cloud-Computing]: Assume the URI,
  http://.../resources/, identifies a collection of resources. The
  following CRUD functions would be implemented:

  * **GET**: List the URIs and details about the collection’s items. 
  * **PUT**: Replace the collection with a different collection.
  * **POST**: Make a new entry in the collection. The operation returns
    new entry’s URI and assigns it automatically.
  * **DELETE**: Delete the collection. 
		
* **Single Resource** [^Cloud-Computing]: Assume the URI,
  http://.../resources/item58, identifies a single resource in a
  collection. The following CRUD functions would be implemented:
	
  * **GET**: Fetch a representation of the item in the collection,
    extracted in the appropriate media type.
  * **PUT**: Replace the item in the collection. If the item does not
	exist, then create the item.
  * **POST**: Typically, not used. Treat the item as a collection and
	make a new entry in it.	
  * **DELETE**: Delete the item in the collection.
	
Because REST has a defined structure, there are tools that manage
programming to REST specifications.  Here are different categories
[^Cloud-Computing]:

* **REST Specification Frameworks**: Frameworks to define REST service
  specifications for generating REST services in a language and
  framework independently, include: Swagger 2.0 [^Swagger2.0],
  OpenAPI 3.0 [^OpenAPI3.0], and RAML [^RAML].
* **REST programming language support**: Tools and services for
  targeting specific programming languages, include: Flask Rest
  [^Flask-Rest], Django Rest Services [^Django-Rest-Services]
* **REST documentation-based tools**: These tools document REST
  specifications. One such tool is Swagger [^Swagger]
* **REST design support tools**: These tools support the design
  process in developing REST services while extracting on top of the
  programming languages.  These tools also define reusable to create
  clients and servers for particular targets.These tools include
  Swagger [^Swagger] , additional swagger tools are available at
  OpenAPI Tools [^OpenAPI-Tools] to generate code from OpenAPI
  specifications [^OpenAPI-Specifications]

### 2.3 VM Cloud providers

Cloud computing providers offer their customers on-demand self-service
computing resources that are rapidly elastic and accessible via broad
network access [^NIST-SP-800-145]. They accomplish this through the
economies of scale achieved by resource pooling (serving multiple
customers on the same hardware), and utilizing measured services for
fine grained customer billing [^NIST-SP-800-145]. Examples of cloud
providers include Amazon Web Services, Microsoft Azure, Google Cloud
Platform, Oracle’s OpenStack based providers, and more.  Cloud
providers offer these resources in multiple service models including
infrastructure as a service, platform as a service, software as a
service, and, recently, function as a service. [^NIST-SP-800-145].
These providers are rapidly offering new platforms and services
ranging from bare-metal machines to AI development platforms like
Google’s TensorFlow Enterprise platform [^tensorflow-enterprise], and
AI services such as Amazon’s text-to-speech service [^polly].

Customers can take advantage of cloud computing to reduce overhead
expenses, increase their speed and scale of service deployment, and
reduce development requirements by utilizing providers’ platforms or
services. For example, customers’ developing AI systems can utilize
clouds to handle big data inputs for which private infrastructure
would be too costly or slow to implement. However, having multiple
competing cloud providers leads to situations where service
availability, performance, and cost may vary greatly. Customer’s must
navigate these heterogeneous solutions to meet their business needs
while avoiding provider lock-in and managing organizational risk. This
may require utilizing multiple cloud providers to meet various
objectives.

### 2.4 Containers and Microservices

TBD

## 3. Architecture

TBD

## 4. Benchmarks

### 4.1. Algorithms and Datasets

This project uses a number of simple example algorithms and
datasets. We have chosen to use the once included in Scikit Learn as
they are widel known and can be used by others to replicate our
benchmarks easily. Nevertheless, it will be possible to integrate
easily other data sources, as well as algorithms due to the generative
nature of our base code for creating REST services.

Within Skikit Learn we have chosen the following examples:

* **Pipelined ANOVA SVM**: A code thet shows a pipeline running
  successively a univariate feature selection with anova and then a
  SVM of the selected features [^6].

### 4.2. Cloud Providers

#### AWS

#### Azure

#### Google

#### OpenStack

#### Oracle

#### Raspberry Pi Cluster

### 4.3. Result Comparision

## 5. Conclusion

## 6. Limitations

Azure has updated their libraries and discontinued the version 4.0
Azure libraries. We have not yet identified if code changes in Azure
need to be conducted to execute our code on Azure

Idially this project will modify the code to use the new Azure library.

## APPENDIX A. - Setup 

### A.1. Deployment

The project is easy to replicate with our detailed instructions. First you must install Cloudmesh OpenAPI whihch can be done by the follwoing steps:

```
python -m venv ~/ENV3
source ~/ENV3/bin/activate 
mkdir cm
cd cm
pip install cloudmesh-installer
cloudmesh-installer get openapi 
cms help
cms gui quick
#fill out mongo variables
#make sure autinstall is True
cms config set cloudmesh.data.mongo.MONGO_AUTOINSTALL=True
cms admin mongo install --force
#Restart a new terminal to make sure mongod is in your path
cms init
```

As a first example we like to test if the deployment works by using a
number of simple commands we execute in a terminal.

```
cd ~/cm/cloudmesh-openapi

cms openapi generate get_processor_name \
    --filename=./tests/server-cpu/cpu.py

cms openapi server start ./tests/server-cpu/cpu.yaml

curl -X GET "http://localhost:8080/cloudmesh/get_processor_name" \
     -H "accept: text/plain"
cms openapi server list

cms openapi server stop cpu
```
The output will be a string containing your computer.

TODO: how does the string look like

Next you can test a more sophiticated example. Here we generate from a
python function a rest servive. We consider the following function
definition in which a float is returned as a simple integer

```
def add(x: float, y: float) -> float:
    """
    adding float and float.
    :param x: x value
    :type x: float
    :param y: y value
    :type y: float
    :return: result
    :return type: float
    """
    result = x + y

    return result
```

Once we execute the following lines in a terminal, the result of the
addition will be calculated in the REST service and it is returned as
a string.

```
cms openapi generate add --filename=./tests/add-float/add.py
cms openapi server start ./tests/add-float/add.yaml 
curl -X GET "http://localhost:8080/cloudmesh/add?x=1&y=2" -H  "accept: text/plain"
#This command returns
> 3.0
cms openapi server stop add
```

As we often also need the information as a REST service, we provide in
our next example a jsonified object specification.


```
from flask import jsonify

def add(x: float, y: float) -> str:
    """
    adding float and float.
    :param x: x value
    :type x: float
    :param y: y value
    :type y: float
    :return: result
    :return type: float
    """
    result = {"result": x + y}

    return jsonify(result)

```

The result will include a json string returned by the service.

```
cms openapi generate add --filename=./tests/add-json/add.py
cms openapi server start ./tests/add-json/add.yaml 
curl -X GET "http://localhost:8080/cloudmesh/add?x=1&y=2" -H  "accept: text/plain"
#This command returns
> {"result":3.0}
cms openapi server stop add
```

These examples are used to demonstrate the ease of use as well as the
functionality for those that want to replicate our work.

### A.2.  Pipiline ANOVA SVM

Next we demonstrate how oto run the Pipeline ANOVA example.

```
$ pwd
~/cm/cloudmesh-openapi

$ cms openapi generate PipelineAnovaSVM \
      --filename=./tests/Scikitlearn-experimental/sklearn_svm.py \
      --import_class --enable_upload

$ cms openapi server start ./tests/Scikitlearn-experimental/sklearn_svm.yaml
```

After running these commands, we opened a web user interface. In the
user interface, we uploaded the file iris data located in
~/cm/cloudmesh-openapi/tests/ Scikitlearn-experimental/iris.data

We then trained the model on this data set by inserting the name of
the file we uploaded `iris.data`. Next, we tested the model by
clicking on make_prediction and giving it the name of the file
iris.data and the parameters `5.1`, `3.5`, `1.4`, `0.2`

The response we received was `Classification: ['Iris-setosa']`

Lastly, we close the server:

```
$ cms openapi server stop sklearn_svm
```

This process can easily be replicated when we create more service
examples that we derive from existing sklearn examples. We benchmark
these tests while wrapping them into pytests and run them on various
cloud services.

### A.3. Using unit tests for Benchmarking

TODO: This section will be expanded upon

* Describe why we can unit tests
* Describe how we access multiple clouds

  ```
  cms set cloud=aws
  # run test
  cms set cloud=azure
  # run test
  ```
  
* Describe the Benchmark class from cloudmesh in one sentence and how
  we use it



## APPENDIX B. - Code Location

This is temporary and will in final be moved elsewhere. Its
conveniently for now placed on top so we can easier locate it

* github: <https://github.com/cloudmesh/cloudmesh-openapi> [^cloudmesh-openapi]
* branch: benchmark (not yet created)


## APPENDIX C. - Cloudmesh Links

We added this section so the Reader can easily find some cloudmesh
related information 
Documentation for Cloudmesh can be found at:

* <https://cloudmesh.github.io/cloudmesh-manual/> [^1]

Code for cloud mesh can be found at: 

* <https://github.com/cloudmesh/> [^2]

Examples in this paper came from the cloudmesh openapi manual which is located here: 

* <https://github.com/cloudmesh/cloudmesh-openapi> [^3].

Information about cloudmesh can be found here: 
* <https://cloudmesh.github.io/cloudmesh-manual/preface/about.html> [^4]

Various cloudmesh installations for various needs can be found here: 

* <https://cloudmesh.github.io/cloudmesh-manual/installation/install.html> [^5]

## APPENDIX D. - Plan

Thus far in the project we have familiarized ourselves with
Cloudmesh-Openapi by recreating example services on our local
machines, setup a git branch of the source project on which we will
collaborate, contributed to the paper’s background section, and
started looking for example AI analytics, like those provided at
SciKitLearn’s website. We obtained cloud service accounts from AWS, Azure,
GCP, and Chameleon Cloud, and verified Cloudmesh documentation while
applying for the cloud accounts. We registered our accounts with the Cloudmesh shell and executed VM operations using Cloudmesh.
  
Moving forward, we will develop benchmark tests in the
form of pytests that replicate the AI analytic examples.  We will each
use Cloudmesh to deploy these tests as an Openapi based REST service
and benchmark their performance on various cloud providers. Our
benchmarks will measure various components such as data transfer time,
model train time, model prediction time, etc. We will then consolidate
and report on our findings. Our final project will include a script
that utilizes the Cloudmesh shell to automate our benchmark tests so
others can replicate our work.

For an AI analytic benchmark test, one intesresting example to
replicate may be the faces recognition example using eigenfaces and
SVMs
<https://scikit-learn.org/stable/auto_examples/applications/plot_face_recognition.html#sphx-glr-auto-examples-applications-plot-face-recognition-py>.

One of our goals for next week is to replicate this example as a OpenAPI service.

## References

*NOTE:*
> We will use bibtex, but start with footnotes. All http or links must
> also be in refernces. No exception.

[^1]: Cloudmesh Manual, <https://cloudmesh.github.io/cloudmesh-manual/> 

[^2]: Cloudmesh Repositories, <https://github.com/cloudmesh/>

[^3]: Cloudmesh OpenAPI Repository for automatically generated REST services from Python functions <https://github.com/cloudmesh/cloudmesh-openapi>.

[^4]: Cloudmesh Manaual Preface for cloudmesh,  <https://cloudmesh.github.io/cloudmesh-manual/preface/about.html>

[^5]: Cloudmesh Manual, Instalation instryctions for cloudmesh <https://cloudmesh.github.io/cloudmesh-manual/installation/install.html>

[^6]: Scikit Learn, Pipeline Anova SVM, <https://scikit-learn.org/stable/auto_examples/feature_selection/plot_feature_selection_pipeline.html>

[^cloudmesh-openapi]: Cloudmesh Openapi Web page <https://github.com/cloudmesh/cloudmesh-openapi>

[^Cloud-Computing]: G. von Laszewski, “Cloud Computing.” Web Page, Sep-2020 [Online]. Available: <https://cloudmesh-community.github.io/pub//vonLaszewski-cloud.pdf>

[^Swagger2.0]: OpenAPI Initiative, “The openapi specification.” Web Page [Online]. Available: <https://github.com/OAI/OpenAPI- Specification/blob/main/versions/2.0.md>

[^OpenAPI3.0]: OpenAPI Initiative, “The openapi specification.” Web Page [Online]. Available: <https://github.com/OAI/OpenAPI-Specification> 

[^RAML]: RAML, “RAML version 1.0: RESTful api modeling language.” Web Page [Online]. Available: <https://github.com/raml-org/raml-spec/blob/main/versions/raml-10/raml-10.md>

[^Flask-Rest]: R. H. Kevin Burke Kyle Conroy, “Flask-restful.” Web Page [Online]. Available: <https://flask-restful.readthedocs.io/en/latest/>

[^Django-Rest-Services]: E. O. Ltd, “Django rest framework.” Web Page [Online]. Available: 
<https://www.django-rest-framework.org/>

[^Swagger]: S. Software, “API development for everyone.” Web Page [Online]. Available: <https://swagger.io>

[^OpenAPI-Tools]: A. Y. W. Hate, “OpenAPI.Tools.” Web Page [Online]. Available: 
<https://openapi.tools/>

[^OpenAPI-Specifications]: S. Software, “Swagger codegen documentation.” Web Page [Online]. Available: https://swagger.io/docs/open-source-tools/swagger-codegen/ 

[^NIST-SP-800-145]: NIST SP 800-145 Webpage < https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-145.pdf>

[^tensorflow-enterprise]: Google Tensorflow Enterprise website https://cloud.google.com/tensorflow-enterprise

[^polly]: Amazon Polly text-to-speech service website https://aws.amazon.com/polly/?c=ml&sec=srv



 




