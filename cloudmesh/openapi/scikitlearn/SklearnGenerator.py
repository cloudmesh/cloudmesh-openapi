#from cloudmesh.common.console import Console
import inspect
import re
import textwrap
from pydoc import locate

from numpydoc import docscrape


class TypeScraper:
    """
    Scrape types from a string.
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
        """
        The Constructor function

            Parameters:
                type_table: A dictionary indicates the matching rules
        """
        self.type_table = type_table

    def scrap(self, literal_type):
        """
        Match types from the string

            Parameters:
                literal_type: A string that defines a type
        """

        res = set()

        # Traverse all known mappings to check which key of the table
        # matches the string
        for table_key in self.type_table.keys():
            #print(literal_type)
            if re.search(table_key, literal_type, re.IGNORECASE):
                res.add(self.type_table[table_key])

        if literal_type[0] == '{':
            table_key = 'string'
            res.add(self.type_table[table_key])
        if literal_type[:4] == 'dict':
            table_key = 'dictionary'
            res.add(self.type_table[table_key])
        if len(res) == 1:
            return res.pop()
        else:
            reslist = list(res)
            return reslist[0]


class Generator:

    functiontemplate = textwrap.dedent("""
        def {functioname}({parameters}) -> {returnparam1}:
        
            {text1}
            {description}
            
            
            {docstring}
            {text1}
              
            return {returnparam1}
        """)

    def populate_parameters_function(self, f, paras_dict, paras_desc):
        """
        Function to loop all the parameters of given function and generate
        specification

        :param function_name:
        :return:
        """
        spec = str()
        docstring = str()
        for i, item in enumerate(paras_dict):
            if i == (len(paras_dict) - 1):
                last_key = item
        for parameter_dict, _type in paras_dict.items():
            for parameter_desc, desc in paras_desc.items():
                if parameter_dict == 'return1':
                    docstring = docstring + \
                                (f""":param {parameter_dict}: {desc}""") + "\n" + \
                                "    " + (f""":type {parameter_dict}: {_type}""") + "\n" + "    "
                else:
                    if parameter_dict == parameter_desc:
                        docstring = docstring  + \
                        (f""":param {parameter_dict}: {desc}""") +  "\n" + \
                        "    "+ (f""":type {parameter_dict}: {_type}""") + "\n" + "    "
                        if parameter_dict == last_key:
                            spec = spec + (f"""{parameter_dict}: {_type}""")
                        else:
                            spec = spec + f"""{parameter_dict}: {_type},""" + " "

        return spec,docstring

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
            #print(p)
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
                #returnparam['return'] = para_type
                paras['return'] = para_type
            else:
                continue
        print(paras)
        return paras

    def get_docstrings(self, doc):
        """Get descriptions  from the doc of a class, function, or property object.

        Given the sklean docstring follows the numpy conventions, this function
        use the numpy docstring parser to read the doc of sklean.
        """
        r = docscrape.NumpyDocString(doc)
        paras_desc = {}
        for p in r['Parameters']:
            para_name = str(p.name)
            para_desc = '\n                    '.join(p.desc)
            paras_desc[para_name] = para_desc

        for p in r['Returns']:
            #print(p.name,p.desc)
            para_name = str(p.name)
            para_desc = '\n                    '.join(p.desc)
            paras_desc['return'] = para_desc
        print(paras_desc)
        return paras_desc

    def generate_function(self, module, function):
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
            'bool': 'bool',
            'int': 'int',
            'float': 'float',
            'string': 'str',
            'dictionary': 'dict',
            'dict': 'dict',
            'object': 'self',
            'self': 'self'
        }
        module = module
        class_name = function
        class_obj = getattr(module, class_name)
        doc = class_obj.__doc__
        paras_dict_func = self.get_parameters(doc, type_table)
        paras_desc = self.get_docstrings(doc)
        description = class_obj.__doc__.strip().split("\n")[0]
        title = class_obj.__name__
        parametersfunc,docstring = self.populate_parameters_function(function, paras_dict_func, paras_desc)
        text1 = '"""'
        key = 'return'
        if  key in paras_dict_func.keys():
            returnparam = paras_dict_func['return']
        else:
            returnparam = 'self'

        functionname = class_obj.__name__
        spec = self.functiontemplate.format(
            functioname=functionname,
            description=description,
            text1 = text1,
            parameters=parametersfunc,
            docstring=docstring,
            returnparam1=returnparam
        )

        return spec

def generator(input):
    my_class = locate(input)
    method_list = [func for func,value in inspect.getmembers(my_class) if func[0] != '_']
    input_params = input.split('.')
    input_module = f'{input_params[0]}.{input_params[1]}'
    module = locate(input_module)
    class_name = input_params[-1]
    openAPI = Generator()
    spec = openAPI.generate_function(module, class_name)

    open(f"{input_params[-1]}.py", 'a').write(spec)
    for i in range(len(method_list)):
        module = my_class
        function =  method_list[i]
        openAPI = Generator()
        spec = openAPI.generate_function(module, function)
        open(f"{input_params[-1]}.py", 'a').write(spec)

if __name__ == "__main__":
    input = 'sklearn.linear_model.LogisticRegression'
    generator(input)

