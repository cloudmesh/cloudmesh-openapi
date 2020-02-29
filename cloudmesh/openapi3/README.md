# OpenAPI3 FUnction generator

## Install for development

cloudmesh-installer git pull analytics

```
cd cloudmesh-openapi
pip install -e .
```

USe proper < > for http links, dont use the word below 

## Keep up to date

explain how to set up and use upstream sync

### Project Meeting 

Mon 17 Feb

https://iu.zoom.us/rec/share/4dIpJZ-p8ztIHpH_q1HAZ6wzL6iiaaa8h3QX8_YMzRkn8tBfY_mRIe8z3j-3cZ_9?startTime=1581987567000 
AI Service meeting
Mon 24 Feb https://iu.zoom.us/rec/share/_8ZLKK7Z6zpLb53f73_UW4EFBY_iX6a8gydM_vVbzRu2MhrC_sUCKhChUkLzgEK8?startTime=1582591839000


### Andrew Goldfarb - SP20-516-234

https://github.com/cloudmesh-community/sp20-516-234/tree/open-api-exercise/openAPI
I have created a basic function that returns the IP address of the server running the function to tell if it is running on the device itself or connected to the internet running while running the function.

###Prateek Shaw -  code link.

https://github.com/cloudmesh-community/sp20-516-229/tree/master/cloudmesh-openapi
I have created a basic function that will return the OpenAPI YAML file of given python function including parameters.

### SP20-516-237 -- Jonathan Beckford

I created a class that generates the OpenAPI yaml file. I also created a sample program that defines an example function, instantiates my OpenAPI generator class and passes in the sample function as input. I figured this would make things really easy to just paste any new sample function for testing purposes. I also included the parameters as was requested. I also ran my output yaml through the swagger validator (https://editor.swagger.io/) to make sure it was compliant and it was.
Link to my code directory in git:
https://github.com/cloudmesh-community/sp20-516-237/tree/master/projectAI/generateOpenAPI

### sp20-516-231 - Brian Kegerreis

I created a function to generate an OpenAPI spec including a rough attempt at response types (only supports text/plain media types at this point)
https://github.com/cloudmesh-community/sp20-516-231/blob/master/openapi-exercises/example_echo.py
