# Automated Multicloud AI Service Generation

[Gregor von Laszewski](https://laszewski.github.io/), 
Richard Otten (github: ???), 
Caleb Wilson (hid?, github: ???), 
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

[^NIST SP 800-145]: NIST SP 800-145 Webpage < https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-145.pdf>

[^tensorflow enterprise]: Google Tensorflow Enterprise website https://cloud.google.com/tensorflow-enterprise

[^polly]: Amazon Polly text-to-speech service website https://aws.amazon.com/polly/?c=ml&sec=srv


