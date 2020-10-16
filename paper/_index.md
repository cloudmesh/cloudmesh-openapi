# Automated Multicloud AI Service Generation

[Gregor von Laszewski](https://laszewski.github.io/), 
Richard Otten (github: ???), 
Caleb Wilson (hid?, github: ???), 
[Anthony Orlowski](https://github.com/aporlowski) (hid?),
Vishwanadh M??? (hid?, github: ???) (your name does not shwo in slack)

Corresponding author: laszewski@gmail.com

## Code Location

This is temporary and will in final be moved elsewhere. Its conveniently for now placed on top so we can easier locate it

* github: <https://github.com/cloudmesh/cloudmesh-openapi>[^cloudmesh-openapi]
* branch: benchmark (not yet created)

## Abstract

## Introduction

## Background and Related Research

### REST
REST is an acronym for representational state transfer. REST often uses the HTTP protocol for the CRUD functions which create, read, update, and delete resources. It is important to note that REST is not a standard, but it is a software architectural style for building network services. When a part of the HTTP protocol, REST has the methods of GET, PUT, POST, and DELETE. These methods are used to implement the CRUD functions on collections and items that REST introduces. [^Cloud-Computing]
Collection of resources [^Cloud-Computing]:
Assume the URI, http://.../resources/, identifies a collection of resources.                       The following CRUD functions would be implemented:
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
Because REST has a defined structure, there are tools that manage programming to REST specifications. Here are different categories [^Cloud-Computing]: 
REST Specification Frameworks: 
Frameworks to define REST service specifications for generating REST services in a language and framework independently, include: Swagger 2.0 [^Swagger2.0], OpenAPI 3.0 [^OpenAPI3.0], and RAML [^RAML]. 
REST programming language support: 
Tools and services for targeting specific programming languages, include Flask Rest [^Flask-Rest], Django Rest Services [^Django-Rest-Services]
REST documentation-based tools:
These tools document REST specifications. One such tool is Swagger [^Swagger]
REST design support tools: 
These tools support the design process in developing REST services while extracting on top of the programming languages. These tools also define reusable to create clients and servers for particular targets. These tools include Swagger [^Swagger] , additional swagger tools are available at OpenAPI Tools [^OpenAPI-Tools] to generate code from OpenAPI specifications [^OpenAPI-Specifications]


### VM Cloud providers 

### Containers and MIcroservices

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

