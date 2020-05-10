###############################################################
# pytest -v --capture=no ./tests/generator-natural-lang/test_generator_natural_language.py
# pytest -v  ./tests/generator-natural-lang/test_generator_natural_language.py
# pytest -v --capture=no  ./tests/generator-natural-lang/test_generator_natural_language.py::TestGenerator::<METHODNAME>
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
import sys
sys.path.append("./tests/lib")
from generator_test import GeneratorBaseTest, ServerBaseTest

sys.path.append("./tests/lib")
filename="./tests/generator-natural-lang/natural-lang-analysis.py"
all_functions=True
import_class=False

#Replace test_dir with location of your cloudmesh install
test_dir = "/Users/andrewgoldfarb/e516-spring/cm/cloudmesh-openapi/tests/generator-natural-lang/"
func_filename = "natural-lang-analysis.py"
yaml_filename = "natural-lang-analysis.yaml"
sample_text_file = "bladerunner-neg.txt"
example_text_directory="/Users/andrewgoldfarb/.cloudmesh/text-cache/"
ssh_keys = "/Users/andrewgoldfarb/Desktop/project-keys.txt"

func_path = test_dir + func_filename
yaml_path = test_dir + yaml_filename

service = 'openapi'

user = Config()["cloudmesh.profile.user"]
variables = Variables()
VERBOSE(variables.dict())

pub_key = variables['pub_key']
priv_key = variables['priv_key']
google_sa = variables['google_sa_path']

cloud = variables.parameter('cloud')

vm_info = {}

print(f"Test run for {cloud}")

if cloud is None:
    raise ValueError("cloud is not not set")

name_generator = Name()
name_generator.set(f"test-{user}-vm-" + "{counter}")

name = str(name_generator)

provider = Provider(name=cloud)

username = "andrewgoldfarb"

startup_script = "/Users/andrewgoldfarb/e516-spring/cm/get/ubuntu19.10/index.html"
vm_location_script = "text-analysis-startup-script.sh"

Benchmark.debug()

@pytest.mark.incremental
class TestGenerator():

    @pytest.fixture(scope="module")
    def generatorBaseTestFixture(self):
        gen = GeneratorBaseTest(filename, all_functions, import_class)
        return gen

    @pytest.fixture(scope="module")
    def serverBaseTestFixture(self):
        server = ServerBaseTest()
        return server

    def test_copy_file(self, generatorBaseTestFixture):
        generatorBaseTestFixture.copy_py_file()

    def test_generate(self, generatorBaseTestFixture):
        """
        function to validate paths information
        """
        generatorBaseTestFixture.generate()

    def test_read_spec(self, generatorBaseTestFixture):
        generatorBaseTestFixture.read_spec()

    # def test_validate_function(self, generatorBaseTestFixture):
    #     generatorBaseTestFixture.validate_function()

    def test_start_service(self, serverBaseTestFixture):
        serverBaseTestFixture.start_service()

    def test_run_analyze_google(self):
        HEADING()
        Benchmark.Start()
        res_code = ""

        while res_code != "200":

            response_google = requests.get(
                f"http://localhost:8080/cloudmesh/natural-lang-analysis/analyze?filename={sample_text_file}&cloud=google")
            res_code = str(response_google.status_code)
        Benchmark.Stop()
        assert res_code == "200"


    def test_run_analyze_azure(self):
        HEADING()
        Benchmark.Start()
        res_code = ""

        while res_code != "200":
            response_azure = requests.get(
                f"http://localhost:8080/cloudmesh/natural-lang-analysis/analyze?filename={sample_text_file}&cloud=azure")
            res_code = str(response_azure.status_code)
        Benchmark.Stop()
        assert res_code == "200"

    # def test_run_translate_google(self):
    #     HEADING()
    #     Benchmark.Start()
    #     res_code = ""
    #     text = "Testing"
    #     lang = "it"
    #
    #     while res_code != "200":
    #         response_google = requests.get(
    #             f"http://127.0.0.1:8080/cloudmesh/natural-lang-analysis/translate_text?cloud=google&text={text}&lang={lang}")
    #         print(response_google)
    #         res_code = str(response_google.status_code)
    #
    #         Benchmark.Stop()
    #
    #     assert res_code == "200"
    #
    # def test_run_translate_azure(self):
    #     HEADING()
    #     Benchmark.Start()
    #     res_code = ""
    #     text = "I am testing for cloudmesh on Azure"
    #     lang = "it"
    #
    #     while res_code != "200":
    #         response_azure = requests.get(
    #             f"http://127.0.0.1:8080/cloudmesh/natural-lang-analysis/translate_text?cloud=azure&text={text}&lang={lang}")
    #         print(response_azure)
    #         res_code = str(response_azure.status_code)
    #
    #         Benchmark.Stop()
    #
    #     assert res_code == "200"


    def test_stop_server(self, serverBaseTestFixture):
        serverBaseTestFixture.stop_server()

    def test_delete_build_file(self, generatorBaseTestFixture):
       generatorBaseTestFixture.delete_file()

    def test_benchmark(self):
        Benchmark.print(sysinfo=True, csv=True, tag=service)
#
@pytest.mark.incremental
class TestVM:
    def test_provider_vm_create(self):
        HEADING()
        os.system(f"cms vm list --cloud={cloud}")
        # replace with provider.list
        name_generator.incr()
        Benchmark.Start()
        data = provider.create(key=pub_key)
        # provider.wait()
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
        #
        #
        command = f'scp -r -i {priv_key} {example_text_directory} {username}@{external_IP}:./.cloudmesh/'
        upload_service_account = f'scp -i {priv_key} {google_sa} {username}@{external_IP}:.'

        google_sa_vm = "./cloudmesh-final-project-53d3e59c4d15.json"
        add_ssh_keys = f'gcloud compute project-info add-metadata --metadata-from-file ssh-keys={ssh_keys}'
        register_google =f"cms register update --kind=google --service=compute --filename={google_sa_vm}"

        Shell.run(command)
        Shell.run(upload_service_account)
        Shell.run(add_ssh_keys)

        command_2 = f'ssh -i {priv_key} {username}@{external_IP} | {register_google}'

        Shell.run(command_2)









