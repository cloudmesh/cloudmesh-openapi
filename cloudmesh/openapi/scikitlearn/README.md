# Scikit-learn GeneratorFile


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



## Pytests for Scikit learn tests.

* Generate the .py for the Scikit learn module

  pytest -v --capture=no tests/Scikitlearn_tests/test_06a_sklearngeneratortest.py

* Running Pytests for the LinearRegression.py generated from 6a pytest

  pytest -v --capture=no tests/Scikitlearn_tests/test_06b_sklearngeneratortest.py

 
## Pytests for Scikit learn tests.

* Generate the .py for the Scikit learn module woth file reading capabilities

  pytest -v --capture=no tests/Scikitlearn_tests/test_06c_sklearngeneratortest.py

* Running Pytests for the LinearRegression.py generated from 6d pytest
