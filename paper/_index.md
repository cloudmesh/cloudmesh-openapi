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

Cloud computing providers offer their customers on-demand self-service computing resources that are rapidly elastic and accessible via broad network access [^NIST-SP-800-145]. They accomplish this through the economies of scale achieved by resource pooling (serving multiple customers on the same hardware) and using measured services for fine grained customer billing [^NIST-SP-800-145]. Cloud providers offer these resources in multiple service models including infrastructure as a service, platform as a service, software as a service, and, recently, function as a service [^NIST-SP-800-145]. These providers are rapidly offering new platforms and services ranging from bare-metal machines to AI development platforms like Google’s TensorFlow Enterprise platform [^tensorflow-enterprise], and AI services such as Amazon’s text-to-speech service [^polly].

Customers can take advantage of cloud computing to reduce overhead expenses, increase their speed and scale of service deployment, and reduce development requirements by using cloud providers’ platforms or services. For example, customers’ developing AI systems can utilize clouds to handle big data inputs for which private infrastructure would be too costly or slow to implement. However, having multiple competing cloud providers leads to situations where service availability, performance, and cost may vary. Customer’s must navigate these heterogeneous solutions to meet their business needs while avoiding provider lock-in and managing organizational risk. This may require comparing or using multiple cloud providers to meet various objectives.

Cloudmesh works with a variety of cloud providers including Amazon Web Services, Microsoft Azure, Google Cloud Platform, and Oracle’s OpenStack based providers such as the academic research serving Chameleon Cloud.

### 2.4 Containers and Microservices

TBD

## 3. Architecture

### 3.1 Basic Auth Security

Cloudmesh OpenAPI supports configuration of a single authorized user through
basic authentication. Basic authentication is a simple authentication scheme built 
into the HTTP protocol. The client sends HTTP requests with the `Authorization` 
header that contains the word `Basic` followed by a space and a base64-encoded 
string of the format `username:password`. 

From wikipedia, basic auth is "a method for an HTTP user agent (e.g. a web browser) to provide a user name and password when making a request". ([more on this](https://github.com/cloudmesh/cloudmesh-openapi))

A cloudmesh user can create an OpenAPI server whose endpoints are only accessible 
as an authorized user. Currently, when basic auth is used as the authentication mechanism,
all endpoints are secured with this method. While this can be benficial to lock down an API,
it is limited in the sense that is is "all or nothing": either all endpoints are secured or none at all. 
This is something that can be improved upon in the future.

For an example of basic auth usage, see [Appendix A.5.](#a5-basic-auth-example)

Read more about Basic Auth usage with OpenAPI [here](https://swagger.io/docs/specification/authentication/basic-authentication/)

### 3.2 Utilizing Pickle as an alternative to MongoDB for "out-of-the-box" functionality

Currently, the installation and setup of cloudmesh openapi involves the installation of MongoDB and the configuration of mongo variables. This is documented [here.](https://github.com/cloudmesh/cloudmesh-openapi#installation)

There have been serveral recent cloudmesh projects involving Raspberry Pis. Unfortunately, the minimum version of MongoDB required for openapi is not available to the Raspberry Pi. Thus cloudmesh-openapi is not available to Pi users with MongoDB.

In an effort to provide this software to all those that are interested regardless of OS/machine, we have added a new default storage mechanism that functions "out-of-the-box" with cloudmesh-openapi. This storage mechanism is implemented with python's native Pickle at the heart. All interfaces associated with MongoDB interactions have been extended to support switching to PickleDB. Thus, this addition is backwards compatible with previous versions of cloudmesh-openapi and requires little changes in the existing code base to support. Since Pickle is native to python, it is supported on any platform running python.


It is important to note that there are essentially no security mechanisms with Pickle. We provide this option for users to test their APIs on different machines with little to no setup, but we do not recommend its usage in a production server. 

See [Appendix A.6](#a6-switching-between-pickledb-and-mongodb) to see how to switch between DB protocols.

### 3.3 Cloud Provider Hosted AI Service

A user deploys Cloudmesh OpenAPI on a virtual machine from a cloud provider, and uses it to host auto-generated, RESTful, AI services. A user constructs an AI service as a set of Python functions that implement a workflow, for example, downloading data from a remote server, training an AI model, uploading a new sample for prediction, and running a prediction on that sample. Cloudmesh OpenAPI hosts user provided Python functions on a web server that is accessible using standard HTTP request methods. In Figure 1 we show a remote client accessing a Cloudmesh OpenAPI server to execute an AI service workflow. In this example, the user deployed Cloudmesh OpenAPI on a virtual machine from a single cloud provider. Cloudmesh OpenAPI provides the choice of multiple supported providers to allow users to meet their specific administrative requirements.

![AI Service Workflow](https://github.com/cloudmesh/cloudmesh-openapi/raw/main/images/ai-service-workflow.png)

**Figure 1:** A client running an AI service workflow, generated and hosted by Cloudmesh OpenAPI, on a cloud provider virtual machine. Requests for each function invocation are made using standard HTTP request methods including function arguments. 

### 3.4 Multi-Cloud Hosted AI Service

Cloudmesh with Cloudmesh OpenAPI provides a framework to deploy AI services to multiple clouds. One use case for a multi-cloud deployment is to benchmark cloud provider VM performance. A user can use these tools to script the deployment of virtual machines with different providers, virtual machine sizes, or operating systems.  In Figure 2, a user has deployed an AI service hosted by Cloudmesh OpenAPI on three separate cloud providers, AWS, Azure, and Google. The user makes standard HTTP method requests to access the services simultaneously, and gathers responses and benchmark statistics. With the Cloudmesh benchmark utility, the user can measure the runtime of each AI service function and collect key information such as virtual machine memory usage. This information provides the user key insight for future hosting decisions. We distinguish this example from Figure 1, where the AI service is deployed on a single cloud provider. 

![Mult-Cloud AI Services](https://github.com/cloudmesh/cloudmesh-openapi/raw/main/images/multi-cloud-ai-service.png)

**Figure 2:** A client simultaneously accesses an AI service hosted on three seperate cloud providers, AWS, Azure, and Google to benchmark provider performance. 

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

In this section we will discuss the setup and execution of a benchmark for three example AI services.

#### 4.3.1 VM Selection

When benchmarking cloud performance, it is important to identify and control deployment parameters that can affect the performance results. This enables one to analyze comparable services or identify opportunities for service improvement for varying deployment features such as machine size, location, network, or storage hardware. These examples aimed to create similar machines across all three clouds and measure service performance. See Table 1 for a summary of the parameters controlled in these benchmark examples.

One key component is the virtual machine size, which determines the number of vCPUs, the amount of memory, attached storage types, and resource sharing policies. Resource sharing policies include shared core machine varieties which providers offer at less expensive rates and allow the virtual machines to burst over its base clock rate in exchange for credits or the machines inherent bursting factor [^aws-images] [^google-images]. For this example, we chose three similar machine sizes that had comparable vCPUs, comparable underlying processors, memory, price, and were not a shared core variety. We installed the same Ubuntu 20.04 operating system on all three clouds. 

Another factor that can affect performance, particularly in network latency, is the zone and region selected. We deploy all benchmark machines to zones on the east coast of the United States. This helps control variations caused by network routing latency and provides more insight into the inherent network performance of the individual cloud services.

**Table 1:** Selected VM parameters for benchmark measurement. Clouds were tested at least twice, and were run sequentially between the hours of approximately 1945 EST and 0330 EST starting with Google and ending with Azure. * For the Eigenfaces SVM example, only 60 runs were conducted on Azure due to a failed VM deployment from factors outside of the benchnmark scripts control.

|                  | AWS                    | Azure                                                            | Google          |
|------------------|------------------------|------------------------------------------------------------------|-----------------|
| Size (flavor) | m4.large               | Standard_D2s_v3                                                  | n1-standard-2   |
| vCPU          | 2                      | 2                                                                | 2               |
| Memory (GB)   | 8                      | 8                                                                | 7.5             |
| Image         | ami-0dba2cb6798deb6d8  | Canonical:0001-com-ubuntu-server-focal:20_04-lts:20.04.202006100 | ubuntu-2004-lts |
| OS            | Ubuntu 20.04 LTS  | Ubuntu 20.04 LTS | Ubuntu 20.04 LTS |
| Region           | us-east-1              | eastus                                                           | us-east1        |
| Zone             | N/A                    | N/A                                                              | us-east1-b      |
| Price ($/hr)     | 0.1                    | 0.096                                                            | 0.0949995       |
| Runs/Test        | 90                     | 60*                                                              | 90              |

#### 4.3.2 Eigenfaces-SVM Example

The benchmark script for the Eigenfaces SVM example uses Cloudmesh to create virtual machines and setup a Cloudmesh OpenAPI environment sequentially across the three measured clouds including Amazon, Azure, and Google. After the script sets up the environment, it runs a series of pytests that generate and launch the Eigenfaces-SVM OpenAPI service, and then conduct runtime measurements of various service functions. 

The benchmark runs the pytest in two configurations. After the benchmark script sets up a virtual machine environment, it runs the first pytest locally on the OpenAPI server and measures five runtimes:

1. Download and extraction of remote image data from ndownloader.figshare.com/files/5976015
2. The model training time when run as an OpenAPI service
3. The model training time when run as the Scikit-learn example without OpenAPI involvement
4. The time to upload an image from the server to itself
5. The time to predict and return the target label of the uploaded image

The benchmark runs the second pytest iteration from the remote client it is running on and interacts with the deployed OpenAPI service over the internet. It tests two runtimes:

1. The time to upload an image to the remote OpenAPI server
2. The time to run the predict function on the remote OpenAPI server, and return the target label  of the uploaded image 

In Figure 1 we compare the download and extraction time of the labeled faces in the wild dataset. This data set is approximately 233 MBs compressed, which allows us to measure a non-trivial data transfer. Lower transfer times imply the cloud has higher throughput from the data server, less latency to the data server, or that it provides access to a higher performing internal network. The standard deviation is displayed to compare the variation in the download times.

![Sample Graph 1](https://github.com/cloudmesh/cloudmesh-openapi/raw/main/images/sample_graph_1.png)

**Figure 1:** Donwnload (233MB) and extraction (~275MB) of remote image data from ndownloader.figshare.com/files/5976015.

In Figure 2 we measure the training time of the Eigenfaces-SVM model both as an OpenAPI service and as the basic Scikit-learn example. This allows us to measure runtime overhead added by OpenAPI compared to the source example. Here the two functions are identical except that the OpenAPI train function makes an additional function call to store the model to disk using joblib. This is necessary to share the model across the train and predict functions. The standard deviation is displayed to compare the variation in the training times.

![Sample Graph 2](https://github.com/cloudmesh/cloudmesh-openapi/raw/main/images/sample_graph_2.png)

**Figure 2:** Compares the eigenfaces-svm model training time running both as an OpenAPI service, and as the raw Scikit-learn example. There are two bars per cloud provider. The bold bars are the training time of the model when hosted as a Cloudmesh OpenAPI function. The pastel bars are the training time of the Scikit-learn example code without Cloudmesh OpenAPI involvement. The bars plot mean runtimes and the error bar reflects the standard deviation of the runtimes.

In Figure 3 we measure the time to upload an image to the server both from itself, and from a remote client. This allows us to compare the function runtime as experienced by the server, and as experienced by a remote client. The difference helps determine the network latency between the benchmark client and the cloud service. The standard deviation is displayed to compare the variation in the upload times.

![Sample Graph 3](https://github.com/cloudmesh/cloudmesh-openapi/raw/main/images/sample_graph_3.png)

**Figure 3:** Runtime of the upload function when run locally from the OpenAPI server and from a remote client. There are two bars per cloud provider. The bold bars are the runtime of the upload function as experienced by the server, and the pastel as experienced by the remote client. The bars plot mean runtimes and the error bar reflects the standard deviation of the runtimes.

In Figure 4 we measure the time to call the predict function on the uploaded image. Again we run this once from the local server itself, and a second time from a remote client to determine as experienced runtimes. The standard deviation is displayed to compare the variation in the predict times.

![Sample Graph 4](https://github.com/cloudmesh/cloudmesh-openapi/raw/main/images/sample_graph_4.png)

**Figure 4:** Runtime of the predict function when run locally from the OpenAPI server and from a remote client. There are two bars per cloud provider. The bold bars are the runtime of the predict function as experienced by the server, and the pastel as experienced by the remote client. The bars plot mean runtimes and the error bar reflects the standard deviation of the runtimes.

#### 4.3.3 Pipelined Anova SVM Example

#### 4.3.4 Caleb Example

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

This example demonstrates how to deploy a simple machine learning example onto a server using cloudmesh-openapi. The specific implementation details that this example is based on can be found [here.](https://scikit-learn.org/stable/auto_examples/feature_selection/plot_feature_selection_pipeline.html)

The model being implemented is, in essence, an SVM with extra features to improve the model.  An SVM (support vector machine) is a supervised learning model with associated learning algorithms used for classification and regression analysis. This model has become one of the most robust prediction methods widely used in problems conerning classification and the like.

The Pipeline and ANOVA aspects are extensions to the SVM to improve the overall model. The purpose of the pipeline is to assemble several steps that can be cross-validated together while setting different parameters. ANOVA on the other hand is an acronym for Analysis of Variance. It is an omnibus test, meaning it tests for a difference overall between all groups. In the context of an SVM, this information is useful as an SVM mainly classifies data into separate groups.

We can now proceed as follows:

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

### A.3.  Eigenfaces SVM Facial Recognition

Next we demonstrate how to locally run the Eigenfaces SVM example, and
then how to run its associated benchmark script. 

```
$ pwd
~/cm/cloudmesh-openapi

$ git checkout benchmark # todo required until merged into main

$ cms openapi generate EigenfacesSVM \
      --filename=./tests/generator-eigenfaces-svm/eigenfaces-svm-full.py \
      --import_class --enable_upload

$ cms openapi server start ./tests/generator-eigenfaces-svm/eigenfaces-svm-full.yaml
```

After running these commands, we opened a web user interface at <http://localhost:8080/cloudmesh/ui>.In the user interface, we run the download_data function with the default arguments. This downloads and extracts the labeled faces in the wild data set to the ~/scikit_learn_data/lfw_home directory. 

Next, we run the train function to train the model. The train function performs a 50/50 train/test split on the input data, and returns performance statistics of the trained model.

Next, we use the upload function to upload an example image using `~./tests/generator-eigenfaces-svm/example_image.jpg` as the function argument. This puts the example image in the ~/.cloudmesh/upload-file/ directory.

Finally, we run the predict function with the uploaded file path as an argument, `~/.cloudmesh/upload-file/example_image.jpg`, and recieve the classification as a response `['George W. Bush']`


Lastly, we close the server:

```
$ cms openapi server stop EigenfacesSVM
```

Next, we benchmark these tests while wrapping them into pytests and run them on various cloud services.

**Before continuing you must have successfully registered AWS, Azure, and Google clouds in your yaml file and be able to boot virtual machines on Google, AWS, and Azure. This example currently should work on Linux and macOS**

First we must change to a git branch that includes Azure provider fixes, and setup our ~./cloudmesh/cloudmesh.yaml file to replicate the parameters set for the benchmark results above. 

```
$ cd ~/cm/cloudmesh-azure 
$ git checkout benchmark # required until changes merged to main

$ cd ~/cm/cloudmesh-openapi

$ cp ~/.cloudmesh/cloudmesh.yaml ~/.cloudmesh/cloudmesh.bak.1 # to revert reverse the cp

$ cms config set cloudmesh.cloud.azure.default.image="Canonical:0001-com-ubuntu-server-focal:20_04-lts:20.04.202006100"
$ cms config set cloudmesh.cloud.azure.default.size="Standard_D2s_v3"
$ cms config set cloudmesh.cloud.azure.credentials.AZURE_REGION="eastus"

$ cms config set cloudmesh.cloud.aws.default.image="ami-0dba2cb6798deb6d8"
$ cms config set cloudmesh.cloud.aws.default.size="m4.large"
$ cms config set cloudmesh.cloud.aws.default.username="ubuntu"
$ cms config set cloudmesh.cloud.aws.credentials.region="us-east-1"

$ cms config set cloudmesh.cloud.google.default.image="ubuntu-2004-lts"
$ cms config set cloudmesh.cloud.google.default.image_project="ubuntu-os-cloud"
$ cms config set cloudmesh.cloud.google.default.zone="us-east1-b"
$ cms config set cloudmesh.cloud.google.default.region="us-east1"
$ cms config set cloudmesh.cloud.google.default.flavor="n1-standard-2"
```

Next we will modify the default security group to open the flask server port 8080 for OpenAPI service testing.

```
$ cms sec rule add openapi 8080 8080 tcp 0.0.0.0/0
$ cms sec group add default openapi for_openapi_demo
# the above two command should allow aws and azure to work
# sec group load is broken for google and it does not use the default sec group, so you have to manually add the openapi rule to google cloud for now
# console.cloud.google.com > VPC network > firewall > create firewall rule
# name: openapi, targets:  all instances in network, Source IP ranges: 0.0.0.0 /0, specified protocols and ports: tcp 8080 > create
```

Next we will run the benchmarking script, ~./tests/generator-eigenfaces-svm/benchmark-eigenfaces.py. This script utilizes the Cloudmesh shell and the Bash script, ~/.tests/generator-eigenfaces-svm/eigenfaces-svm-full-script, to sequentially deploy a VM on each of the clouds, install Cloudmesh-openapi and the example dependencies, and then us the pytest, ./tests/test_030_generator_eigenfaces_svm.py, twice to benchmark the EigenfacesSVM service functions both locally from the server, and from the remote client running the benchmark script. Finally, it prints and plots performance statistics.

```
$ ./tests/generator/eigenfaces-svm/benchmark-eigenfaces.py run
```

If the command line argument `run` is passed to the script, then it will start up the virtual machines on each cloud. Output and benchmark results from each of the virtual machines will be store in the ~/.cloudmesh/eigenfaces-svm/vm_script_output/ directory. The benchmark results are scraped from the script outputs and stored in the ~/.cloudmesh/eigenfaces-svm/benchmark_output directory. If the `run` argument is **not** provided, it will only print statistics from script output already stored in the vm_script_output directory.

Statistics will be printed to the commandline, and graphs will be displayed using plt.show() function calls as well as saved to the ~./tests/generator-eigenfaces-svm/ directory.

### A.4. Using unit tests for Benchmarking

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

  ### A.5. Basic Auth Example

  Basic Auth in cloudmesh openapi can be enabled with the following flag
  ```
  --basic_auth=<username>:<password>
  ``` 
  flag. As such, this example will be an extension of a previously existing example. To follow with this example, navigate to the `cloudmesh-openapi` directory.

  We will use the `server-cpu` example which tells the user the CPU of the machine running the API.

  For this example, let's create a user with username `admin` and password `secret`.

  ```
  cms openapi generate get_processor_name \
    --filename=./tests/server-cpu/cpu.py \
    --basic_auth=admin:secret
    ```

    We can start the server as follows:
    ```
    cms openapi server start ./tests/server-cpu/cpu.yaml
    ```

    The user will now be required to authenticate as the registered user in order to access the API. This can be done by specifying the Basic Auth credentials in the header as done [here](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Authorization). Alternatively, the user can login via the [swagger UI](http://localhost:8080/cloudmesh/u) when the server is started.

### A.6 Switching between PickleDB and MongoDB

The default "out-of-the-box" storage mechanism of cloudmesh-openapi is Pickle. This requires no setup of the DB on the user's end.

To switch to MongoDB, the user must first change their config option as follows:
```
cms openapi register protocol mongo
```
Note that by switching to mongo, certain mongo variables need to be filled out. Mongo may need to be installed as well. Refer to [this](https://github.com/cloudmesh/cloudmesh-openapi/#installation) documentation to see how this process can be done.

One may switch back to pickle with the same command:
```
cms openapi register protocol pickle
```

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

[^Cloud-Computing]: G. von Laszewski, "Cloud Computing", Web Page, Sep-2020 [Online]. Available: <https://cloudmesh-community.github.io/pub//vonLaszewski-cloud.pdf>

[^Swagger2.0]: OpenAPI Initiative, "The openapi specification", Web Page [Online]. Available: <https://github.com/OAI/OpenAPI- Specification/blob/main/versions/2.0.md>

[^OpenAPI3.0]: OpenAPI Initiative, "The openapi specification." Web Page [Online]. Available: <https://github.com/OAI/OpenAPI-Specification> 

[^RAML]: RAML, "RAML version 1.0: RESTful api modeling language", Web Page [Online]. Available: <https://github.com/raml-org/raml-spec/blob/main/versions/raml-10/raml-10.md>

[^Flask-Rest]: R. H. Kevin Burke Kyle Conroy, "Flask-restful", Web Page [Online]. Available: <https://flask-restful.readthedocs.io/en/latest/>

[^Django-Rest-Services]: E. O. Ltd, "Django rest framework", Web Page [Online]. Available: 
<https://www.django-rest-framework.org/>

[^Swagger]: S. Software, "API development for everyone", Web Page [Online]. Available: <https://swagger.io>

[^OpenAPI-Tools]: A. Y. W. Hate, "OpenAPI.Tools", Web Page [Online]. Available: 
<https://openapi.tools/>

[^OpenAPI-Specifications]: S. Software, "Swagger codegen documentation", Web Page [Online]. Available: <https://swagger.io/docs/open-source-tools/swagger-codegen/>

[^NIST-SP-800-145]: "NIST SP 800-145", Web page [Online]. Available: <https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-145.pdf>

[^tensorflow-enterprise]: "TensorFlow Enterprise", Web page [Online]. Available: <https://cloud.google.com/tensorflow-enterprise>

[^polly]: "Amazon Polly. Turn text into lifelike speech using deep learning." Web page [Online]. Available: <https://aws.amazon.com/polly/?c=ml&sec=srv>

[^eigenfaces-svm]: "Faces recognition example using eigenfaces and SVMs", Web Page [Online]. Available: <https://scikit-learn.org/stable/auto_examples/applications/plot_face_recognition.html#sphx-glr-auto-examples-applications-plot-face-recognition-py>

[^labeled-faces-wild]: Huang, Gary & Jain, Vidit & Learned-Miller, Erik. (2007). Unsupervised Joint Alignment of Complex Images. ICCV. 1-8. 10.1109/ICCV.2007.4408858. Available: <http://vis-www.cs.umass.edu/papers/iccv07alignment.pdf>

[^google-images]: "Machine Types", Web page [Online]. Available: <https://cloud.google.com/compute/docs/machine-types>

[^aws-images]: "Amazon EC2 Instance Types", Web page [Online]. Available: <https://aws.amazon.com/ec2/instance-types/>

[^nist-wg]: "NIST Big Data Working Group", Web Page [Online]. Available: <https://bigdatawg.nist.gov/show_InputDoc.php> 




