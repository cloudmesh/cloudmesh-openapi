# Project Review

## Team members:
  - Jonathan Beckford
  - Brian Kegerreis
  - Prateek Shaw
  - Jagadeesh Kandimalla
  - Ishan Mishra
  - Andrew G
  - Falconi

## Project Documentation:

<https://cloudmesh.github.io/cloudmesh-openapi/index.html>

## Code Breakdown

1. cms command:

    <https://github.com/cloudmesh/cloudmesh-openapi/blob/master/cloudmesh/openapi/command/openapi.py>

    **Contributors:** all team

    -----------

2. cms generate - to generate server yaml
    - **executor** that parses parameters and calls generator:
         
         <https://github.com/cloudmesh/cloudmesh-openapi/blob/master/cloudmesh/openapi/function/executor.py>
         
         **Contributors:**  Brian, Professor
        
    - **generator** that generates the server yaml:
         
         <https://github.com/cloudmesh/cloudmesh-openapi/blob/master/cloudmesh/openapi/function/generator.py>
         
        **Contributors:**  Brian, Jonathan, Prateek

    -----------

3. cms server - to start and stop server

    <https://github.com/cloudmesh/cloudmesh-openapi/blob/master/cloudmesh/openapi/function/server.py>
 
    - **Contributors:**  Jonathan, Andrew, Prateek, Ishan

    -----------

4. cms registry - register the server and cache model

    - **registry** - registers server 
    
        <https://github.com/cloudmesh/cloudmesh-openapi/blob/master/cloudmesh/openapi/registry/Registry.py>
    
        **Contributors:** Falconi, Praful, Professor

    - **cache** - cache serialized model locally

        <https://github.com/cloudmesh/cloudmesh-openapi/blob/master/cloudmesh/openapi/registry/cache.py>
      
        **Contributors:** Jonathan
      
    - **fileoperation** - upload input files

        <https://github.com/cloudmesh/cloudmesh-openapi/blob/master/cloudmesh/openapi/registry/fileoperation.py>
    
        **Contributors:** Prateek, Brian 

    -----------

5. cms scikitlearn - generate sklearn functions

    <https://github.com/cloudmesh/cloudmesh-openapi/blob/master/cloudmesh/openapi/scikitlearn/SklearnGeneratorFile.py>
    
    **Contributors:** Jagadeesh

      -----------

6. cms image processing

    **Contributors:** Falconi, Ishan
    
7. cms text analysis
    
    **Contirbutor:** Andrew Goldfarb
    
    <https://github.com/cloudmesh/cloudmesh-openapi/tree/master/tests/generator-natural-lang>

-----------

## Deployment steps

   <https://cloudmesh.github.io/cloudmesh-openapi/README.html#installation>


-----------


## Quick Start

   <https://cloudmesh.github.io/cloudmesh-openapi/README.html#quick-steps-to-generate-start-and-stop-cpu-sample-example>
   
-----------

## Pytests

   <https://cloudmesh.github.io/cloudmesh-openapi/README.html#pytests>

-----------

## Additional artifacts produced:

### Openstack VM set up script

   <https://github.com/cloudmesh/get/blob/master/openapi/ubuntu18.04/index.html>

   **Contributors:** Jonathan Beckford, Andrew Goldfarb

  
### Openapi project readme generator

   <https://github.com/cloudmesh/cloudmesh-openapi/tree/master/sphinx>

   **Contributors:** Jonathan Beckford, Professor

  
### Chapters

##### Kubernetes

   <https://github.com/cloudmesh-community/sp20-516-231/blob/master/chapter/k8s-kubernetes-scheduler.md>

   **Contributors:**  Jonathan Beckford, Brian Kegerreis, Ashok Singam




