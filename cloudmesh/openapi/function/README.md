# function package

The function package includes 3 submodules:

  1. executor.py
  2. generator.py
  3. server.py

## Submodules

## function.executor module


### class function.executor.Parameter(arguments)
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


## function.generator module


### class function.generator.Generator()
Bases: `object`


#### file_get(service, filename)

#### file_list()

#### file_put(service, filename, verbose=False)

#### generate_openapi(f=None, filename=None, serverurl=None, outdir=None, yamlfile=None, dataclass_list=None, write=True)
function to generate open API of python function.


* **Parameters**

    
    * **f** – 


    * **filename** – 


    * **serverurl** – 


    * **outdir** – 


    * **yamlfile** – 


    * **dataclass_list** – 


    * **write** – 



* **Returns**

    


#### generate_openapi_class(class_name=None, class_description=None, filename=None, func_objects=None, serverurl=None, outdir=None, yamlfile=None, dataclass_list=None, all_function=False, write=True)
function to generate open API of python function.


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
function to generate parameters YAML contents


* **Parameters**

    
    * **name** – 


    * **_type** – 


    * **description** – 



* **Returns**

    


#### generate_path(class_name=None, description=None, long_description=None, funcname=None, parameters=None, responses=None, filename=None, all_function=None)
function to generate path yaml contents


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
function to generate properties of a schema


* **Parameters**

    
    * **attr** – 


    * **_type** – 



* **Returns**

    


#### generate_response(code, _type, description)
function to generate response yaml contents


* **Parameters**

    
    * **code** – 


    * **_type** – 


    * **description** – 



* **Returns**

    


#### generate_schema(_class)
function to generate schema in the components section from @dataclass
attributes


* **Parameters**

    **_class** – 



* **Returns**

    


#### openAPITemplate( = '\\nopenapi: 3.0.0\\ninfo:\\n  title: {title}\\n  description: "{description}"\\n  version: "{version}"\\nservers:\\n  - url: {serverurl}\\n    description: "{description}"\\npaths:\\n  /{name}:\\n     get:\\n      summary: "{description}"\\n      description: Optional extended description in CommonMark or HTML.\\n      operationId: {filename}.{name}\\n      parameters:\\n        {parameters}\\n      responses:\\n        {responses}\\n{components}\\n')

#### openAPITemplate2( = '\\nopenapi: 3.0.0\\ninfo:\\n  title: {title}\\n  description: "{description}"\\n  version: "{version}"\\nservers:\\n  - url: {serverurl}\\n    description: "{description}"\\npaths:\\n  {paths}\\n{components}\\n')

#### parse_type(_type)
function to parse supported openapi data types


* **Parameters**

    **_type** – 



* **Returns**

    


#### populate_parameters(func_obj)
Function to loop all the parameters of given function and generate
specification


* **Parameters**

    **func_obj** – 



* **Returns**

    

## function.server module


### class function.server.Server(name=None, spec=None, directory=None, host='127.0.0.1', server='flask', port=8080, debug=True)
Bases: `object`


#### \__init__(name=None, spec=None, directory=None, host='127.0.0.1', server='flask', port=8080, debug=True)
Initialize self.  See help(type(self)) for accurate signature.


#### static get_name(name, spec)

#### static list(name=None)
Lists the servises registered


* **Parameters**

    **name** – 



* **Returns**

    


#### static ps(name=None)

#### run_os()
Start an openapi server by creating a physical flask script


* **Returns**

    


#### start(name=None, spec=None, foreground=False)
Start up an openapi server


* **Parameters**

    
    * **name** – 


    * **spec** – 


    * **foreground** – 



* **Returns**

    


#### static stop(name=None)
Stop a running server


* **Parameters**

    **name** – 



* **Returns**

    


### function.server.daemon(func)

### function.server.dynamic_import(abs_module_path, class_name)
