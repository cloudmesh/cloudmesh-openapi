###############################################################
# pytest -v --capture=no tests/test_03_generator.py
# pytest -v  tests/test_03_generator.py
# pytest -v --capture=no  tests/test_generator..py::Test_name::<METHODNAME>
###############################################################
"""
# Headline

Here come document for test

"""
import os
import sys

import requests

sys.path.append("./tests")
import util as util
from cloudmesh.common.Shell import Shell
from importlib import import_module
from cloudmesh.openapi.function.executor import Parameter
import types
from cloudmesh.common.dotdict import dotdict
from cloudmesh.common.Benchmark import Benchmark
from cloudmesh.common.util import HEADING




class GeneratorBaseTest:



    def __init__(self,filename,all_functions,import_class,function_name = None):
        global globalcommandstring  # this will hold command string without build folder
        global globalbuildcommandstring # this will hold command string with build folder
        global globalcommandparameter  # this will hold command string without build parameter information
        global globalbuildcommandparameter  # this will hold command string with build parameter information
        globalcommandparameter = Parameter(self.server_dotdict(self.get_servercommand(filename, all_functions, import_class,function_name)))
        build_dotdict=self.build_dotdict(function_name)
        globalbuildcommandparameter=Parameter(build_dotdict)
        globalbuildcommandstring= self.get_build_servercommand(build_dotdict)
        self.service ="openapi"



    def get_servercommand(self,filename,all_functions,import_class,function_name) -> str:
        serverCommand=""
        if import_class:
          serverCommand=f"cms openapi generate --filename={filename} --import_class"
        elif all_functions:
          serverCommand = f"cms openapi generate --filename={filename} --all_functions"
        else:
          serverCommand = f"cms openapi generate {function_name} --filename={filename}"
        return serverCommand

    def get_build_servercommand(self,build_dotdict) -> str:
        serverCommand=""
        if globalbuildcommandparameter.import_class:
          serverCommand=f"cms openapi generate {build_dotdict.FUNCTION} --filename={build_dotdict['--filename']} --import_class"
        elif globalbuildcommandparameter.all_functions:
          serverCommand = f"cms openapi generate --filename={build_dotdict['--filename']} --all_functions"
        else:
          serverCommand = f"cms openapi generate {build_dotdict.FUNCTION} --filename={build_dotdict['--filename']}"
        return serverCommand

    def server_dotdict(self,serverCommand) -> dotdict:
        if serverCommand.__contains__("generate"):
            words=serverCommand.split()
            dotdictd= dotdict()
            for word in words:
                if "--import_class" in word:
                    dotdictd["import_class"] = True
                    dotdictd["all_functions"] = False
                elif "--all_functions" in word:
                    dotdictd["all_functions"] = True
                    dotdictd["import_class"] = False
                elif "--filename" in word:
                    dotdictd["--filename"] = word.split("=")[1]
            return dotdictd
        if serverCommand.__contains__("server"):
           pass

    def build_dotdict(self,function_name = None) -> dotdict:
        dotdictd = dotdict()

        if  globalcommandparameter.import_class:
            dotdictd["import_class"] = True
            dotdictd["all_functions"] = False
            dotdictd["FUNCTION"] = globalcommandparameter.module_name.capitalize()
        elif globalcommandparameter.all_functions:
            dotdictd["all_functions"] = True
            dotdictd["import_class"] = False
        else:
            dotdictd["all_functions"] = False
            dotdictd["import_class"] = False
            dotdictd["FUNCTION"] = function_name

        dotdictd["--filename"] = globalcommandparameter.module_directory+"/build/"+globalcommandparameter.module_name+".py"


        return dotdictd


    def copy_py_file(self):
        import os
        os.makedirs(globalcommandparameter.module_directory+"/build")
        from shutil import copyfile
        HEADING()
        Benchmark.Start()
        copyfile(globalcommandparameter.filename, globalbuildcommandparameter.filename)
        Benchmark.Stop()


    def generate(self):
        """
        function to validate paths information
        """
        HEADING()
        Benchmark.Start()
        Shell.run(globalbuildcommandstring)
        Benchmark.Stop()

    def read_spec(self):
        """
        function to check if YAML synatx is correct or not
        """
        global spec
        HEADING()
        Benchmark.Start()
        spec = util.readyaml(globalbuildcommandparameter.yamlfile)
        keys = spec.keys()
        Benchmark.Stop()
        assert "openapi" in keys
        assert "info" in keys
        assert "servers" in keys
        assert "paths" in keys


    def validate_function(self):
        """
        function to check number of functions are same in py and yaml file.
        """
        HEADING()
        Benchmark.Start()
        sys.path.append(globalbuildcommandparameter.yamldirectory)
        imported_module = import_module(globalbuildcommandparameter.module_name)
        keys = spec.get('paths')
        paths= keys.keys()
        if (globalbuildcommandparameter.all_functions is True):
            for attr_name in dir(imported_module):
                if type(getattr(imported_module, attr_name)).__name__ == 'function':
                    assert f"/{globalbuildcommandparameter.function}/{attr_name}" in paths
        if (globalbuildcommandparameter.import_class is True):
            class_obj = getattr(imported_module, globalbuildcommandparameter.function)
            for attr_name in dir(class_obj):
                attr = getattr(class_obj, attr_name)
                if isinstance(attr, types.MethodType):
                    assert f"/{globalbuildcommandparameter.function}/{attr_name}" in paths

        Benchmark.Stop()

    def delete_file(self):
        HEADING()
        Benchmark.Start()
        import shutil
        shutil.rmtree(globalcommandparameter.module_directory+"/build")
        Benchmark.Stop()


class ServerBaseTest:

    def start_service(self):
        """
        function to test if the server is started and available to return
        a successful http code
        """
        HEADING()
        Benchmark.Start()
        os.system(f"cms openapi server start {globalbuildcommandparameter.yamlfile}")
        result = requests.get('http://127.0.0.1:8080/cloudmesh/ui')
        Benchmark.Stop()
        assert result.status_code == 200  # find test

    def stop_server(self):
        HEADING()

        Benchmark.Start()
        os.system(f"cms openapi server stop {globalbuildcommandparameter.function}")
        Benchmark.Stop()
        gotException = False;
        try:
            result = requests.get('http://127.0.0.1:8080/cloudmesh/ui')
        except Exception as ex:
            gotException = True
        assert gotException


    def benchmark(self):
        Benchmark.print(sysinfo=True, csv=True, tag=service)
