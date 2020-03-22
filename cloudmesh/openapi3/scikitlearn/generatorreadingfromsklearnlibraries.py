import textwrap
#from cloudmesh.common.console import Console
from dataclasses import dataclass, is_dataclass
import textwrap
import re
import array as arr
from inspect import signature
import inspect
from sklearn.linear_model import Ridge
from sklearn.linear_model import LinearRegression
import sklearn.linear_model
from numpydoc import docscrape



class TypeScraper:
    """Scrape types from a string.
        Using  the regular expression to match the keywords that imply the
        types.

        A type table for matching the types from the string is required

        Examples:
            'boolean, optional, default True' = bool
            'int or None, optional (default=None)' = int
            'array-like or sparse matrix, shape (n_samples, n_features)' = list
            'numpy array of shape [n_samples]' 'boolean, optional' = list
 """

    def __init__(self, type_table):
        """The Constructor function

            Parameters:
                type_table: A dictionary indicates the matching rules
        """
        self.type_table = type_table

    def scrap(self, literal_type):
        """Match types from the string

            Parameters:
                literal_type: A string that defines a type
        """

        res = set()

        # Traverse all known mappings to check which key of the table
        # matches the string
        for table_key in self.type_table.keys():
            #print('literal_type:',literal_type)
            if re.search(table_key, literal_type, re.IGNORECASE):
                res.add(self.type_table[table_key])
        #if re.search('default', literal_type, re.IGNORECASE):

        if literal_type[0] == '{':
            table_key = 'string'
            res.add(self.type_table[table_key])
        if literal_type[:4] == 'dict':
            table_key = 'dictionary'
            res.add(self.type_table[table_key])

        # For testing purpose, if more than one is machted, it should report
        # error
        if len(res) == 1:
            return res.pop()
        else:
            reslist = list(res)
            return reslist[0]

class Generator:
    openAPITemplate = textwrap.dedent("""
        openapi: 3.0.0
        info:
          title: {title}
          description: {description}
          version: "{version}"
        servers:
          - url: http://localhost/cloudmesh
            description: TODO THIS MUST BE CHANGEABLE
        paths:
          /{baseurl}:
             get:
              summary: {description}
              description: Optional extended description in CommonMark or HTML.
              operationId: {filename}.{name}
              parameters:
                {parameters}
              responses:
                {responses}
        
        components:
          schemas:
            {schemas}
        """)

    def parse_type(self, _type):
        """
        function to parse supported openapi3 data types

        :param _type:
        :return:
        """
        parser = {
            'integer': 'type: integer',
            'boolean': 'type: boolean',
            'number': 'type: number',
            'array': 'type: array',
            'string': 'type: string',
            'dictionary': 'type: dictionary',
            'self': 'type: self'
        }
        if is_dataclass(_type):
            return f'$ref: "#/components/schemas/{_type.__name__}'
        # exits with KeyError if unsupported type is given
        try:
            t = parser[_type]
        except KeyError:
            print(f'unsupported data type supplied for {_type.__name__}:')
            print(_type)
            raise
        return t

    def generate_parameter(self, name, _type, description):
        """
        function to generate parameters YAMAL contents

        :param name:
        :param _type:
        :param description:
        :return:
        """
        _type = self.parse_type(_type)
        spec = textwrap.dedent(f"""
            - in: query
              name: {name}
              description: {description}
              schema:
                {_type}""")
        return spec

    def generate_response(self, code, _type, description):
        """
        function to generate response yaml contents

        :param code:
        :param _type:
        :param description:
        :return:
        """
        _type = self.parse_type(_type)
        if not _type.startswith('object'):
            # int, bool, float, str, list
            spec = textwrap.dedent(f"""
              '{code}':
                description: {description}
                content:
                  text/plain:
                    schema:
                      {_type}""")
        else:
            # dict (generic json) or dataclass ($ref)
            spec = textwrap.dedent(f"""
              '{code}':
                description: {description}
                content:
                  application/json:
                    schema:
                      {_type}""")
        return spec

    def generate_properties(self, attr, _type):
        """
        function to generate properties of a schema

        :param attr:
        :param _type:
        :return:
        """
        _type = self.parse_type(_type)
        spec = textwrap.dedent(f"""
          {attr}:
            {_type}""")

    def generate_schema(self, _class):
        """
        function to generate schema in the components section from @dataclass
        attributes

        :param _class:
        :return:
        """
        class_name = _class.__name__
        if not is_dataclass(_class):
            raise TypeError(
                f'{class_name} is not a dataclass. '
                'Use the @dataclass decorator to define the class properly')
        properties = str()
        for attr, _type in _class.__annotations__.items():
            properties = properties + self.generate_properties(attr, _type)
        spec = textwrap.dedent(f"""
          {class_name}:
            type: object
            properties:
              {properties}""")

    def populate_parameters(self,f,paras_dict,paras_desc):
        """
        Function to loop all the parameters of given function and generate
        specification

        :param function_name:
        :return:
        """
        spec = str()
        for parameter_dict, _type in paras_dict.items():
             for parameter_desc, desc in paras_desc.items():
                if parameter_dict == 'return':
                    continue  # dicts are unordered, so use continue
                    # intead of break to be safe
                else:
                    if parameter_dict == parameter_desc:
                        spec = spec + self.generate_parameter(
                            parameter_dict,
                            _type,
                            desc)
        return spec

    def is_valid_para(self, para_type, type_table):
        """Check if it is a valid parameter type contained in the type table.
        """
        # The values of the table contain all known destination types
        if para_type in type_table.values():
            return True
        return True

    def get_parameters(self, doc, type_table):
        """Get parameters from the doc of a class, function, or property object.

        Given the sklean docstring follows the numpy conventions, this function
        use the numpy docstring parser to read the doc of sklean.
        """
        scraper = TypeScraper(type_table=type_table)
        r = docscrape.NumpyDocString(doc)

        paras = {}
        returnparam = {}

        for p in r['Parameters']:
            para_str = str(p.type)
            para_type = scraper.scrap(para_str)
            if self.is_valid_para(para_type, type_table):
                paras[p.name] = para_type
            else:
                continue
        for p in r['Returns']:
            para_str = str(p.type)
            para_type = scraper.scrap(para_str)
            if self.is_valid_para(para_type, type_table):
                returnparam[p.name] = para_type
            else:
                continue
        if returnparam == {}:
            returnparam['self'] = 'self'

        return paras,returnparam
    def get_docstrings(self, doc):
        """Get descriptions  from the doc of a class, function, or property object.

        Given the sklean docstring follows the numpy conventions, this function
        use the numpy docstring parser to read the doc of sklean.
        """
        r = docscrape.NumpyDocString(doc)
        paras_desc = {}
        for p in r['Parameters']:
            para_name = str(p.name)
            para_desc = ''.join(p.desc)
            paras_desc[para_name] = para_desc


        return paras_desc

    def generate_openapi(self, f, baseurl, outdir, yaml, write=True):
        """
        function to generate open API of python function.

        :param f:
        :param baseurl:
        :param outdir:
        :param yaml:
        :param write:
        :return:

        """
        type_table = {
            'matrix': 'array',
            'array': 'array',
            'array-like': 'array',
            'numpy array': 'array',
            'bool': 'boolean',
            'int': 'integer',
            'float': 'number',
            'string': 'string',
            'dictionary': 'dictionary',
            'self': 'self'

        }
        module = sklearn.linear_model
        class_name = 'LinearRegression'
        class_obj = getattr(module, class_name)
        doc = inspect.getdoc(class_obj)
        paras_dict,returnparam = self.get_parameters(doc, type_table)
        paras_desc = self.get_docstrings(doc)
        description = f.__doc__.strip().split("\n")[0]
        version = "1.0"  # TODO:  hard coded for now
        title = f.__name__
        parameters = self.populate_parameters(f,paras_dict,paras_desc)
        parameters = textwrap.indent(parameters, ' ' * 8)
        responses = self.generate_response('200',
                                           returnparam['self'],
                                           'OK')
        responses = textwrap.indent(responses, ' ' * 8)

        # TODO: figure out where to define dataclasses and how
        #  best to pass them to generate_schema()
        #filename = f.__code__.co_filename.strip().split("\\")[-1].split(".")[0]
        filename = module
        spec = self.openAPITemplate.format(
            title=title,
            name=f.__name__,
            description=description,
            version=version,
            parameters=parameters.strip(),
            responses=responses.strip(),
            baseurl=baseurl,
            filename=filename,
            schemas=''
        )

        # return code
        rc = 0
        open(f"test.yaml", 'w').write(spec)
        if write:
            try:
                if yaml != "" and yaml is not None:
                    version = open(f"{outdir}/{yaml}.yaml", 'w').write(spec)
                else:
                    version = open(f"{outdir}/{title}.yaml", 'w').write(spec)
            except IOError:
                #Console.error("Unable to write yaml file")
                rc = 1
            except Exception as e:
                print(e)
                rc = 1

        return rc

f = LinearRegression
openAPI = Generator()
spec = openAPI.generate_openapi(f,"http://localhost:8000/cloudmesh",
                                "/Users/jagadeeshk/cm/cloudmesh-openapi/cloudmesh/tests/generator",
                                "test")


