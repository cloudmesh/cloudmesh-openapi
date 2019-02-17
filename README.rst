OpenAPI merge
=============

IMPORTANT: 

```
cloudmesh.common 

cloudmesh.cmd5
```

MUST BE INSTALLED FROM SOURCE AS THE VERSION ON PYPI IS NOT YET UPDATED


YOu need to have the yaml file in the current directory and execute this program in this directory

An example for yaml files are provided in 

* <https://github.com/cloudmesh-community/nist/tree/master/spec>

YOu can download some examples, as well as the `.header.yaml` file you will need with for example curl 

Once you have `user.yaml` `timestap.yaml` and `.header.yaml` in your directory you can say

```bash
$ cms openapi description user timestamp
```

Please note that this script does not yet rewrite the `$ref` appropriately, but if you like to help you can do so.
