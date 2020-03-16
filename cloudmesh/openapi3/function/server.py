import os
import subprocess
import sys
import textwrap
import yaml
from datetime import date
from importlib import import_module

import connexion
from cloudmesh.common.Shell import Shell
from cloudmesh.common.console import Console
from cloudmesh.common.debug import VERBOSE
from cloudmesh.common.util import path_expand
from cloudmesh.openapi3.registry.Registry import Registry


def daemon(func):
    def wrapper(*args, **kwargs):
        pid = os.fork()

        if pid != 0:
            print ("Deamon PID", pid)

        if pid: return
        r = func(*args, **kwargs)

        os._exit(os.EX_OK)
    return wrapper

def dynamic_import(abs_module_path, class_name):
    module_object = import_module(abs_module_path)
    target_class = getattr(module_object, class_name)
    return target_class

class Server(object):

    @staticmethod
    def get_name(name, spec):
        if name is None:
            return os.path.basename(spec).replace(".yaml", "")
        else:
            return name

    def __init__(self,
                 name=None,
                 spec=None,
                 directory=None,
                 host="127.0.0.1",
                 server="flask",
                 port=8080,
                 debug=True):
        if spec is None:
            Console.error("No service specification file defined")
            raise FileNotFoundError


        self.spec = path_expand(spec)

        if directory is None:
            self.directory = os.path.dirname(self.spec)
        else:
            self.directory = directory

        self.name = Server.get_name(name, self.spec)

        self.host = host
        self.port = port
        self.debug = debug
        self.server = server or "flask"
        self.server_command = ""

        data = dict(self.__dict__)
        #data['import'] = __name__

        VERBOSE(data, label="Server parameters")

        if server == "tornado":
            try:
                import tornado
            except Exception as e:
                print(e)
                Console.error(
                    "tornado not install. Please use `pip install tornado`")
                sys.exit(1)
                return ""
            if self.debug:
                Console.error("Tornado does not support --verbose")
                sys.exit(1)
                return ""

        Console.ok(self.directory)


    @daemon
    def _run_deamon(self):
        self._run_app()

    def _run_app(self):
        Console.ok("starting server")

        sys.path.append(self.directory)
        app = connexion.App(__name__,
                            specification_dir=self.directory)

        # ### app.add_cls(self.directory)
        app.add_api(self.spec)
        r = app.run(host=self.host,
                    port=self.port,
                    debug=self.debug,
                    server=self.server)



    def start(self, name=None, spec=None, foreground=False):
        if foreground:
            self._run_app()
        else:
            self._run_deamon()
        name = Server.get_name(name, spec)
        pid = Server.ps(name=name)[1]["pid"]
        _spec = Server.ps(name=name)[1]["spec"]

        with open(_spec, "r") as stream:
            try:
                details = yaml.safe_load(stream)
            except yaml.YAMLError as e:
                print(e)
                assert False, "Yaml file has syntax error"

        url = details["servers"][0]["url"]

        print()
        print("   Starting:", name)
        print("   PID:     ", pid)
        print("   Spec:    ", _spec)
        print("   URL:     ", url)

        print()

        registry = Registry()
        registry.add_form_file(details,
                               pid=pid,
                               spec=_spec,
                               directory=self.directory,
                               port=self.port,
                               host=self.host,
                               url=url
                               )

        return pid

    @staticmethod
    def ps(name=None):
        pids = []
        result = Shell.ps().splitlines()
        result = Shell.find_lines_with(result, "openapi3 server start")

        for p in result:
            pid, rest = p.strip().split(" ", 1)
            info = p.split("start")[1].split("--")[0].strip()
            if name is None:
                name = os.path.basename(rest.split("openapi3 server start")[1]).split(".")[0]
            if name is not None and f"{name}.yaml" in info:
                pids.append({"name":name, "pid": pid, "spec": info})
            else:
                pids.append({"name":name, "pid": pid, "spec": info})
        return pids

    @staticmethod
    def stop(name=None):
        Console.ok(f"shutting down server {name}")

        registry = Registry()

        result = Server.ps(name=None)

        try:
            pid = result[0]["pid"]
            if len(pid) > 0:
                print ("Killing:", pid)
                Shell.kill(pid)
                registry.delete(name=name)
            else:
                print()
                Console.error(f"No Cloudmesh OpenAPI Server found with the name {name}")
        except:
            print("got to exception")
            Console.error(
                f"No Cloudmesh OpenAPI Server found with the name {name}")

    def _run_os(self):
        Console.ok("starting server")

        # If windows convert backslashes to forward slashes to be python compatible
        if sys.platform == 'win32':
            self.spec = "/".join(self.spec.replace('C:', '').split('\\'))
            self.directory = "/".join(self.directory.replace('C:', '').split('\\'))

        today_dt = date.today().strftime("%m%d%Y")
        VERBOSE("spec path: ", self.spec)

        flask_script = textwrap.dedent(f'''
                import connexion
    
                # Create the application instance
                app = connexion.App(__name__, specification_dir='{self.directory}')
    
                # Read the yaml file to configure the endpoints
                app.add_api('{self.spec}')
    
                if __name__ == '__main__':
                    app.run(host='{self.host}',
                            port={self.port},
                            debug={self.debug},
                            server={self.server})
            ''')

        VERBOSE("server script: ", f"{self.directory}/{self.name}_server.py")

        # Write out flask python script to file so that it can be run in background
        try:
            version = open(f"{self.directory}/{self.name}_server.py", 'w').write(
                flask_script)
        except IOError:
            Console.error("Unable to write server file")
        except Exception as e:
            print(e)

        # Run python flask script in background
        try:
            # TODO: need to write log somewhere else or use a logger to write to common log

            logname = f"{self.directory}/{self.name}_server.{today_dt}.log"

            f = open(logname, "w")
            process = subprocess.Popen([sys.executable,
                                        f"{self.directory}/{self.name}_server.py"],
                                       stdout=f,
                                       stderr=f,
                                       shell=False);

            # Write PID file
            pidfile = open(f"{self.directory}/{self.name}_server.pid", 'w')
            pidfile.write(str(process.pid))
        except Exception as e:
            Console.error("Unable to start server")
            print(e)



