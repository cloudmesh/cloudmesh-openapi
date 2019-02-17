import sys
import os
from cloudmesh.common.util import path_expand
from glob import glob
from pathlib import Path
import yaml
from pprint import pprint


class Manager(object):

    def __init__(self):
        pass

    def description(self, directory, services):
        if len(services) == 0:
            services = self.get(directory)
        else:
            s = []
            for service in services:
                s.append(self.name(directory, service))
            services = s

        for service in services:

            with open(service, 'r') as stream:
                try:
                    spec = yaml.load(stream)

                    print("\n# " + spec["info"]["title"])
                    print(spec["info"]["description"])
                except yaml.YAMLError as exc:
                    print(exc)
                    sys.exit()


    def merge(self, directory, services, header=".header"):
        try:
            with open(self.name(directory, header), 'r') as  stream:
                data = yaml.load(stream)
        except Exception as e:
            data = {}

        data["paths"] = [],
        data["definitions"] = []

        if len(services) == 0:
            services = self.get(directory)
        else:
            s = []
            for service in services:
                s.append(self.name(directory, service))
            services = s

        for field in ['info','paths', 'definitions']:
            data[field] = {}

        data["info"]["description"] = "|-\n"

        for service in services:

            with open(service, 'r') as stream:
                try:
                    spec = yaml.load(stream)

                    data["info"]["description"] += "# " + spec["info"]["title"] + "\n"
                    data["info"]["description"] += spec["info"]["description"]

                    #print (data["info"]["description"])

                    for field in ['paths', 'definitions']:
                        if field in spec:
                            s = spec[field]
                            for entry in s:
                                data[field][entry] = s[entry]
                except yaml.YAMLError as exc:
                    print(exc)
                    sys.exit()

            #data["info"]["description"] =data["info"]["description"]

        return data

    def name(self, directory, n):
        return os.path.join(directory, n + ".yaml")

    def get(self, dir):
        files = glob(os.path.join(dir, "*.yaml"))
        return files

    """

        def filename(dri, service):
            return os.path.join(dir, service, service + ".yaml")
        
        def read(dir, service):
            
            
            with open(filename(dir, service), "r") as f:
                content = f.read()
            return content

        def read_header(dir, service):
            with open(filename(dir, service), "r") as f:
                content = f.read()
            return content

        def parse_definitions(content):
            return content.split("definitions:")[1]

        def parse_paths(content):
            return content.split("paths:")[1].split("definitions:")[0]

        def merge_yaml(services):
            out = ""
            out = out + "definitions:"
            for service in services:
                content = read("services", service)
                out = out + parse_paths(content)

            out = out + "paths:"
            for service in services:
                content = read("services", service)
                out = out + parse_definitions(content)
            return out

        def add(services, out):

            header = read_header("service", "header")
            output = header + "paths:"

            for service in services:
                content = read("services", service)
                output = output + parse_paths(content)

            output = output + "definitions:"

            for service in services:
                content = read("services", service)
                output = output + parse_definitions(content)
            output = re.sub(r'\n+', '\n', output)
            print(output, file=out)

        merge(services, out)
        """
