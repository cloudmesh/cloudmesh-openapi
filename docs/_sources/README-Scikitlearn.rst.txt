Cloudmesh OpenAPI Scikit-learn
==============================

Prerequisites
-------------

-  We use recommend Python 3.8.2 Python or newer.
-  We recommend pip version 20.0.2 or newer
-  We recommend that you use a venv (see developer install)
-  MongoDB installed as regular program not as service
-  Please run cim init command to start mongodb server

We have not checked if it works on older versions.

Installation
------------

Make sure to follow the instruction for ``cms openapi``

Overview
--------

When getting started using the ``openapi``, please first call
``cms help openapi`` to see the available functions and options. For
your convenience we include the manual page later on in this document.

Scikit-learn Documentation
--------------------------

Scikit-learn is a Machine learning library in Python.We can choose a ML
algorithm like LinearRegression and cloudmesh will be able to spin up
OPENAPI specification for the library we choose. We can interact with
the Scikit-learn library using either CURL commands or through GUI.

This Version of Scikit-learn service accepts csv files in UTF-8 format
only.It is the user responsibility to make sure the files are in UTF-8
format.It is the user responsiblity to split the data in to train and
test datasets. Split data functionality is not currently supported.

Setting up Scikit-learn service
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1.  Please complete the basic installation of
    `cloudmesh-openapi <https://github.com/cloudmesh/cloudmesh-openapi>`__,
    To make set up easy the same steps are even referenced at the
    Developer Installation section in the document.

2.  You can find Scikit-learn documentation in
    `Scikit-learn <https://scikit-learn.org/dev/modules/classes.html>`__

3.  The following packages needs to be installed to access Scikit-learn

    .. code:: bash

    pip install pandas pip install Scikit-learn

4.  Navigate to the ``./cloudmesh-openapi`` directory on your machine

5.  Utilize the Scikit-learn generate command to create the python file
    which will used to generate OpenAPI spec

    .. code:: bash

    ::

       cms openapi sklearnreadfile sklearn.linear_model.LinearRegression Linregpytest

    The sample generated file can be viewed at
    `tests/generator <https://github.com/cloudmesh/cloudmesh-openapi/tree/main/tests/generator>`__

6.  Utilize the generate command to generate OpenAPI spec with upload
    functionality enabled

    .. code:: bash

    ::

       cms openapi generate --filename=./tests/generator/LinearRegression.py --all_functions --enable_upload

7.  Start the server after the yaml file is generated ot the same
    directory as the .py file

    .. code:: bash

    ::

       cms openapi server start ./tests/generator/LinearRegression.yaml

8.  Access the REST service using http://localhost:8080/cloudmesh/ui/

9.  Run a curl command against the newly running server to upload the
    testfiles.

    Place your test files in
    `Scikitlearn-data <https://github.com/cloudmesh/cloudmesh-openapi/tree/main/tests/Scikitlearn-data>`__
    We are testing with X_SAT.csv(SAT Scores of students),y_GPA(GPA of
    students)

    .. code:: bash

    ::

       curl -X POST "http://localhost:8080/cloudmesh/upload" \
            -H "accept: text/plain" \
            -H "Content-Type: multipart/form-data" \
            -F "upload=@tests/Scikitlearn-data/X_SAT.csv;type=text/csv"


       curl -X POST "http://localhost:8080/cloudmesh/upload" \
            -H "accept: text/plain" \
            -H "Content-Type: multipart/form-data" \
            -F "upload=@tests/Scikitlearn-data/y_GPA.csv;type=text/csv"

10. Run a curl command against the newly running server to verify fit
    method in Scikit-learn using the uploaded files

    .. code:: bash

    ::

       curl -X GET "http://localhost:8080/cloudmesh/LinearRegression_upload-enabled/fit?X=X_SAT&y=y_GPA" -H "accept: */*"

11. Run a curl command against the newly running server to run the
    Predict method.

    .. code:: bash

    ::

       curl -X GET "http://localhost:8080/cloudmesh/LinearRegression_upload-enabled/predict?X=X_SAT" -H "accept: text/plain"

12. Run a curl command against the newly running server to run the Score
    method.

    .. code:: bash

    ::

       curl -X GET "http://localhost:8080/cloudmesh/LinearRegression_upload-enabled/score?X=X_SAT&y=y_GPA" -H "accept: text/plain"   

13. Stop the server

    .. code:: bash

    ::

       cms openapi server stop LinearRegression
