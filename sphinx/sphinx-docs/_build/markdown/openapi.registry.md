# openapi.registry package

## Submodules

## openapi.registry.Registry module


### class openapi.registry.Registry.Registry()
Bases: `object`


#### Print(data, output=None)

#### \__init__()
Initialize self.  See help(type(self)) for accurate signature.


#### add(\*\*kwargs)

#### add_form_file(filename, \*\*kwargs)

* **Parameters**

    **filename** – 



* **Returns**

    


#### collection( = 'local-registry')

#### delete(name=None)

* **Parameters**

    **name** – 



* **Returns**

    


#### kind( = 'register')

#### list(name=None)

* **Parameters**

    **name** – if none all



* **Returns**

    


#### output( = {'register': {'header': ['Name', 'Status', 'Url', 'Pid'], 'order': ['cm.name', 'status', 'url', 'pid'], 'sort_keys': ['cm.name']}})

#### start()
start the registry

possibly not needed as we have cms start


* **Returns**

    


#### stop()
stop the registry

possibly not needed as we have cms start
this will not just sto the registry but mongo


* **Returns**

    

## openapi.registry.cache module


### class openapi.registry.cache.ResultCache()
Bases: `object`


#### \__init__()
Initialize self.  See help(type(self)) for accurate signature.


#### load(name)
Load cached model


* **Parameters**

    **name** – 



* **Returns**

    


#### save(\*\*kwargs)
## openapi.registry.fileoperation module


### class openapi.registry.fileoperation.FileOperation()
Bases: `object`


#### file_upload()
