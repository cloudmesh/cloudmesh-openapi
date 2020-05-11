Cloudmesh OpenAPI Service Generator
===================================

   **Note:** The README.md page is outomatically generated, do not edit
   it. To modify change the content in
   https://github.com/cloudmesh/cloudmesh-openapi/blob/master/README-source.md
   Curley brackets must use two in README-source.md

|image| |Python| |License| |Format| |Status| |Travis|

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

Make sure that ``cloudmesh`` is properly installed on your machine and
you have mongodb setup to work with cloudmesh.

More details to setting up ``mongo`` can be found in the

-  `Cloudmesh
   Manual <https://cloudmesh.github.io/cloudmesh-manual/installation/install.html>`__

User Installation
~~~~~~~~~~~~~~~~~

Make sure you use a python venv before installing. Users can install the
code with

.. code:: bash

   python -m venv ~/ENV3
   source ~/ENV3/bin/activate # on windows ENV3\Scripts\activate
   mkdir cm
   cd cm
   pip installl cloudmesh-installer get openapi 
   cms help
   cms gui quick
   # fill out mongo variables
   # make sure autinstall is True
   cms admin mongo install --force

.. code:: bash

   $ pip install cloudmesh-openapi

Developer Installation
~~~~~~~~~~~~~~~~~~~~~~

Developers install also the source code

.. code:: bash

   python -m venv ~/ENV3
   source ~/ENV3/bin/activate # on windows ENV3\Scripts\activate
   mkdir cm
   cd cm
   pip install cloudmesh-installer
   cloudmesh-installer get openapi 
   cms help
   cms gui quick
   # fill out mongo variables
   # make sure autinstall is True
   cms admin mongo install --force

Overview
--------

When getting started using the ``openapi``, please first call:

::

   cms help openapi

This will show the available functions and options. For your convenience
we include the manual page later on in this document.

Quick steps to generate,start and stop CPU sample example
---------------------------------------------------------

Navigate to ~/cm/cloudmesh-openapi folder and run following commands

Generate yaml file
~~~~~~~~~~~~~~~~~~

::

   cms openapi generate get_processor_name --filename=./tests/server-cpu/cpu.py

Start server
~~~~~~~~~~~~

::

   cms openapi server start ./tests/server-cpu/cpu.yaml

Issue a Request
~~~~~~~~~~~~~~~

::

   curl -X GET "http://localhost:8080/cloudmesh/get_processor_name" -H "accept: text/plain"

Stop server
~~~~~~~~~~~

::

   cms openapi server stop cpu

End-to-end walkthrough
----------------------

Writing Python
~~~~~~~~~~~~~~

Cloudmesh uses introspection to generate an OpenAPI compliant YAML
specification that will allow your Python code to run as a web service.
For this reason, any code you write must conform to a set of guidelines.

-  The parameters and return values of any functions you write must use
   typing
-  Your functions must include docstrings
-  If a function uses or returns a class, that class must be defined as
   a dataclass in the same file

The following function is a great example to get started. Note how x, y,
and the return value are all typed. In this case they are all ``float``,
but other types are supported. The description in the docstring will be
added to your YAML specification to help describe what the function
does.

.. code:: python

   def add(x: float, y: float) -> float:
       """
       adding float and float.
       :param x: x value
       :type x: float
       :param y: y value
       :type y: float
       :return: result
       :return type: float
       """
       return x + y

Generating OpenAPI specification
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Once you have a Python function you would like to deploy as a web
service, you can generate the OpenAPI specification. Navigate to your
.py file’s directory and generate the YAML. This will print information
to your console about the YAML file that was generated.

::

   $ cms openapi generate [function_name] --filename=[filename.py]

If you would like to include more than one function in your web service,
like addition and subtraction, use the ``--all_functions`` flag. This
will ignore functions whose names start with ‘\_’.

.. code:: bash

   $ cms openapi generate --filename=[filename.py] --all_functions

You can even write a class like Calculator that contains functions for
addition, subtraction, etc. You can generate a specification for an
entire class by using the ``--import_class`` flag.

.. code:: bash

   $ cms openapi generate [ClassName] --filename=[filename.py] --import_class

Starting a server
~~~~~~~~~~~~~~~~~

Once you have generated a specification, you can start the web service
on your localhost by providing the path to the YAML file. This will
print information to your console about the server

::

   $ cms openapi server start ./[filename.yaml]

     Starting: [server name]
     PID:      [PID]
     Spec:     ./[filename.py]
     URL:      http://localhost:8080/cloudmesh
     Cloudmesh UI:      http://localhost:8080/cloudmesh/ui
     

Sending requests to the server
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Now you have two options to interact with the web service. The first is
to navigate the the Cloudmesh UI and click on each endpoint to test the
functionality. The second is to use curl commands to submit requests.

::

   $ curl -X GET "http://localhost:8080/cloudmesh/add?x=1.2&y=1.5" -H "accept: text/plain"
   2.7

Stopping the server
~~~~~~~~~~~~~~~~~~~

Now you can stop the server using the name of the server. If you forgot
the name, use ``cms openapi server ps`` to get a list of server
processes.

::

   $ cms openapi stop [server name]

Manual
------

.. code:: bash

Pytests
-------

Please follow `Pytest Information <tests/README.md>`__ document for
pytests related information

Examples
--------

One function in python file
~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Please check `Python file <tests/server-cpu/cpu.py>`__.

2. Run below command to generate yaml file and start server

::

   cms openapi generate get_processor_name --filename=./tests/server-cpu/cpu.py

Multiple functions in python file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Please check `Python
   file <tests/generator-calculator/calculator.py>`__

2. Run below command to generate yaml file and start server

::

   cms openapi generate --filename=./tests/generator-calculator/calculator.py --all_functions

::

   cms openapi generate server start ./tests/generator-calculator/calculator.py

Function(s) in python class file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Please check `Python
   file <tests/generator-testclass/calculator.py>`__

2. Run below command to generate yaml file and start server

::

   cms openapi generate --filename=./tests/generator-testclass/calculator.py --import_class"

::

   cms openapi generate server start ./tests/generator-testclass/calculator.py

Uploading data
~~~~~~~~~~~~~~

Code to handle uploads is located in
cloudmesh-openapi/tests/generator-upload. The code snippet in
uploadexample.py and the specification in uploadexample.yaml can be
added to existing projects by adding the ``--enable_upload`` flag to the
``cms openapi generate`` command. The web service will be able to
retrieve the uploaded file from ~/.cloudmesh/upload-file/.

Upload example
^^^^^^^^^^^^^^

This example shows how to upload a CSV file and how the web service can
retrieve it.

First, generate the OpenAPI specification and start the server

::

   cms openapi generate print_csv2np --filename=./tests/generator-upload/csv_reader.py --enable_upload
   cms openapi server start ./tests/generator-upload/csv_reader.yaml

Next, navigate to localhost:8080/cloudmesh/ui. Click to open the /upload
endpoint, then click ‘Try it out.’ Click to choose a file to upload,
then upload ``tests/generator-upload/np_test.csv``. Click ‘Execute’ to
complete the upload.

The uploaded file will be located at
``~/.cloudmesh/upload-file/[filename]``.
``tests/generator-upload/csv_reader.py`` contains some example code to
retrieve the array in the uploaded file. To see this in action, click to
open the /print_csv2np endpoint, then click ‘Try it out.’ Enter
“np_test.csv” in the field that prompts for a filename, and then click
Execute to view the numpy array defined by the CSV file.

Downloading data
~~~~~~~~~~~~~~~~

Always the same

abc.txt <- /data/xyz/klmn.txt

Merge openapi’s
~~~~~~~~~~~~~~~

::

   merge [APIS...] - > single.yaml

Running AI Services in the Cloud using OpenApi
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Google
^^^^^^

After you create your google cloud account, it is recommended to
download and install Google’s `Cloud
SDK <https://cloud.google.com/sdk/docs/quickstarts>`__. This will enable
CLI. Make sure you enable all the required services.

For example:

::

   gcloud services enable servicemanagement.googleapis.com

::

   gcloud services enable endpoints.googleapis.com

and any other services you might be using for your specific Cloud API
function.

To begin using the tests for any of the Google Cloud Platform AI
services you must first set up a Google account (set up a free tier
account): `Google Account
Setup <https://cloud.google.com/billing/docs/how-to/manage-billing-account>`__

After you create your google cloud account, it is recommended to
download and install Google’s `Cloud
SDK <https://cloud.google.com/sdk/docs/quickstarts>`__. This will enable
CLI. Make sure you enable all the required services.

For example:

::

   gcloud services enable servicemanagement.googleapis.com

::

   gcloud services enable servicecontrol.googleapis.com

::

   gcloud services enable endpoints.googleapis.com

and any other services you might be using for your specific Cloud API
function.

It is also required to install the cloudmesh-cloud package, if not
already installed:

.. code:: bash

   cloudmesh-installer get cloud
   cloudmesh-installer install cloud

This will allow you automatically fill out the cloudmesh yaml file with
your credentials once you generate the servcie account JSON file.

After you have verified your account is created you must then give your
account access to the proper APIs and create a project in the Google
Cloud Platform(GCP) console.

1. Go to the `project
   selector <console.cloud.google.com/projectselector2/home/>`__

2. Follow directions from Google to create a project linked to your
   account

Quickstart Google Python API
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

   pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

-  For quickstart in using Google API for Python visit
   `here <https://developers.google.com/docs/api/quickstart/python>`__

Setting up your Google account
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Before you generate the service account JSON file for your account you
will want to enable a number of services in the GCP console.

-  Google Compute
-  Billing
-  Cloud Natural Language API
-  Translate API

1. To do this you will need to click the menu icon in the Dashboard
   navigation bar. Ensure you are in the correct porject.

2. Once that menu is open hover over the “APIs and Services” menu item
   and click on “Dashboard” in the submenu.

3. At the dashboard click on the “+ Enable APIs and Services” button at
   the top of the dashboard

4. Search for **cloud natural language** to find the API in the search
   results and click the result

5. Once the page opens click “Enable”

6. Do the same for the **translate** API to enable that as well

7. Do the same for the **compute engine API** to enable that as well

You must now properly set up the account roles to ensure you will have
access to the API. Follow the directions from Google to `set up proper
authentication <https://cloud.google.com/natural-language/docs/setup#auth>`__

Make you account an owner for each of the APIs in the IAM tool as
directed in the authentication steps for the natural language API. This
makes your service account have proper access to the required APIs and
once the private key is downloaded those will be stored there.

It is VERY important that you create a service account and download the
private key as described in the directions from Google. If you do not
the cms google commands will not work properly.

Once you have properly set up your permissions please make sure you
download your JSON private key for the service account that has
permissions set up for the required API services. These steps to
download are found
`here <https://cloud.google.com/natural-language/docs/setup#sa-create>`__.
Please take note of where you store the downloaded JSON and copy the
path string to a easily accessible location.

The client libraries for each API are included in teh requirements.txt
file for the openapi proejct and should be isntalled when the package is
installed. If not, follow directions outlined by google install each
package:

::

   google-cloud-translate
   google-cloud-language

To pass the information from your service account private key file ot
the cloudmesh yaml file run the following command:

.. code:: bash

   cms register update --kind=google --service=compute --filename=<<google json file>>

Running the Google Natural Language and Translate REST Services
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

1. Navigate to the ``~/.cloudmesh`` repo and create a cache directory
   for your text examples you would like to analyze.

   .. code:: bash

      mkdir text-cache

2. Add any plain text files your would like to analyze to this directory
   with a name that has no special characters or spaces. You can copy
   the files at this location,
   ``./cloudmesh-openapi/tests/textanaysis-example-text/reviews/`` into
   the text-cache if you want to use provided examples.

3. Navigate to the ``./cloudmesh-openapi`` directory on your machine

4. Utilize the generate command to create the OpenAPI spec

   .. code:: bash

      cms openapi generate TextAnalysis --filename=./tests/generator-natural-lang/natural-lang-analysis.py --all_functions

5. Start the server after the yaml file is generated ot the same
   directory as the .py file

   .. code:: bash

      cms openapie start server ./tests/generator-natural-lang/natural-lang-analysis.yaml

6. Run a curl command against the newly running server to verify it
   returns a result as expected.

   -  Sample text file name is only meant to be the name of the file not
      the full path.

   .. code:: bash

      curl -X GET "http://127.0.0.1:8080/cloudmesh/analyze?filename=<<sample text file name>>&cloud=google"

   -  This is currently only ready to translate a single word through
      the API.

   .. code:: bash

      curl -X GET "http://127.0.0.1:8080/cloudmesh/translate_text?cloud=google&text=<<word to translate>>&lang=<<lang code>>"

7. Stop the server

   .. code:: bash

      cms openapi server stop natural-lang-analysis

AWS
^^^

Sign up for AWS

-  Go to https://portal.aws.amazon.com/billing/signup
-  Follow online instructions

Create an IAM User

-  For instructions, see
   `here <https://docs.aws.amazon.com/IAM/latest/UserGuide/getting-started_create-admin-group.html>`__

Set up AWS CLI and AWS SDKs

-  To download and instructions to install AWS CLI, see
   `here <https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install>`__

Install Boto 3

.. code:: bash

   pip install boto3

-  For quickstart, vist
   `here <https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html>`__

As long as you enable all the services you need for using AWS AI APIs
you should be able to write your functions for OpenAPI

Azure
^^^^^

Setting up Azure Sentiment Analysis and Translation Services
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

1.  Create an Azure subscription. If you don’t have one, create a `free
    account <https://azure.microsoft.com/try/cognitive-services/>`__

2.  Create a `Text Analysis
    resource <https://portal.azure.com/#create/Microsoft.CognitiveServicesTextAnalytics>`__

    -  This link will require you to be logged in to the Azure portal

3.  Create a `Translation
    Resource <https://docs.microsoft.com/en-us/azure/cognitive-services/cognitive-services-apis-create-account?tabs=multiservice%2Cwindows>`__

4.  The microsoft packages are included in the openapi package
    requirements file so they should be installed. If they are not,
    install the following:

    ::

       pip install msrest
       pip install azure-ai-textanalytics

5.  Navigate to the ``~/.cloudmesh`` repo and create a cache directory
    for your text examples you would like to analyze.

    .. code:: bash

       mkdir text-cache

6.  Add any plain text files your would like to analyze to this
    directory with a name that has no special characters or spaces. You
    can copy the files at this location,
    ``./cloudmesh-openapi/tests/textanaysis-example-text/reviews/`` into
    the text-cache if you want to use provided examples.

7.  Navigate to the ``./cloudmesh-openapi`` directory on your machine

8.  Utilize the generate command to create the OpenAPI spec

    .. code:: bash

       cms openapi generate TextAnalysis --filename=./tests/generator-natural-lang/natural-lang-analysis.py --all_functions

9.  Start the server after the yaml file is generated ot the same
    directory as the .py file

    .. code:: bash

       cms openapie start server ./tests/generator-natural-lang/natural-lang-analysis.yaml

10. Run a curl command against the newly running server to verify it
    returns a result as expected.

    -  Sample text file name is only meant to be the name of the file
       not the full path.

    .. code:: bash

       curl -X GET "http://127.0.0.1:8080/cloudmesh/analyze?filename=<<sample text file name>>&cloud=azure"

    -  This is currently only ready to translate a single word through
       the API.
    -  Available language tags are described in the `Azure
       docs <https://docs.microsoft.com/en-us/azure/cognitive-services/translator/reference/v3-0-languages>`__

    .. code:: bash

       curl -X GET "http://127.0.0.1:8080/cloudmesh/translate_text?cloud=azure&text=<<word to translate>>&lang=<<lang code>>"

11. Stop the server

    .. code:: bash

       cms openapi server stop natural-lang-analysis

The natural langauge analysis API can be improved by allowing for full
phrase translation via the API. If you contribute to this API there is
room for improvement to add custom translation models as well if
preferred to pre-trained APIs.

Setting up Azure ComputerVision AI services
'''''''''''''''''''''''''''''''''''''''''''

Prerequisite
            

Using the Azure Computer Vision AI service, you can describe, analyze
and/ or get tags for a locally stored image or you can read the text
from an image or hand-written file.

-  Azure subscription. If you don’t have one, create a `free
   account <https://azure.microsoft.com/try/cognitive-services/>`__
   before you continue further.
-  Create a Computer Vision resource and get the
   COMPUTER_VISION_SUBSCRIPTION_KEY and COMPUTER_VISION_ENDPOINT. Follow
   `instructions <https://docs.microsoft.com/en-us/azure/cognitive-services/cognitive-services-apis-create-account?tabs=singleservice%2Cunix>`__
   to get the same.
-  Install following Python packages in your virtual environment:

   -  requests
   -  Pillow

-  Install Computer Vision client library

.. code:: bash

     pip install --upgrade azure-cognitiveservices-vision-computervision

Steps to implement and use Azure AI image and text *REST-services*
                                                                  

-  Go to ``./cloudmesh-openapi`` directory

-  Run following command to generate the YAML files

.. code:: bash

     cms openapi generate AzureAiImage --filename=./tests/generator-azureai/azure-ai-image-function.py --all_functions --enable_upload
     cms openapi generate AzureAiText --filename=./tests/generator-azureai/azure-ai-text-function.py --all_functions --enable_upload

-  Verify the *YAML* files created in ``./tests/generator-azureai``
   directory

.. code:: bash

     azure-ai-image-function.yaml
     azure-ai-text-function.yaml

-  Start the REST service by running following command in
   ``./cloudmesh-openapi`` directory

.. code:: bash

     cms openapi server start ./tests/generator-azureai/azure-ai-image-function.yaml

The default port used for starting the service is 8080. In case you want
to start more than one REST service, use a different port in following
command:

.. code:: bash

     cms openapi server start ./tests/generator-azureai/azure-ai-text-function.yaml --port=<**Use a different port than 8080**>

-  Access the REST service using http://localhost:8080/cloudmesh/ui/

-  After you have started the azure-ai-image-function or
   azure-ai-text-function on default port 8080, run following command to
   upload the image or text_image file

.. code:: bash

     curl -X POST "http://localhost:8080/cloudmesh/upload" -H  "accept: text/plain" -H  "Content-Type: multipart/form-data" -F "upload=@tests/generator-azureai/<image_name_with_extension>;type=image/jpeg"

Keep your test image files at ``./tests/generator-azureai/`` directory

-  With *azure-ai-text-function* started on port=8080, in order to test
   the azure ai function for text detection in an image, run following
   command

.. code:: bash

     curl -X GET "http://localhost:8080/cloudmesh/azure-ai-text-function_upload-enabled/get_text_results?image_name=<image_name_with_extension_uploaded_earlier>" -H "accept: text/plain"

-  With *azure-ai-image-function* started on port=8080, in order to test
   the azure ai function for describing an image, run following command

.. code:: bash

     curl -X GET "http://localhost:8080/cloudmesh/azure-ai-image-function_upload-enabled/get_image_desc?image_name=<image_name_with_extension_uploaded_earlier>" -H "accept: text/plain"

-  With *azure-ai-image-function* started on port=8080, in order to test
   the azure ai function for analyzing an image, run following command

.. code:: bash

     curl -X GET "http://localhost:8080/cloudmesh/azure-ai-image-function_upload-enabled/get_image_analysis?image_name=<image_name_with_extension_uploaded_earlier>" -H "accept: text/plain"

-  With *azure-ai-image-function* started on port=8080, in order to test
   the azure ai function for identifying tags in an image, run following
   command

.. code:: bash

     curl -X GET "http://localhost:8080/cloudmesh/azure-ai-image-function_upload-enabled/get_image_tags?image_name=<image_name_with_extension_uploaded_earlier>" -H "accept: text/plain"

-  Check the running REST services using following command:

.. code:: bash

     cms openapi server ps

-  Stop the REST service using following command(s):

.. code:: bash

     cms openapi server stop azure-ai-image-function
     cms openapi server stop azure-ai-text-function

Test
----

The following table lists the different test we have, we provide
additional information for the tests in the test directory in a README
file. Summaries are provided below the table

+-----------------------+-----------------------+-----------------------+
| Test                  | Short Description     | Link                  |
+=======================+=======================+=======================+
| Generator-calculator  | Test to check if      | `test_01_generator.py |
|                       | calculator api is     |  <https://github.com/ |
|                       | generated correctly.  | cloudmesh/cloudmesh-o |
|                       | This is to test       | penapi/blob/master/te |
|                       | multiple function in  | sts/generator-calcula |
|                       | one python file       | tor/test_01_generator |
|                       |                       | .py>`__               |
+-----------------------+-----------------------+-----------------------+
| Generator-testclass   | Test to check if      | `test_02_generator.py |
|                       | calculator api is     |  <https://github.com/ |
|                       | generated correctly.  | cloudmesh/cloudmesh-o |
|                       | This is to test       | penapi/blob/master/te |
|                       | multiple function in  | sts/generator-testcla |
|                       | one python class file | ss/test_02_generator. |
|                       |                       | py>`__                |
+-----------------------+-----------------------+-----------------------+
| Server-cpu            | Test to check if cpu  | `test_03_generator.py |
|                       | api is generated      |  <https://github.com/ |
|                       | correctly. This is to | cloudmesh/cloudmesh-o |
|                       | test single function  | penapi/blob/master/te |
|                       | in one python file    | sts/server-cpu/test_0 |
|                       | and function name is  | 3_generator.py>`__    |
|                       | different than file   |                       |
|                       | name                  |                       |
+-----------------------+-----------------------+-----------------------+
| Server-cms            | Test to check if cms  | `test_04_generator.py |
|                       | api is generated      |  <https://github.com/ |
|                       | correctly. This is to | cloudmesh/cloudmesh-o |
|                       | test multiple         | penapi/blob/master/te |
|                       | function in one       | sts/server-cms/test_0 |
|                       | python file.          | 4_generator.py>`__    |
+-----------------------+-----------------------+-----------------------+
| Registry              | test_001_registry.py  | `Link <https://github |
|                       | - Runs tests for      | .com/cloudmesh/cloudm |
|                       | registry. Description | esh-openapi/blob/mast |
|                       | is in tests/README.md | er/tests/README.md>`_ |
|                       |                       | _                     |
+-----------------------+-----------------------+-----------------------+
| Image-Analysis        | image_test.py - Runs  | `image <https://githu |
|                       | benchmark for text    | b.com/cloudmesh/cloud |
|                       | detection for Google  | mesh-openapi/blob/mas |
|                       | Vision API and AWS    | ter/tests/image-analy |
|                       | Rekognition.          | sis/README.md>`__     |
|                       | Description in        |                       |
|                       | image-analysis/README |                       |
|                       | .md                   |                       |
+-----------------------+-----------------------+-----------------------+

For more infromation about test cases ,please check `tests
info <https://github.com/cloudmesh/cloudmesh-openapi/blob/master/tests/README.md>`__

-  `test_001_registry <tests/test_001_registry.py>`__
-  `test_003_server_manage_cpu <tests/test_003_server_manage_cpu.py>`__
-  `test_010_generator <tests/test_010_generator.py>`__
-  `test_011_generator_cpu <tests/test_011_generator_cpu.py>`__
-  `test_012_generator_calculator <tests/test_012_generator_calculator.py>`__
-  `test_015_generator_azureai <tests/test_015_generator_azureai.py>`__
-  `test_020_server_manage <tests/test_020_server_manage.py>`__
-  `test_server_cms_cpu <tests/test_server_cms_cpu.py>`__

.. |image| image:: https://img.shields.io/pypi/v/cloudmesh-openapi.svg
   :target: https://pypi.org/project/cloudmesh-openapi/
.. |Python| image:: https://img.shields.io/pypi/pyversions/cloudmesh-openapi.svg
   :target: https://pypi.python.org/pypi/cloudmesh-openapi
.. |License| image:: https://img.shields.io/badge/License-Apache%202.0-blue.svg
   :target: https://github.com/cloudmesh/cloudmesh-openapi/blob/master/LICENSE
.. |Format| image:: https://img.shields.io/pypi/format/cloudmesh-openapi.svg
   :target: https://pypi.python.org/pypi/cloudmesh-openapi
.. |Status| image:: https://img.shields.io/pypi/status/cloudmesh-openapi.svg
   :target: https://pypi.python.org/pypi/cloudmesh-openapi
.. |Travis| image:: https://travis-ci.com/cloudmesh/cloudmesh-openapi.svg?branch=master
   :target: https://travis-ci.com/cloudmesh/cloudmesh-openapi
