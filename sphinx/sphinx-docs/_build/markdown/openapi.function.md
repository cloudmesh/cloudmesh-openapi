# openapi.function package

## Submodules

## openapi.function.conf module


### openapi.function.conf.setup(app)

### openapi.function.conf.skip(app, what, name, obj, would_skip, options)
## openapi.function.executor module


### class openapi.function.executor.Parameter(arguments)
Bases: `object`

To generate a useful output for the variables. Example:

> from cloudmesh.openapi.function.executor import Parameter
> p = Parameter(arguments)
> p.Print()

Invocation from program

> cd cloudmesh-openapi
> cms openapi generate calculator              –filename=./tests/generator-calculator/calculator.py             –all_functions

Returns

> Cloudmesh OpenAPI Generator:

> > File Locations:


> >     * Currdir:    .


> >     * Directory:  ./tests/generator-calculator


> >     * Filename:   ./tests/generator-calculator/calculator.py


> >     * YAML:       ./tests/generator-calculator/calculator.yaml

> > Yaml File Related:


> >     * Function:   calculator


> >     * Server url: [http://localhost:8080/cloudmesh](http://localhost:8080/cloudmesh)


> >     * Module:     calculator


#### Print()

#### \__init__(arguments)
Initialize self.  See help(type(self)) for accurate signature.


#### get(arguments)
## openapi.function.generator module


### class openapi.function.generator.Generator()
Bases: `object`


#### file_get(service, filename)

#### file_list()

#### file_put(service, filename, verbose=False)

#### generate_openapi(f=None, filename=None, serverurl=None, outdir=None, yamlfile=None, dataclass_list=None, enable_upload=False, write=True)
This is a main entry point into the module.  This function will generate the full OpenApi YAML formatted
specification for a module with one single function.


* **Parameters**

    
    * **f** – 


    * **filename** – 


    * **serverurl** – 


    * **outdir** – 


    * **yamlfile** – 


    * **dataclass_list** – 


    * **write** – 



* **Returns**

    


#### generate_openapi_class(class_name=None, class_description=None, filename=None, func_objects=None, serverurl=None, outdir=None, yamlfile=None, dataclass_list=None, all_function=False, enable_upload=False, write=True)
This is a main entry point into the module.  This function will generate the full OpenApi YAML formatted
specification for a python class or module with multiple functions.


* **Parameters**

    
    * **class_name** – 


    * **class_description** – 


    * **filename** – 


    * **func_objects** – 


    * **serverurl** – 


    * **outdir** – 


    * **yamlfile** – 


    * **dataclass_list** – 


    * **all_function** – 


    * **write** – 



* **Returns**

    


#### generate_parameter(name, _type, description)
Function to generate a single OpenApi YAML formatted parameter section


* **Parameters**

    
    * **name** – 


    * **_type** – 


    * **description** – 



* **Returns**

    


#### generate_path(class_name=None, description=None, long_description=None, funcname=None, parameters=None, responses=None, filename=None, all_function=None)
Function that generates a single OpenApi YAML formatted operation ID section


* **Parameters**

    
    * **class_name** – 


    * **description** – 


    * **long_description** – 


    * **funcname** – 


    * **parameters** – 


    * **responses** – 


    * **filename** – 


    * **all_function** – 



* **Returns**

    


#### generate_properties(attr, _type)
Function to generate a single OpenApi YAML formatted schema properties section


* **Parameters**

    
    * **attr** – 


    * **_type** – 



* **Returns**

    


#### generate_response(code, _type, description)
Function to generate a single OpenApi YAML formatted response section


* **Parameters**

    
    * **code** – 


    * **_type** – 


    * **description** – 



* **Returns**

    


#### generate_schema(_class)
Function to generate a single OpenApi YAML formatted schema section using python dataclass as input


* **Parameters**

    **_class** – 



* **Returns**

    


#### openAPITemplate( = '\\nopenapi: 3.0.0\\ninfo:\\n  title: {title}\\n  description: "{description}"\\n  version: "{version}"\\nservers:\\n  - url: {serverurl}\\n    description: "{description}"\\npaths:\\n  /{name}:\\n     get:\\n      summary: "{description}"\\n      description: Optional extended description in CommonMark or HTML.\\n      operationId: {filename}.{name}\\n      parameters:\\n        {parameters}\\n      responses:\\n        {responses}\\n{upload}\\n{components}\\n')

#### openAPITemplate2( = '\\nopenapi: 3.0.0\\ninfo:\\n  title: {title}\\n  description: "{description}"\\n  version: "{version}"\\nservers:\\n  - url: {serverurl}\\n    description: "{description}"\\npaths:\\n  {paths}\\n{upload}\\n{components}\\n')

#### parse_type(_type)
Function to lookup and output supported OpenApi data type using python data type as input


* **Parameters**

    **_type** – 



* **Returns**

    


#### populate_parameters(func_obj)
Function that converts all the input parameters of a python function into a single OpenApi YAML formatted
parameters section.


* **Parameters**

    **func_obj** – 



* **Returns**

    


#### uploadTemplate( = '\\n/upload:\\n  post:\\n    summary: upload a file\\n    operationId: {filename}.upload\\n    requestBody:\\n      content:\\n        multipart/form-data:\\n          schema:\\n            type: object\\n            properties:\\n              upload:\\n                type: string\\n                format: binary\\n    responses:\\n      \\'200\\':\\n        description: "OK"\\n        content:\\n          text/plain:\\n            schema:\\n              type: string\\n')
## openapi.function.server module


### class openapi.function.server.Server(name=None, spec=None, directory=None, host='127.0.0.1', server='flask', port=8080, debug=True)
Bases: `object`

This class manages all actions taken to interact with an OpenAPI AI server.


#### \__init__(name=None, spec=None, directory=None, host='127.0.0.1', server='flask', port=8080, debug=True)
Initialize self.  See help(type(self)) for accurate signature.


#### static get_name(name, spec)
Get the name of a server using specification


* **Parameters**

    
    * **name** – 


    * **spec** – 



* **Returns**

    


#### static list(name=None)
Lists the servers that have been registered in Registry


* **Parameters**

    **name** – 



* **Returns**

    


#### static ps(name=None)
List all of the actively running servers or if name is provided return whether the server is running


* **Parameters**

    **name** – 



* **Returns**

    


#### run_os()
Start an openapi server by creating a physical flask script


* **Returns**

    


#### start(name=None, spec=None, foreground=False)
Start up an OpenApi server


* **Parameters**

    
    * **name** – 


    * **spec** – 


    * **foreground** – 



* **Returns**

    


#### static stop(name=None)
Stop a running OpenApi server


* **Parameters**

    **name** – 



* **Returns**

    


### openapi.function.server.daemon(func)
Decorator used to execute a Connexion flask app as a daemon


* **Parameters**

    **func** – 



* **Returns**

    


### openapi.function.server.dynamic_import(abs_module_path, class_name)
