import os
from glob import glob
import sys
import yaml

from pprint import pprint

class Manager(object):
    indent = "  "

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
            with open(self.name(directory, header), 'r') as stream:
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

        for field in ['paths', 'definitions']:
            data[field] = {}


        data["info"]["description"] = ""

        for service in services:

            with open(service, 'r') as stream:
                try:
                    spec = yaml.load(stream)

                    data["info"]["description"] += "# " + spec["info"][
                        "title"] + "\n"
                    data["info"]["description"] += spec["info"]["description"]

                    # print (data["info"]["description"])

                    for field in ['paths', 'definitions']:
                        if field in spec:
                            s = spec[field]
                            for entry in s:
                                #print (field, entry)
                                data[field][entry] = s[entry]
                except yaml.YAMLError as exc:
                    print(exc)
                    sys.exit()

            data["info"]["description"] = "TBD"

        return data

    def codegen(self, services, srcdirectory=".", destdirectory="."):
        s = []
        if len(services) == 0:
            services = self.get(srcdirectory)
        else:
            s = []
            for service in services:
                s.append(self.name(srcdirectory, service))
            services = s

        for service in services:
            with open(service, 'r') as stream:
                spec = yaml.load(stream)
                paths = spec["paths"]
                pathskeys = list(paths.keys())
                #pprint (pathskeys)
                for pathkey in pathskeys:
                    #print (pathkey)
                    ops = paths[pathkey]
                    #print (ops)
                    opskeys = list(ops.keys())
                    #print (opskeys)
                    for opkey in opskeys:
                        opid = ops[opkey]["operationId"]
                        #print (opid)
                        (module, file, method) = opid.split(".")
                        fullpathdir = os.path.join(srcdirectory, module)
                        #print (fullpathdir)
                        fullpathfile = os.path.join(fullpathdir, file + ".py")
                        #print (fullpathfile)
                        if not os.path.exists(module):
                            os.makedirs(module)
                        open(fullpathfile, 'w').close()
                for pathkey in pathskeys:
                    #print (pathkey)
                    ops = paths[pathkey]
                    #print (ops)
                    opskeys = list(ops.keys())
                    #print (opskeys)
                    for opkey in opskeys:
                        opid = ops[opkey]["operationId"]
                        #print (opid)
                        opsummary = ''
                        if "summary" in ops[opkey]:
                            opsummary = ops[opkey]["summary"]
                        elif "description" in ops[opkey]:
                            opsummary = ops[opkey]["description"]
                        #print (opsummary)
                        params = []
                        if "parameters" in ops[opkey]:
                            params = ops[opkey]["parameters"]
                        #print (params)

                        (module, file, method) = opid.split(".")
                        fullpathdir = os.path.join(srcdirectory, module)
                        fullpathfile = os.path.join(fullpathdir, file + ".py")
                        with open(fullpathfile, 'a+') as pycode:
                            pycode.write(self.methoddefhead(method,
                                                            params,
                                                            opsummary))

    def methoddefhead(self, name, params, summary):
        paramslist = [param["name"] for param in params]
        paramsstr = ', '.join(paramslist)
        defstr = "def {name}({paramsstr}):\n".format(name=name,
                                                   paramsstr=paramsstr)
        defstr = defstr + self.methoddoc(summary, params)
        defstr = defstr + "\n{indent}return 'TO BE IMPLEMENTED'\n\n".format(
                                                        indent=Manager.indent)
        #print (defstr)
        return defstr

    def methoddoc(self, summary, params):
        docstr = "{indent}'''{summary}\n\n".format(indent=Manager.indent,
                                                   summary=summary)
        if params:
            docstr = docstr + "{indent}Params:\n".format(indent=Manager.indent)
        for param in params:
            paramstr = "{indent}{name} - {description}\n".format(
                                                        indent=Manager.indent*2,
                                                        **param)
            docstr = docstr + paramstr
        docstr = docstr + "\n{indent}'''\n".format(indent=Manager.indent)
        return docstr

    def name(self, directory, n):
        return os.path.join(directory, n + ".yaml")

    def get(self, directory):
        files = glob(os.path.join(directory, "*.yaml"))
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


class OpenAPIMarkdown(object):
    try:
        columns, lines = os.get_terminal_size()
    except Exception as e:
        rows, columns = map(int, os.popen('stty size', 'r').read().split())

    def ERROR(self, *args, **kwargs):
        print("ERROR", *args, file=sys.stderr, **kwargs)

    def convert_definitions(self, filename, indent=1):
        with open(filename, "r") as f:
            spec = yaml.load(f)
            # print (yaml.dump( spec, default_flow_style=False, default_style='' ))
            print(spec["info"]["description"])
            print()
            for definition in spec["definitions"]:
                # print (indent * "#", definition)
                print(indent * "#", 'Properties', definition)
                print()
                print("|", "Property", "|", "Type", "|", "Description", "|")
                print("|", "---", "|", "---", "|", "-------------", "|")
                properties = spec["definitions"][definition]['properties']
                for property in properties:
                    if 'description' not in properties[property]:
                        properties[property][
                            'description'] = "ERROR: description missing"

                    if 'type' not in properties[property]:
                        properties[property]['type'] = ""

                    if properties[property]['type'] == "array":
                        if "type" in properties[property]["items"]:
                            properties[property]['type'] = "array[{}]".format(
                                properties[property]["items"]["type"])
                        elif "$ref" in properties[property]["items"]:
                            properties[property]['type'] = "array[{}]".format(
                                properties[property]["items"]["$ref"])

                    print("|", property, "|", properties[property]['type'], "|",
                          properties[property]['description'], "|")
                print()

    def section_link_from_ref(self, response):
        # See [section one](#section-one).
        link = ""
        try:
            response["section"] = response['schema']['$ref'].replace(
                "#/definitions/", "")
            response["lsection"] = response["section"].lower()
        except Exception as e:
            response["section"] = ""
            response["lsection"] = ""
        if response["section"] != "":
            link = "[{section}](#sec:spec-{lsection})".format(**response)
        else:
            link = ""
        response["link"] = link
        return response

    def title(self, filename, indent=1):
        with open(filename, "r") as f:
            spec = yaml.load(f)
        title = spec["info"]["title"]

        print("#" * indent, title, "{#sec:spec-" + title.lower() + "}")
        print()
        print("Version:", spec["info"]["version"] + ",", spec["info"][
            "x-date"])
        print()

    def convert_paths(self, filename, indent=2):
        with open(filename, "r") as f:
            spec = yaml.load(f)
            # print (yaml.dump( spec, default_flow_style=False, default_style='' ))
            print()
            print(indent * "#", "Paths")
            print()
            paths = spec["paths"]
            for path in paths:
                print((indent + 1) * "#", path)
                print()
                # print ("|", "Property", "|", "Type", "|", "Description", "|")
                # print ("|", "---", "|", "---", "|", "-------------", "|")
                urls = paths[path]
                for method in urls:
                    print((indent + 2) * '#', method.upper(), path)
                    print()
                    #
                    # DESCRIPTION
                    #
                    # print ((indent + 3) * "#", "Description")
                    # print()
                    try:
                        description = paths[path][method]['description']
                    except Exception as e:
                        description = "ERROR: missing"
                    print(description)
                    print()
                    #
                    # RESPONSES
                    #
                    # print ((indent + 3) * "#", "Responses")
                    print("Responses")
                    print()
                    try:
                        responses = paths[path][method]['responses']
                    except Exception as e:
                        responses = "ERROR: undefined"
                    for code in responses:
                        print("|", "Code", "|", "Description", "|", "Schema",
                              "|")
                        print("|", "---", "|", "---", "|", "-------------", "|")
                        response = responses[code]
                        if "schema" not in response:
                            response['schema'] = ""

                        response['code'] = code
                        response = self.section_link_from_ref(response)
                        print("| {code} | {description} | {link} |".format(
                            **response))
                        print()
                    #
                    # PARAMETERS
                    #
                    # print ((indent + 3) * "#", "PARAMETERS")
                    parameters = None
                    try:
                        parameters = paths[path][method]['parameters']
                        print("Parameters")
                        print()
                    except Exception as e:
                        parameters = None
                    if parameters is not None:
                        print(
                            "| Name | Located in | Description | Required | Schema |")
                        print("| --- | --- | ------------- | --- | --- |")
                        for parameter in parameters:
                            if "required" not in parameter:
                                parameter['required'] = False
                            if "description" not in parameter:
                                parameter[
                                    'description'] = "ERROR: description missing"
                            parameter = self.section_link_from_ref(parameter)

                            print(
                                "| {name} | {in} | {description} | {required} | {link} | ".format(
                                    **parameter))
                print()
