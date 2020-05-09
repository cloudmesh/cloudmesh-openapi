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

 - contributors: all team

2. cms generate - to generate server yaml
    - executor that parses parameters and calls generator:
         
         <https://github.com/cloudmesh/cloudmesh-openapi/blob/master/cloudmesh/openapi/function/executor.py>
         
      - contributors:  Brian, Professor
        
    - generator that generates the server yaml:
         
         <https://github.com/cloudmesh/cloudmesh-openapi/blob/master/cloudmesh/openapi/function/generator.py>
         
      - contributors:  Brian, Jonathan, Prateek
    
3. cms server - to start and stop server

 <https://github.com/cloudmesh/cloudmesh-openapi/blob/master/cloudmesh/openapi/function/server.py>
 
  - contributors:  Jonathan, Andrew, Prateek, Ishan
      
4. cms registry - register the server and cache model

    - registry - registers server 
    
    <https://github.com/cloudmesh/cloudmesh-openapi/blob/master/cloudmesh/openapi/registry/Registry.py>
    
      - contributors: Falconi, Praful, Professor

    - cache - cache serialized model locally

    <https://github.com/cloudmesh/cloudmesh-openapi/blob/master/cloudmesh/openapi/registry/cache.py>
      
      - contributors: Jonathan
      
    - fileoperation - upload input files

    <https://github.com/cloudmesh/cloudmesh-openapi/blob/master/cloudmesh/openapi/registry/fileoperation.py>
    
      - contributors: Prateek, Brian 
  
5. cms scikitlearn - generate sklearn functions

<https://github.com/cloudmesh/cloudmesh-openapi/blob/master/cloudmesh/openapi/scikitlearn/SklearnGenerator.py>
    
   - contributors: Jagadeesh
   
6. cms image processing

   - contributors: Falconi, Ishan


## Deployment steps

<https://cloudmesh.github.io/cloudmesh-openapi/README.html#installation>

## Quick Start

<https://cloudmesh.github.io/cloudmesh-openapi/README.html#quick-steps-to-generate-start-and-stop-cpu-sample-example>

## Pytests

<https://cloudmesh.github.io/cloudmesh-openapi/README.html#pytests>

## Additional artifacts produced:

### Openapi VM set up script (Contributors: Jonathan Beckford)

<https://github.com/cloudmesh/get/blob/master/openapi/ubuntu18.04/index.html>

### Openapi project readme generator (Contributors: Jonathan Beckford, Professor)

<https://github.com/cloudmesh/cloudmesh-openapi/tree/master/sphinx>

### Chapters

##### Kubernetes (Contributors: Jonathan Beckford, Brian Kegerreis, Ashok Singam

<https://github.com/cloudmesh-community/sp20-516-231/blob/master/chapter/k8s-kubernetes-scheduler.md>





