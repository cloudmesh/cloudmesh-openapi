# Automated Multicloud AI Service Generation

[Gregor von Laszewski](https://laszewski.github.io/), 
Richard Otten (github: ???), 
[Caleb Wilson](https://github.com/calewils), 
[Anthony Orlowski](https://github.com/aporlowski) (aporlows),
Vishwanadh M??? (hid?, github: ???) (your name does not shwo in slack)

Corresponding author: laszewski@gmail.com

## Code Location

This is temporary and will in final be moved elsewhere. Its conveniently for now placed on top so we can easier locate it

* github: <https://github.com/cloudmesh/cloudmesh-openapi> [^cloudmesh-openapi]
* branch: benchmark (not yet created)

## Abstract

## Introduction

## Background and Related Research

### REST
REST is an acronym for representational state transfer. REST often uses the HTTP protocol for the CRUD functions which create, read, update, and delete resources. It is important to note that REST is not a standard, but it is a software architectural style for building network services. When a part of the HTTP protocol, REST has the methods of GET, PUT, POST, and DELETE. These methods are used to implement the CRUD functions on collections and items that REST introduces. [^Cloud-Computing]



Collection of resources [^Cloud-Computing]:

	Assume the URI, http://.../resources/, identifies a collection of resources. The following CRUD functions would be implemented:

GET

	List the URIs and details about the collection’s items. 
	
PUT

	Replace the collection with a different collection.
	
POST

	Make a new entry in the collection. The operation returns new entry’s URI and assigns it automatically.  
	
DELETE

	Lastly, delete the collection. 
		



	
Single Resource [^Cloud-Computing]:

	Assume the URI, http://.../resources/item58, identifies a single resource in a collection. The following CRUD functions would be implemented:
	
GET

	Fetch a representation of the item in the collection, extracted in the appropriate media type.
	
PUT

	Replace the item in the collection. If the item does not exist, then create the item. 
	
POST 

	Typically, not used. Treat the item as a collection and make a new entry in it. 
	
DELETE

	Delete the item in the collection. 
	


	
	
Because REST has a defined structure, there are tools that manage programming to REST specifications. 
Here are different categories [^Cloud-Computing]: 




REST Specification Frameworks: 

Frameworks to define REST service specifications for generating REST services in a language and framework independently, include: 
Swagger 2.0 [^Swagger2.0], OpenAPI 3.0 [^OpenAPI3.0], and RAML [^RAML]. 




REST programming language support: 

Tools and services for targeting specific programming languages, include:
Flask Rest [^Flask-Rest], Django Rest Services [^Django-Rest-Services]




REST documentation-based tools:

These tools document REST specifications. One such tool is Swagger [^Swagger]




REST design support tools: 

These tools support the design process in developing REST services while extracting on top of the programming languages. 
These tools also define reusable to create clients and servers for particular targets.These tools include Swagger [^Swagger] , additional swagger tools are available at OpenAPI Tools [^OpenAPI-Tools] to generate code from OpenAPI specifications [^OpenAPI-Specifications]

### VM Cloud providers 
Cloud computing providers offer their customers on-demand self-service computing resources that are rapidly elastic and accessible via broad network access [^NIST SP 800-145]. They accomplish this through the economies of scale achieved by resource pooling (serving multiple customers on the same hardware), and utilizing measured services for fine grained customer billing [^NIST SP 800-145]. Examples of cloud providers include Amazon Web Services, Microsoft Azure, Google Cloud Platform, Oracle’s OpenStack based providers, and more.  Cloud providers offer these resources in multiple service models including infrastructure as a service, platform as a service, software as a service, and, recently, function as a service. [^NIST SP 800-145].  These providers are rapidly offering new platforms and services ranging from bare-metal machines to AI development platforms like Google’s TensorFlow Enterprise platform [^tensorflow enterprise], and AI services such as Amazon’s text-to-speech service [^polly]. 

Customers can take advantage of cloud computing to reduce overhead expenses, increase their speed and scale of service deployment, and reduce development requirements by utilizing providers’ platforms or services. For example, customers’ developing AI systems can utilize clouds to handle big data inputs for which private infrastructure would be too costly or slow to implement. However, having multiple competing cloud providers leads to situations where service availability, performance, and cost may vary greatly. Customer’s must navigate these heterogeneous solutions to meet their business needs while avoiding provider lock-in and managing organizational risk. This may require utilizing multiple cloud providers to meet various objectives.
### Containers and Microservices

## Architecture

## Benchmarks

### AWS

### Azure

### Google

### OpenStack

### Oracle

### Raspberry Pi Cluster

### Result Comparision

## Conclusion

## Acknowledgements

## Plan
Thus far in the project we have familiarized ourselves with Cloudmesh-Openapi by recreating example services on our local machines, setup a git branch of the source project on which we will collaborate, contributed to the paper’s background section, and started looking for example AI analytics, like those provided at SciKitLearn’s website.
  
  Moving forward, we will obtain cloud service accounts from AWS, Azure, GCP, and Chameleon Cloud. We will verify Cloudmesh documentation while applying for cloud accounts. We will develop benchmark tests in the form of pytests that replicate the AI analytic examples.  We will each use Cloudmesh to deploy these tests as an Openapi based REST service and benchmark their performance on various cloud providers. Our benchmarks will measure various components such as data transfer time, model train time, model prediction time, etc. We will then consolidate and report on our findings. Our final project will include a script that utilizes the Cloudmesh shell to automate our benchmark tests so others can replicate our work. 

For an AI analytic benchmark test, one intesresting example to replicate may be the faces recognition example using eigenfaces and SVMs  <https://scikit-learn.org/stable/auto_examples/applications/plot_face_recognition.html#sphx-glr-auto-examples-applications-plot-face-recognition-py>. 
## Appendix

### Setup 

### Benchmark Source code

## References

We will use bibtex, but start with footnotes. All http or links must also be in refernces. No exception.

[^cloudmesh-openapi]: Cloudmesh Openapi Web page <https://github.com/cloudmesh/cloudmesh-openapi>

[^Cloud-Computing] G. von Laszewski, “Cloud Computing.” Web Page, Sep-2020 [Online]. Available: https://cloudmesh-community.github.io/pub//vonLaszewski-cloud.pdf

[^Swagger2.0] OpenAPI Initiative, “The openapi specification.” Web Page [Online]. Available: https://github.com/OAI/OpenAPI- Specification/blob/master/versions/2.0.md 

[^OpenAPI3.0] OpenAPI Initiative, “The openapi specification.” Web Page [Online]. Available: https://github.com/OAI/OpenAPI-Specification 

[^RAML] RAML, “RAML version 1.0: RESTful api modeling language.” Web Page [Online]. Available: https://github.com/raml-org/raml-spec/blob/master/versions/raml-10/raml-10.md 

[^Flask-Rest] R. H. Kevin Burke Kyle Conroy, “Flask-restful.” Web Page [Online]. Available: https://flask-restful.readthedocs.io/en/latest/ 

[^Django-Rest-Services] E. O. Ltd, “Django rest framework.” Web Page [Online]. Available: 
https://www.django-rest-framework.org/ 

[^Swagger] S. Software, “API development for everyone.” Web Page [Online]. Available: https://swagger.io 

[^OpenAPI-Tools] A. Y. W. Hate, “OpenAPI.Tools.” Web Page [Online]. Available: 
https://openapi.tools/ 

[^OpenAPI-Specifications] S. Software, “Swagger codegen documentation.” Web Page [Online]. Available: https://swagger.io/docs/open-source-tools/swagger-codegen/ 

[^NIST SP 800-145]: NIST SP 800-145 Webpage < https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-145.pdf>

[^tensorflow enterprise]: Google Tensorflow Enterprise website https://cloud.google.com/tensorflow-enterprise

[^polly]: Amazon Polly text-to-speech service website https://aws.amazon.com/polly/?c=ml&sec=srv


