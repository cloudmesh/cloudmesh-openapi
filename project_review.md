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

-----------

## Contributors based on Git tracking

***NOTE:*** This is not completely accurate because some did not have git config done correctly.

<https://github.com/cloudmesh/cloudmesh-openapi/graphs/contributors>

-----------

## Code Breakdown

1. cms command:

    <https://github.com/cloudmesh/cloudmesh-openapi/blob/main/cloudmesh/openapi/command/openapi.py>

    **Contributors:** all team

    -----------

2. cms generate - to generate server yaml
    - **executor** that parses parameters and calls generator:
         
         <https://github.com/cloudmesh/cloudmesh-openapi/blob/main/cloudmesh/openapi/function/executor.py>
         
         **Contributors:**  Brian, Professor
        
    - **generator** that generates the server yaml:
         
         <https://github.com/cloudmesh/cloudmesh-openapi/blob/main/cloudmesh/openapi/function/generator.py>
         
        **Contributors:**  Brian, Jonathan, Prateek

    -----------

3. cms server - to start and stop server

    <https://github.com/cloudmesh/cloudmesh-openapi/blob/main/cloudmesh/openapi/function/server.py>
 
    - **Contributors:**  Jonathan, Andrew, Prateek, Ishan

    -----------

4. cms registry - register the server and cache model

    - **registry** - registers server 
    
        <https://github.com/cloudmesh/cloudmesh-openapi/blob/main/cloudmesh/openapi/registry/Registry.py>
    
        **Contributors:** Falconi, Praful, Professor

    - **cache** - cache serialized model locally

        <https://github.com/cloudmesh/cloudmesh-openapi/blob/main/cloudmesh/openapi/registry/cache.py>
      
        **Contributors:** Jonathan
      
    - **fileoperation** - upload input files

        <https://github.com/cloudmesh/cloudmesh-openapi/blob/main/cloudmesh/openapi/registry/fileoperation.py>
    
        **Contributors:** Prateek, Brian 

    -----------

5. cms scikitlearn - generate sklearn functions

    <https://github.com/cloudmesh/cloudmesh-openapi/blob/main/cloudmesh/openapi/scikitlearn/SklearnGeneratorFile.py>
    
    **Contributors:** Jagadeesh

      -----------

6. cms image processing

    **Contributors:** Falconi, Ishan
    
7. cms text analysis
    
    **Contirbutor:** Andrew Goldfarb
    
    <https://github.com/cloudmesh/cloudmesh-openapi/tree/main/tests/generator-natural-lang>

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

## Limitations

1. Integration of openapi with cms allows for running locally only.  Cloud integration was not fully completed although team did create a way to setup openapi in a VM using a remote script for [openstack](https://github.com/cloudmesh/get/blob/main/openapi/ubuntu18.04/index.html) and [google](https://github.com/cloudmesh/get/blob/main/openapi/google/index.html)  

2. The generator only supports creating arrays of number data type.  This limitation is due to the bug documented below in ***Bugs*** section.  So manual changes are required to the output yaml to allow for other data types until another work around is found or the bug is resolved.

-----------

## Bugs

1. reported a bug to Connexion and documented it in github for future reference:
  <https://github.com/cloudmesh/cloudmesh-openapi/issues/60>

-----------

## Additional artifacts produced:

### Openstack VM set up script

   - [OPENSTACK](https://github.com/cloudmesh/get/blob/main/openapi/ubuntu18.04/index.html)
   
   - [GOOGLE](https://github.com/cloudmesh/get/blob/main/openapi/google/index.html)

   **Contributors:** Jonathan Beckford, Andrew Goldfarb

  
### Openapi project readme generator

   <https://github.com/cloudmesh/cloudmesh-openapi/tree/main/sphinx>

   **Contributors:** Jonathan Beckford, Professor

  
### Chapters

##### Kubernetes

   <https://github.com/cloudmesh-community/sp20-516-231/blob/main/chapter/k8s-kubernetes-scheduler.md>

   **Contributors:**  Jonathan Beckford, Brian Kegerreis, Ashok Singam




