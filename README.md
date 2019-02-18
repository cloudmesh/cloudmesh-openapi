OpenAPI merge
=============

IMPORTANT

```
cloudmesh.common  
cloudmesh.cmd5
```

MUST BE INSTALLED FROM SOURCE AS THE VERSION ON PYPI IS NOT YET UPDATED


You need to have the yaml file in the current directory and execute this program in this directory

An example for yaml files are provided in 

* <https://github.com/cloudmesh-community/nist/tree/master/spec>

Please note that the spec dire is containing openapi specifications that are not yet completed or 
are actively worked on. You are invited to participate.

You can download some examples, as well as the `.header.yaml` file you will need with for example curl 

Once you have `user.yaml` `timestap.yaml` and `.header.yaml` in your directory you can say

```bash
$ cms openapi description user timestamp
$ cms openapi merge user timestamp
```

Please note that this script does not yet rewrite the `$ref` appropriately, but if you like to help you can do so.
