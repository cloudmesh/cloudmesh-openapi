import os
import subprocess
import sys
import textwrap
from datetime import date
from importlib import import_module
from pathlib import Path

import connexion
import yaml
from cloudmesh.common.Shell import Shell
from cloudmesh.common.console import Console
from cloudmesh.common.debug import VERBOSE
from cloudmesh.common.util import path_expand
from cloudmesh.openapi.registry.Registry import Registry


def daemon(func):
    def wrapper(*args, **kwargs):
        pid = os.fork()
        global daemonpid
        if pid != 0:
            daemonpid = pid
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

        self.name = Server.get_name(name, self.spec)

        if directory is None:
            self.directory = os.path.dirname(self.spec)
        else:
            self.directory = directory




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

    @staticmethod
    def get_name(name, spec):
        if name is None:
            return os.path.basename(spec).replace(".yaml", "")
        else:
            return name

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
        """
        Start up an openapi server

        :param name:
        :param spec:
        :param foreground:
        :return:
        """
        name = Server.get_name(name, spec)
        pid = ""

        if foreground:
            self._run_app()
        else:
            if sys.platform == 'win32':
                pid = self.run_os()
            else:
                self._run_deamon()
                if daemonpid is not None:
                    pid = daemonpid
                else:
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

        result = Shell.ps()
        #result = result.split('\n')
        for pinfo in result:
            if pinfo["cmdline"] is not None:
                line = ' '.join(pinfo["cmdline"])
                if "openapi server start" in line:
                    print(pinfo)
                    info = line.split("start")[1].split("--")[0].strip()
                    if name is None:
                        name = os.path.basename(
                            line.split("openapi server start")[1]
                        ).split(".")[0]
                        pids.append({"name": name, "pid": pinfo['pid'], "spec": info})
                    elif name is not None and f"{name}.yaml" in info:
                        pids.append({"name":name, "pid": pinfo['pid'], "spec": info})
                    else:
                        pids.append({"name":name, "pid": pinfo["pid"], "spec":info})
                elif "cmsoaserver.py" in line and sys.platform == 'win32':
                    info = line.spli("python.exe")[1].strip()
                    if name is None:
                        name = Path(info).stem.split("_")[0].split()
                    pids.append({"name": name, "pid": pinfo['pid'], "spec": info})
        print(pids)
        return pids
        '''for pinfo in result:
            if "openapi server start" in pinfo:
                pinfo = pinfo.split(" ")
                info = pinfo[11]
                if name is None:
                    name = os.path.basename(
                        pinfo[11].split("."))
                if name is not None and name in pinfo:
                    pids.append(
                        {"name": pinfo[12], "pid": pinfo[0], "spec": info})
                else:
                    pids.append(
                        {"name": name, "pid": pinfo[0], "spec": info})
            elif "cmsoaserver.py" in pinfo and sys.platform == 'win32':
                info = pinfo.split("python.exe")[1].strip()
                if name is None:
                    name = Path(info).stem.split("_")[0].strip()
                pids.append({"name": name, "pid": pinfo['pid'], "spec": info})
        return pids'''

    @staticmethod
    def list(name=None):
        """
        Lists the servises registered

        :param name:
        :return:
        """
        registry = Registry()
        result = registry.list(name)

        return result

    @staticmethod
    def stop(name=None):
        """
        Stop a running server

        :param name:
        :return:
        """

        Console.ok(f"shutting down server {name}")

        registry = Registry()

        entries = registry.list(name=name)
        pid = ""
        if len(entries) > 1:
            Console.error(f"Aborting, returned more than one entry from the Registry with the name {name}")
            raise Exception
        elif len(entries) == 1:
            pid = str(entries[0]['pid'])
        else:
            result = Server.ps(name=name)
            #pid = str(result[0]["pid"])

        try:
            if len(pid) > 0:  # check if pid found in registry and if found kill
                print("Killing:", pid)
                Shell.kill_pid(pid)
                registry.delete(name=name)
            elif result:  # no server found in registry so kill based on ps output
                for process in result:
                    pid = str(process["pid"])
                    if len(pid) > 0:
                        print("Killing:", pid)
                        Shell.kill_pid(pid)
                        registry.delete(name=name)
                    else:
                        print()
                        Console.error(f"PS output generated invalid PID for server name {name}")
            else:
                print()
                Console.error(f"No Cloudmesh OpenAPI Server found with the name {name}")
        except:
            print("got to exception")
            Console.error(
                f"No Cloudmesh OpenAPI Server found with the name {name}")

    def run_os(self):
        """
        Start an openapi server by creating a physical flask script

        :return:
        """

        Console.ok("starting server")

        # For windows convert backslashes to forward slashes to be python compatible
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
                            server='{self.server}')
            ''')

        VERBOSE("server script: ", f"{self.directory}/{self.name}_cmsoaserver.py")

        # Write out flask python script to file so that it can be run in background
        try:
            version = open(f"{self.directory}/{self.name}_cmsoaserver.py", 'w').write(
                flask_script)
        except IOError:
            Console.error("Unable to write server file")
        except Exception as e:
            print(e)

        # Run python flask script in background
        pid = ""
        try:
            # TODO: need to write log somewhere else or use a logger to write to common log.  Tried devnull and that does not work.
            logname = f"{self.directory}/{self.name}_server.{today_dt}.log"

            f = open(logname, "w")
            #f = open(os.devnull, "w")
            process = subprocess.Popen([sys.executable,
                                        f"{self.directory}/{self.name}_cmsoaserver.py"],
                                       stdout=f,
                                       stderr=subprocess.STDOUT,
                                       shell=False)

            pid = process.pid

        except Exception as e:
            Console.error("Unable to start server")
            print(e)

        with open(self.spec, "r") as stream:
            try:
                details = yaml.safe_load(stream)
            except yaml.YAMLError as e:
                print(e)
                assert False, "Yaml file has syntax error"

        url = details["servers"][0]["url"]

        print()
        print("   Starting:", self.name)
        print("   PID:     ", pid)
        print("   Spec:    ", self.spec)
        print("   URL:     ", url)
        print()

        registry = Registry()
        registry.add_form_file(details,
                               pid=pid,
                               spec=self.spec,
                               directory=self.directory,
                               port=self.port,
                               host=self.host,
                               url=url
                               )

        return pid
