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

<https://github.com/cloudmesh/cloudmesh-openapi/blob/master/README.md>

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

1. Install cms openapi bundle:

<https://github.com/cloudmesh/cloudmesh-openapi/blob/master/README.md#instalation>


## Pytests

### Test documentation:

  <https://github.com/cloudmesh/cloudmesh-openapi/blob/master/tests/README.md>

### Simple initial test:

1. Manual steps for CPU:
   - Go to main project repo directory
      ```cd ~/cm/cloudmesh-openapi```
      
   - Generate yaml
      ```cms openapi generate get_processor_name --filename=./tests/server-cpu/cpu.py```
     
   - Start Server
      
      ```cms openapi server start ./tests/server-cpu/cpu.yaml```
      
   - Run Swagger UI
   
      - go to <http://127.0.0.1:8080/cloudmesh/ui>
  
   - Stop Server
   
       ```cms openapi server stop cpu```

2. Automated test for CPU:
   - Go to main project repo directory
      ```cd ~/cm/cloudmesh-openapi```
      
   - Execute pytest for cpu
      ```pytest -v -x --capture=no tests/server-cpu/test_03_generator.py```


