# OpenAPI3 Sklearn Generator



## Function read directly from Sklearn libraries.

* Jagadeesh Kandimalla

    * The generatorfromsklearnlibrary.py is the generator function which spits the api from the 
       sklearn library
    * The function input parameters are (module, function, baseurl, outdir, yaml, write=True),
       The module pertains to library it is using like sklearn and function is like LinearRegression
       ,Logisitic Regression.
    * SKlearn uses numpydoc format in the docstring so the scraping of the parameters and docstrings
      are done using docscrape from numpydoc.
    * This code is based on the generator function intially developed.But the generator function annotatitions
      in the code which is not supported by sklearn libraries,so we used the base code for building the 
      api but docscrape code is introduced to get the params and docstrings.
    * People from pytorch and keras can reuse this code if the docstrings in the library follows numpydoc conventions.
