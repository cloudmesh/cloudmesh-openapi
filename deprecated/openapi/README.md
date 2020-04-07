# Openapi Function generator

## Activity Log

## Week of Mar 9 - Mar 16

* Andrew Goldfarb

    * Worked with Ishan and Jonathan to finalize the start stop
      functionality.
    * Added functionality to delete the process entry from the
      registry upon stop command. 
    * Debugged weird start error for my personal machine where the
      start functionality was running two bash terminals causing the
      start function to fail.
    * Met with Professor to discuss proper implementation of the
      start/stop and how to tie into registry functionality.  

## Week prior to Mar 9th

* bkgerreis 
* Jonathan Beckford
* Prateek

* Andrew Goldfarb

1. Edited the stop function to take process PID and use os.kill to
   stop the process based on the name of the python file. However,
   according to Ishan this is still not working.
2. Resolved conflicts between master and our working branch 
3. Began work on assigning a default name if the user does not provide
   one for server start. Potetially, a function to assign an alias
   name to the whole process to amke it easier to reference.

## Install for development

cloudmesh-installer git pull analytics

```
cd cloudmesh-openapi
pip install -e .
```

## Keep up to date

explain how to set up and use upstream sync

### Project Meeting 

* [Mon 17 Feb](https://iu.zoom.us/rec/share/4dIpJZ-p8ztIHpH_q1HAZ6wzL6iiaaa8h3QX8_YMzRkn8tBfY_mRIe8z3j-3cZ_9?startTime=1581987567000)
* [Mon 24 Feb](https://iu.zoom.us/rec/share/_8ZLKK7Z6zpLb53f73_UW4EFBY_iX6a8gydM_vVbzRu2MhrC_sUCKhChUkLzgEK8?startTime=1582591839000)

### Basic Function Generator

#### Prateek Shaw -  code link.

<https://github.com/cloudmesh-community/sp20-516-229/tree/master/cloudmesh-openapi>

* created a basic function that will return the OpenAPI YAML file
  of given python function including parameters.

#### SP20-516-237 -- Jonathan Beckford

I created a class that generates the OpenAPI yaml file. I also created
a sample program that defines an example function, instantiates my
OpenAPI generator class and passes in the sample function as input. I
figured this would make things really easy to just paste any new
sample function for testing purposes. I also included the parameters
as was requested. I also ran my output yaml through the swagger
validator (https://editor.swagger.io/) to make sure it was compliant
and it was.  
[Link](https://github.com/cloudmesh-community/sp20-516-237/tree/master/projectAI/generateOpenAPI)

#### sp20-516-231 - Brian Kegerreis

I created a function to generate an OpenAPI spec including a rough
attempt at response types (only supports text/plain media types at
this point)
<https://github.com/cloudmesh-community/sp20-516-231/blob/master/openapi-exercises/example_echo.py>


### Server Start

#### Andrew Goldfarb - SP20-516-234

<https://github.com/cloudmesh-community/sp20-516-234/tree/open-api-exercise/openAPI>
I have created a basic function that returns the IP address of the
server running the function to tell if it is running on the device
itself or connected to the internet running while running the
function.
