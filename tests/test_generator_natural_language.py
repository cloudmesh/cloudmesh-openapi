###############################################################
# pytest -v --capture=no tests/test_generator_natural_language.py
# pytest -v  tests/test_generator_natural_language.py
# pytest -v --capture=no  ./tests/test_generator_natural_language.py::TestGenerator::<METHODNAME>
###############################################################

import time, os, pytest, requests
from cloudmesh.common.Shell import Shell
from cloudmesh.common.debug import VERBOSE
from cloudmesh.common.util import HEADING
from cloudmesh.common.variables import Variables
from cloudmesh.common.Benchmark import Benchmark
from cloudmesh.compute.vm.Provider import Provider
from cloudmesh.configuration.Config import Config
from cloudmesh.management.configuration.name import Name


Benchmark.debug()

test_dir = "./tests/generator-natural-lang/"
func_filename = "natural-lang-analysis.py"
yaml_filename = "natural-lang-analysis.yaml"
sample_text_file = "bladerunner-neutral.txt"

func_path = test_dir + func_filename
yaml_path = test_dir + yaml_filename

service = 'openapi'

user = Config()["cloudmesh.profile.user"]
variables = Variables()
VERBOSE(variables.dict())

key = variables['key']

cloud = variables.parameter('cloud')

vm_info = {}

print(f"Test run for {cloud}")

if cloud is None:
    raise ValueError("cloud is not not set")

name_generator = Name()
name_generator.set(f"test-{user}-vm-" + "{counter}")

name = str(name_generator)

provider = Provider(name=cloud)

username = "andrew_goldfarb1"

@pytest.mark.incremental
class TestGenerator:

    def test_generate_individual_function(self):
        HEADING()

        Benchmark.Start()

        Shell.run(
            f"cms openapi generate analyze --filename={func_path}")

        file_list = Shell.run(f"ls {test_dir}")

        assert yaml_filename in file_list

        Benchmark.Stop()

    def test_provider_vm_create(self):
        HEADING()
        os.system(f"cms vm list --cloud={cloud}")
        name_generator.incr()
        Benchmark.Start()
        data = provider.create(key=key)
        Benchmark.Stop()
        # print(data)
        VERBOSE(data)
        name = str(Name())
        status = provider.status(name=name)[0]
        print(f'status: {str(status)}')
        if cloud == 'oracle':
            assert status["cm.status"] in ['STARTING', 'RUNNING', 'STOPPING',
                                           'STOPPED']
        else:
            assert status["cm.status"] in ['ACTIVE', 'RUNNING', 'BOOTING',
                                           'TERMINATED', 'STOPPED']

        external_IP = data[0]['ip_public']
        vm_instance = data[0]['name']
        # Shell.run(f"gcloud compute scp {yaml_path} {vm_instance}:~")
        #
        # print("completed test")





    def test_start_server_from_generated(self):
        HEADING()
        Benchmark.Start()

        os.system(f"cms openapi server start {yaml_path}")

        res_code = ""
        while res_code != "200":

            response_google = requests.get(
                f"http://127.0.0.1:8080/cloudmesh/analyze?filename={sample_text_file}&cloud=google")
            res_code = str(response_google.status_code)
            assert res_code == "200"

            response_azure = requests.get(
                f"http://127.0.0.1:8080/cloudmesh/analyze?filename={sample_text_file}&cloud=azure")
            res_code = str(response_azure.status_code)
            assert res_code == "200"


        Benchmark.Stop()


    def test_stop_server(self):
        HEADING()
        Benchmark.Start()

        output = Shell.run("cms openapi server stop analyze")
        Benchmark.Stop()
        assert "shutting down server analyze" in output

    def test_benchmark(self):
        Benchmark.print(sysinfo=True, csv=True, tag=service)









