# Scikit-learn GeneratorFile

* The SklearnGeneratorFile.py is the generator function which outputs the python file for given
  Sckit-learn Library.
  
* The function takes two inputs

    1.input_sklibrary
    
    2.model_tag
    
*  Examples of the inputs are
   
   input_sklibrary = sklearn.linear_model.LinearRegression(Full model specification)
   model_tag = any name which you want the tag the model instance like LinReg1

*  This Version of Scikit-learn service accepts csv files in UTF-8 format only.It is the user responsibility to make
   sure the files are in UTF-8 format.It is the user responsibility to split the data in to train and test datasets.
   Split data functionality is not currently supported.

*  scikit-learn uses numpydoc format in the docstring so the scraping of the parameters and docstrings
   are done using docscrape from numpydoc.
   
*  All the templates used in the code are based on X and y inputs scikit-learn takes and also based on the
   return type


## Pytests for Scikit learn tests.

*  The below pytest generates the .py file used by generator to do a OPENAPI specification.
  
   [Pytestcode](https://github.com/cloudmesh/cloudmesh-openapi/blob/master/tests/Scikitlearn-tests/test_06c_sklearngeneratortest.py)
   
   ```bash
    pytest -v --capture=no tests/Scikitlearn_tests/test_06c_sklearngeneratortest.py
    ```
 
  
*  The below pytest tests the methods generated .
   
   [Pytestcode](https://github.com/cloudmesh/cloudmesh-openapi/blob/master/tests/Scikitlearn-tests/test_06d_sklearngeneratortest.py)
    
    ```bash
    pytest -v --capture=no tests/Scikitlearn_tests/test_06d_sklearngeneratortest.py
    ```
   

  
