# Benchmarking Multi-Cloud Auto Generated AI Services

[![Check Report](https://github.com/cloudmesh/cloudmesh-openapi/workflows/Check%20Report/badge.svg)](https://github.com/cloudmesh/cloudmesh-openapi/actions)

NOTE:
> This document is maintained at:
>
> * <https://github.com/cloudmesh/cloudmesh-openapi/blob/main/paper/_index.md>
>

[Gregor von Laszewski](https://laszewski.github.io), 
Richard Otten,
[Anthony Orlowski](https://github.com/aporlowski), [fa20-523-310](https://github.com/cybertraining-dsc/fa20-523-310/), 
[Caleb Wilson](https://github.com/calewils), [fa20-523-348](https://github.com/cybertraining-dsc/fa20-523-348/)


Corresponding author: laszewski@gmail.com

[Edit](https://github.com/cybertraining-dsc/fa20-523-348/blob/main/project/project.md)

{{% pageinfo %}}

## Abstract

In this work we are benchmarking auto generated cloud REST services on
various clouds. In today's application scientist want to share their
services with a wide number of colleagues while not only offering the
services as bare metal programs, but exposing the functionality as a
software as a service. For this reason a tool has been developed that
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
Sklearn artificial intelligent algorithms. These pytests will then be
ran on different cloud services to benchmark different statistics on
how they run and how the cloud performs. The team will obtain cloud
service accounts from AWS, Azure, Google, and OpenStack. To deploy the
pytests, the team will use Cloudmesh and its Openapi based REST
services to benchmark the performance on different cloud
services. Benchmarks will include components like data transfer time,
model train time, model prediction time, and more. The final project
will include scripts and code for others to use and replicate our
tests. The team will also make a report consisting of research and
findings.

## 2. Background and Related Research

### 2.1 Cloudmesh

Cloudmesh [^1][^4] is a service that enables users to access multi-cloud
environments easily. Cloudmesh is an evolution of previous tools that
have been used by many users. Cloudmesh makes interacting with
clouds easy by creating a service mashup to access common cloud
services across numerous cloud platforms. Cloudmesh contains a
sophisticated command shell, a database to store jason objects
representing virtual machines, storage and a registry of REST
services [^3]. Cloudmesh has a sophisticated plugin concept that is easy to
use and leverages python namespaces while being able to integrate
plugins from different source code directories [^2]. Installation of
Cloudmesh is available for macOS, Linux, Windows, and Rasbian [^5].

### 2.2 REST

REST is an acronym for representational state transfer. REST often
uses the HTTP protocol for the CRUD functions which create, read,
update, and delete resources. It is important to note that REST is not
a standard, but it is a software architectural style for building
network services. When referred to as a part of the HTTP protocol, REST has the
methods of GET, PUT, POST, and DELETE. These methods are used to
implement the CRUD functions on collections and items that REST
introduces [^Cloud-Computing].

* **Collection of resources** [^Cloud-Computing]: Assume the URI,
  `http://.../resources/`, identifies a collection of resources. The
  following CRUD functions would be implemented:

  * **GET**: List the URIs and details about the collection’s items. 
  * **PUT**: Replace the collection with a different collection.
  * **POST**: Make a new entry in the collection. The operation returns
    new entry’s URI and assigns it automatically.
  * **DELETE**: Delete the collection. 
		
* **Single Resource** [^Cloud-Computing]: Assume the URI,
  `http://.../resources/item58`, identifies a single resource in a
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
service, and, recently, function as a service [^NIST-SP-800-145].
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
may require comparing or utilizing multiple cloud providers to meet various
objectives.

### 2.4 Containers and Microservices

TBD

## 3. Architecture

TBD

## 4. Benchmarks

### 4.1. Algorithms and Datasets

This project uses a number of simple example algorithms and
datasets. We have chosen to use the examples included in Scikit Learn as
they are widely known and can be used by others to replicate our
benchmarks easily. Nevertheless, it will be possible to integrate
easily other data sources, as well as algorithms due to the generative
nature of our base code for creating REST services.

Within Skikit Learn we have chosen the following examples:

* **Pipelined ANOVA SVM**: An example code that shows a pipeline running
  successively a univariate feature selection with anova and then a
  SVM of the selected features [^6].
  
* **Eigenfaces SVM Facial Recognition**: A facial recognition example that first  utilizes principle component analysis (PCA) to generate eigenfaces from the training image data, and then trains and tests a SVM model [^eigenfaces-svm]. This example uses the real world "Labeled Faces in the Wild" dataset consisting of labeled images of famous individuals gathered from the internet [^labeled-faces-wild]     .

### 4.2. Cloud Providers

#### AWS

#### Azure

#### Google

#### OpenStack

#### Oracle

#### Raspberry Pi Cluster

### 4.3. Result Comparision

#### Eigenfaces-SVM Example

The Eigenfaces-SVM benchmark script utilizes Cloudmesh to create virtual machines and setup an Cloudmesh OpenAPI environment sequentially across the three measured clouds including Amazon, Azure, and Google. After the environment is setup, a series of pytests are run that generate and launch the Eigenfaces-SVM OpenAPI service, and then conduct runtime measurements of various service functions. 

The pytest is run in two configurations. After the benchmark script sets up a virtual machine environment, it runs the first pytest locally on the OpenAPI machine and measures five runtimes:

1. Downdload and extraction of remote image data from ndownloader.figshare.com/files/5976015
2. The model training time when run as an OpenAPI service
3. The model training time when run as the scikit-learn example without OpenAPI involvement
4. The time to upload an image from the server to itself
5. The time to predict and return the target label of the uploaded image

The second run is conducted on the remote client and interacts with the deployed OpenAPI service over the internet. It tests two runtimes:

1. The time to upload an image to the remote OpenAPI server
2. The time to run the predict function on the remote OpenAPI server, and return the target label  of the uploaded image

When benchmarking cloud performance it is important to identify and control deployment parameters that can affect the performance results. This enables one to analyze comparable services or identify opportunities for service improvement due to varying deployment features such as machine size, location, network, or storage hardware. This example aimed to create similar machines across all three clouds and measure service performance. See Table 1 for a summary of the parameters controlled in this benchmark example.

One key components is the virtual machine size, which determine the number of vCPUs, the amount of memory, attached storage types, and resource sharing policies. Resource sharing policies include shared core machine varieties which are offered at less expensive rates, and allow the virtual machine to opportunistically burst over its base clock rate in exchange for credits or the machines inherent bursting factor [^awsimages] [^google-images]. For this example we chose three similar machine sizes that had comparable vCPUs, comparable underlying processors, memory, price, and were not a shared core variety. Additionally, we installed the same Ubuntu 20.04 operating system on all three clouds. 

Another factor that can affect performance, particularly in network latency, is the zone and region selected. We choose to deploy all benchmark machines to zones located on the east coast of the United States. This helps control variations caused by network routing latency and provide more insight into the inherent network performance of the individual cloud services. 

|                  | AWS                    | Azure                                                            | Google          |
|------------------|------------------------|------------------------------------------------------------------|-----------------|
| VM size (flavor) | m4.large               | Standard_D2s_v3                                                  | n1-standard-2   |
| VM vCPU          | 2                      | 2                                                                | 2               |
| VM memory (GB)   | 8                      | 8                                                                | 7.5             |
| VM Image         | ami-0dba2cb6798deb6d8  | Canonical:0001-com-ubuntu-server-focal:20_04-lts:20.04.202006100 | ubuntu-2004-lts |
| Region           | us-east-1              | eastus                                                           | us-east1        |
| Zone             | N/A                    | N/A                                                              | us-east1-b      |
| Price ($/hr)     | 0.1                    | 0.096                                                            | 0.0949995       |
| Runs/Test        | 90                     | 60*                                                              | 90              |

**Table 1:** Eigenfaces-SVM benchmark parameters. Clouds were tested at least twice, and were run sequentially between the hours of approximately 0745 EST and 0330 EST starting with Google and ending with Azure. *Only 60 runs were conducted on Azure due to a failed VM deployment from factors outside of the benchnmark scripts control. 

In Figure 1 we compare the download and extraction time of the labeled faces in the wild dataset. This data set is approximately 233MBs compressed, which allows us to measure a non-trivial data transfer. Lower transfer times imply the cloud has less routing latency to the data server, or that it provides access to a higher performing internal network. The standard deviation is displayed to compare the variation in the download times.  

![Sample Graph 1](https://github.com/cloudmesh/cloudmesh-openapi/raw/main/images/sample_graph_1.png)

**Figure 1:** Donwload (233MB) and extraction (~275MB) of remote image data from ndownloader.figshare.com/files/5976015

In Figure 2 we measure the training time of the Eigenfaces-SVM model both as a OpenAPI service and as the basic Scikit-learn example. This allows us to measure runtime overhead added by OpenAPI compared to the source example. In this case the two functions are identical except that the OpenAPI train function makes an additional store_model function call to store the model to disk using joblib. This is necessary to share the model across the train and predict functions. The standard deviation is displayed to compare the variation in the training times.  

![Sample Graph 2](https://github.com/cloudmesh/cloudmesh-openapi/raw/main/images/sample_graph_2.png)

**Figure 2:** Compares the eigenfaces-svm model training time running both as an OpenAPI service, and as the raw Scikit-learn example

In Figure 3 we measure the time to upload an image to the server both from itself, and from a remote client. This allows us to compare the function runtime as experienced by the server, and as experienced by a remote client. The difference helps determine the network latency between the benchmark client and the cloud service. The standard deviation is displayed to compare the variation in the upload times.  

![Sample Graph 3](https://github.com/cloudmesh/cloudmesh-openapi/raw/main/images/sample_graph_3.png)

**Figure 3:** Runtime of the upload function when run locally from the OpenAPI server and from a remote client 

In Figure 4 we measure the time to call the predict function on the uploaded image. Again we run this once from the local server itself, and a second time from a remote client to determine as experienced runtimes. The standard deviation is displayed to compare the variation in the predict times.  

![Sample Graph 4](https://github.com/cloudmesh/cloudmesh-openapi/raw/main/images/sample_graph_4.png)

**Figure 4:** Runtime of the predict function when run locally from the OpenAPI server and from a remote client

## 5. Conclusion

## 6. Limitations

Azure has updated their libraries and discontinued the version 4.0
Azure libraries. We updated Cloudmesh to use the new library, but not all features, such as virtual machine delete, are implemented or verified.  

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
# fill out mongo variables
# make sure autinstall is True
cms config set cloudmesh.data.mongo.MONGO_AUTOINSTALL=True
cms admin mongo install --force
# Restart a new terminal to make sure mongod is in your path
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
# This command returns
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
# This command returns
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
SciKitLearn’s website. We obtained cloud service accounts from AWS,
Azure, GCP, and Chameleon Cloud, and verified Cloudmesh documentation
while applying for the cloud accounts. We registered our accounts with
the Cloudmesh shell and executed VM operations using Cloudmesh.
  
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

Last week we created the first draft of the eigenfaces-svm example
that is found in the "benchmark" branch.  It outputs the example and
prints benchmark information. We are making progress on manually
running this example on a cloud VM using the Cloudmesh shell, which
will generate the requirements for our final script.

This week we successfully ran the eigenfaces-svm example on Goolge
Cloud, Amazon Web Services, and Microsoft Azure. We created a script
eigenfaces-svm-script that can deploy the OpenAPI service on a fresh
VM on a cloud and run the eigenfaces-svm example. We also created the
eigenfaces-svm-full example which breaks the workflow into a functions
that download remote data, train and tests the model, provide a image
upload function, and a prediction function. We also created a pytest
that automatically run those four functions and print benchark
information.

Next week we will create a script to run the eigenfaces-svm-full
example on each cloud multiple times, and them summarize and plot
benchmark information to compare the clouds. Additionally, we will
finish the report.

## Acknowledgements

We like to thank [Vishwanadham Mandala](https://github.com/cybertraining-dsc/fa20-523-325/) to participate in helping write an earlier version of this document.

## References

[^1]: Cloudmesh Manual, <https://cloudmesh.github.io/cloudmesh-manual/> 

[^2]: Cloudmesh Repositories, <https://github.com/cloudmesh/>

[^3]: Cloudmesh OpenAPI Repository for automatically generated REST services from Python functions <https://github.com/cloudmesh/cloudmesh-openapi>.

[^4]: Cloudmesh Manaual Preface for cloudmesh,  <https://cloudmesh.github.io/cloudmesh-manual/preface/about.html>

[^5]: Cloudmesh Manual, Instalation instryctions for cloudmesh <https://cloudmesh.github.io/cloudmesh-manual/installation/install.html>

[^6]: Scikit Learn, Pipeline Anova SVM, <https://scikit-learn.org/stable/auto_examples/feature_selection/plot_feature_selection_pipeline.html>

[^cloudmesh-openapi]: Cloudmesh Openapi Web page <https://github.com/cloudmesh/cloudmesh-openapi>

[^Cloud-Computing]: G. von Laszewski, "Cloud Computing." Web Page, Sep-2020 [Online]. Available: <https://cloudmesh-community.github.io/pub//vonLaszewski-cloud.pdf>

[^Swagger2.0]: OpenAPI Initiative, "The openapi specification." Web Page [Online]. Available: <https://github.com/OAI/OpenAPI- Specification/blob/main/versions/2.0.md>

[^OpenAPI3.0]: OpenAPI Initiative, "The openapi specification." Web Page [Online]. Available: <https://github.com/OAI/OpenAPI-Specification> 

[^RAML]: RAML, "RAML version 1.0: RESTful api modeling language." Web Page [Online]. Available: <https://github.com/raml-org/raml-spec/blob/main/versions/raml-10/raml-10.md>

[^Flask-Rest]: R. H. Kevin Burke Kyle Conroy, "Flask-restful." Web Page [Online]. Available: <https://flask-restful.readthedocs.io/en/latest/>

[^Django-Rest-Services]: E. O. Ltd, "Django rest framework." Web Page [Online]. Available: 
<https://www.django-rest-framework.org/>

[^Swagger]: S. Software, "API development for everyone." Web Page [Online]. Available: <https://swagger.io>

[^OpenAPI-Tools]: A. Y. W. Hate, "OpenAPI.Tools." Web Page [Online]. Available: 
<https://openapi.tools/>

[^OpenAPI-Specifications]: S. Software, "Swagger codegen documentation." Web Page [Online]. Available: <https://swagger.io/docs/open-source-tools/swagger-codegen/>

[^NIST-SP-800-145]: "NIST SP 800-145" Web page [Online]. Available: <https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-145.pdf>

[^tensorflow-enterprise]: "TensorFlow Enterprise." Web page [Online]. Available: <https://cloud.google.com/tensorflow-enterprise>

[^polly]: "Amazon Polly. Turn text into lifelike speech using deep learning." Web page [Online]. Available: <https://aws.amazon.com/polly/?c=ml&sec=srv>

[^eigenfaces-svm]: "Faces recognition example using eigenfaces and SVMs." Web Page [Online]. Available: <https://scikit-learn.org/stable/auto_examples/applications/plot_face_recognition.html#sphx-glr-auto-examples-applications-plot-face-recognition-py>

[^labeled-faces-wild]: Huang, Gary & Jain, Vidit & Learned-Miller, Erik. (2007). Unsupervised Joint Alignment of Complex Images. ICCV. 1-8. 10.1109/ICCV.2007.4408858. Available: <http://vis-www.cs.umass.edu/papers/iccv07alignment.pdf>

[^google-images]: "Machine Types" Web page [Online]. Available: <https://cloud.google.com/compute/docs/machine-types>

[^aws-images]: "Amazon EC2 Instance Types" Web page [Online]. Available: <https://aws.amazon.com/ec2/instance-types/>

 




