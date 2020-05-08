# openapi.command package

## Submodules

## openapi.command.openapi module


### class openapi.command.openapi.OpenapiCommand()
Bases: `cloudmesh.shell.command.PluginCommand`


#### do_openapi(args)
```
Usage:
    openapi generate [FUNCTION] --filename=FILENAME
                               [--serverurl=SERVERURL]
                               [--yamlfile=YAML]
                               [--import_class]
                               [--all_functions]
                               [--enable_upload]
                               [--verbose]
    openapi server start YAML [NAME]
                    [--directory=DIRECTORY]
                    [--port=PORT]
                    [--server=SERVER]
                    [--host=HOST]
                    [--verbose]
                    [--debug]
                    [--fg]
                    [--os]
    openapi server stop NAME
    openapi server list [NAME] [--output=OUTPUT]
    openapi server ps [NAME] [--output=OUTPUT]
    openapi register add NAME ENDPOINT
    openapi register filename NAME
    openapi register delete NAME
    openapi register list [NAME] [--output=OUTPUT]
    openapi TODO merge [SERVICES...] [--dir=DIR] [--verbose]
    openapi TODO doc FILE --format=(txt|md)[--indent=INDENT]
    openapi TODO doc [SERVICES...] [--dir=DIR]
    openapi sklearn FUNCTION MODELTAG
    openapi sklearn upload --filename=FILENAME

Arguments:
    FUNCTION  The name for the function or class
    MODELTAG  The arbirtary name choosen by the user to store the Sklearn trained model as Pickle object
    FILENAME  Path to python file containing the function or class
    SERVERURL OpenAPI server URL Default: https://localhost:8080/cloudmesh
    YAML      Path to yaml file that will contain OpenAPI spec. Default: FILENAME with .py replaced by .yaml
    DIR       The directory of the specifications
    FILE      The specification

Options:
    --import_class         FUNCTION is a required class name instead of an optional function name
    --all_functions        Generate OpenAPI spec for all functions in FILENAME
    --debug                Use the server in debug mode
    --verbose              Specifies to run in debug mode
                           [default: False]
    --port=PORT            The port for the server [default: 8080]
    --directory=DIRECTORY  The directory in which the server is run
    --server=SERVER        The server [default: flask]
    --output=OUTPUT        The outputformat, table, csv, yaml, json
                           [default: table]
    --srcdir=SRCDIR        The directory of the specifications
    --destdir=DESTDIR      The directory where the generated code
                           is placed

Description:
  This command does some useful things.

  openapi TODO doc FILE --format=(txt|md|rst) [--indent=INDENT]
      Sometimes it is useful to generate teh openaopi documentation
      in another format. We provide fucntionality to generate the
      documentation from the yaml file in a different formt.

  openapi TODO doc --format=(txt|md|rst) [SERVICES...]
      Creates a short documentation from services registered in the
      registry.

  openapi TODO merge [SERVICES...] [--dir=DIR] [--verbose]
      Merges tow service specifications into a single servoce
      TODO: do we have a prototype of this?


  openapi sklearn sklearn.linear_model.LogisticRegression
      Generates the

  openapi generate [FUNCTION] --filename=FILENAME
                               [--serverurl=SERVERURL]
                               [--yamlfile=YAML]
                               [--import_class]
                               [--all_functions]
                               [--enable_upload]
                               [--verbose]
      Generates an OpenAPI specification for FUNCTION in FILENAME and
      writes the result to YAML. Use --import_class to import a class
      with its associated class methods, or use --all_functions to 
      import all functions in FILENAME. These options ignore functions
      whose names start with '_'. Use --enable_upload to add file
      upload functionality to a copy of your python file and the
      resulting yaml file.

  openapi server start YAML [NAME]
                    [--directory=DIRECTORY]
                    [--port=PORT]
                    [--server=SERVER]
                    [--host=HOST]
                    [--verbose]
                    [--debug]
                    [--fg]
                    [--os]
      starts an openapi web service using YAML as a specification
      TODO: directory is hard coded as None, and in server.py it
        defaults to the directory where the yaml file lives. Can
        we just remove this argument?

  openapi server stop NAME
      stops the openapi service with the given name
      TODO: where does this command has to be started from

  openapi server list [NAME] [--output=OUTPUT]
      Provides a list of all OpenAPI services in the registry

  openapi server ps [NAME] [--output=OUTPUT]
      list the running openapi service

  openapi register add NAME ENDPOINT
      Openapi comes with a service registry in which we can register
      openapi services.

  openapi register filename NAME
      In case you have a yaml file the openapi service can also be
      registerd from a yaml file

  openapi register delete NAME
      Deletes the names service from the registry

  openapi register list [NAME] [--output=OUTPUT]
      Provides a list of all registerd OpenAPI services
```
