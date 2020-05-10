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

        #if literal_type[0] == '{':
        #    table_key = 'string'
        #    res.add(self.type_table[table_key])
        if literal_type[:4] == 'dict':
            table_key = 'dictionary'
            res.add(self.type_table[table_key])
        if len(res) == 1:
            return res.pop()
        else:
            reslist = list(res)
            return reslist[0]


class Generator:

    importfuction = textwrap.dedent("""
        from {library}.{module} import {class_nm}
        import numpy as np
        import array
        from cloudmesh.openapi.registry.cache import ResultCache
                """)

    functiontemplatearrayandX_param = textwrap.dedent("""
    
        def {functioname}({parameters}) -> {returnparam1}:
        
            {text1}
            {description}
            
            
            {docstring}
            {text1}
            
            {X_numpyconversion}
            model = ResultCache().load("{model_tag}")
            {returnparam1} = model.{functioname}({param_wo_type})
            {returnparam1} = {returnparam1}.tolist()
            
            
            return {returnparam1}
        """)

    functiontemplatewithX_param = textwrap.dedent("""

            def {functioname}({parameters}) -> {returnparam1}:

                {text1}
                {description}


                {docstring}
                {text1}

                {X_numpyconversion}
                model = ResultCache().load("{model_tag}")
                {returnparam1} = model.{functioname}({param_wo_type})
                
                
                return {returnparam1}
            """)

    functiontemplate = textwrap.dedent("""

        def {functioname}({parameters}) -> {returnparam1}:

            {text1}
            {description}


            {docstring}
            {text1}

            model = ResultCache().load("{model_tag}")
            {returnparam1} = model.{functioname}({param_wo_type})
            
            
            return {returnparam1}
        """)

    functiontemplatereturningself = textwrap.dedent("""
    
            def {functioname}({parameters}):

                {text1}
                {description}


                {docstring}
                {text1}
               
                {functioname} = {base_estimator}().{functioname}({param_wo_type})
                ResultCache().save("{model_tag}","pickle",{functioname})
                


                return
            """)

    functiontemplatefit = textwrap.dedent("""

                def {functioname}({parameters}):

                    {text1}
                    {description}


                    {docstring}
                    {text1}
                    
                    {X_numpyconversion}
                    {functioname} = {base_estimator}().{functioname}({param_wo_type})
                    ResultCache().save("{model_tag}","pickle",{functioname})


                    return 
                """)

    functiontemplatesetparams = textwrap.dedent("""

                    def {functioname}({parameters}):

                        {text1}
                        {description}


                        {docstring}
                        {text1}

                        {functioname} = {base_estimator}().{functioname}({param_wo_type})
                        ResultCache().save("{model_tag}","pickle",{functioname})


                        return
                    """)
    def populate_parameters_function(self, f, paras_dict, paras_desc):
        """
        Function to loop all the parameters of given function and generate
        specification

        :param paras_dict: parameters dictionary passed to the function
        :param paras_desc: parameters docstrings passed to the function
        :return:
        """
        spec = str()
        spec_params = str()
        docstring = str()
        for i, item in enumerate(paras_dict):
            if i == (len(paras_dict)-1):
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
                            spec_params =  spec_params + (f"""{parameter_dict}""")
                        else:
                            spec = spec + f"""{parameter_dict}: {_type},""" + " "
                            spec_params = spec_params + f"""{parameter_dict},""" + " "

        return spec,spec_params,docstring

    def is_valid_para(self, para_type, type_table):
        """Check if it is a valid parameter type contained in the type table.
        """
        # The values of the table contain all known destination types
        if para_type in type_table.values():
            return True
        return True

    def get_parameters(self, parsing_obj, type_table):
        """Get parameters from the doc of a class, function, or property object.

        Given the sklean docstring follows the numpy conventions, this function
        use the numpy docstring parser to read the doc of sklean.
        """
        scraper = TypeScraper(type_table=type_table)
        r = parsing_obj
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
                #returnparam['return'] = para_type
                paras['return'] = para_type
            else:
                continue
        key = 'return'
        if key not in paras.keys():
            paras['return'] = 'self'
        return paras

    def get_docstrings(self, parsing_obj):
        """Get descriptions  from the doc of a class, function, or property object.

        Given the sklean docstring follows the numpy conventions, this function
        use the numpy docstring parser o read the doc of sklean.
        """
        #r = docscrape.NumpyDocString(doc)
        r = parsing_obj
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
        key = 'return'
        if key not in paras_desc.keys():
            paras_desc['return'] = 'self'
        return paras_desc

    def generate_function(self, module, function,base_estimator,model_tag):
        """

        :param module: Sklearn module like Linear Regression
        :param function: Methods in the class of Linear Regression
        :param base_estimator: Sklearn module like Linear Regression
        :param model_tag: Tag used to store the name of the model instance
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
        base_estimator = base_estimator
        model_tag = model_tag
        class_obj = getattr(module, class_name)
        parsing_obj = docscrape.FunctionDoc(class_obj)
        doc = class_obj.__doc__
        paras_dict_func = self.get_parameters(parsing_obj, type_table)
        paras_desc = self.get_docstrings(parsing_obj)

        description = class_obj.__doc__.strip().split("\n")[0]
        #title = class_obj.__name__
        parametersfunc,params,docstring = self.populate_parameters_function(function, paras_dict_func, paras_desc)
        text1 = '"""'
        key = 'return'
        returnparam =''
        #print(paras_dict_func)
        if  key in paras_dict_func.keys():
            if paras_dict_func['return'] != 'self':
                returnparam = paras_dict_func['return']
            else:
                returnparam
        returnparamindex = 0
        returnparamindex = parametersfunc.find('return')
        if (returnparamindex == -1):
            pass
        elif (returnparamindex == 0):
            parametersfunc = ''
        else:
            parametersfunc = parametersfunc[:returnparamindex-2]
        returnparamindex1 = 0
        returnparamindex1 = params.find('return')
        if (returnparamindex1 == -1):
            pass
        elif (returnparamindex1 == 0):
            params = ''
        else:
            params = params[:returnparamindex1 - 2]
        functionname = class_obj.__name__
        match = re.search(r'X: array', parametersfunc)
        X_param_index = parametersfunc.find('X: array')
        sample_weight_index = parametersfunc.find('sample_weight: array')
        if sample_weight_index != -1:
            parametersfunc = parametersfunc[:sample_weight_index - 2]
        sample_weight_index_params = params.find('sample_weight')
        if sample_weight_index_params != -1:
            params = params[:sample_weight_index_params - 2]
        if match:
            parametersfunc =  parametersfunc + "," + " X_shape_x: int," + " X_shape_y: int"
        parametersfunc = parametersfunc.replace('array','list')
        X_numpyconversion = f"X = np.array(X).reshape(X_shape_x,X_shape_y)"

        if returnparam != '':
            if returnparam == 'array' and  X_param_index == 0 :
                returnparam = 'list'

                spec = self.functiontemplatearrayandX_param.format(
                    functioname=functionname,
                    description=description,
                    text1=text1,
                    model_tag=model_tag,
                    X_numpyconversion=X_numpyconversion,
                    parameters=parametersfunc,
                    param_wo_type=params,
                    docstring=docstring,
                    returnparam1=returnparam
                )
                return spec
            elif X_param_index == 0 :
                spec = self.functiontemplatewithX_param.format(
                    functioname=functionname,
                    description=description,
                    text1=text1,
                    model_tag=model_tag,
                    X_numpyconversion=X_numpyconversion,
                    parameters=parametersfunc,
                    param_wo_type=params,
                    docstring=docstring,
                    returnparam1=returnparam
                )
                return spec
            else:

                spec = self.functiontemplate.format(
                    functioname=functionname,
                    description=description,
                    text1 = text1,
                    model_tag=model_tag,
                    parameters=parametersfunc,
                    param_wo_type=params,
                    docstring=docstring,
                    returnparam1=returnparam
                )

                return spec
        else:
            if functionname == 'fit':
                spec = self.functiontemplatefit.format(
                    functioname=functionname,
                    description=description,
                    base_estimator=base_estimator,
                    X_numpyconversion=X_numpyconversion,
                    model_tag=model_tag,
                    text1=text1,
                    parameters=parametersfunc,
                    param_wo_type=params,
                    docstring=docstring,
                    returnparam1=returnparam
                )
                return spec
            elif functionname =='set_params':
                spec = self.functiontemplatesetparams.format(
                    functioname=functionname,
                    description=description,
                    base_estimator=base_estimator,
                    model_tag=model_tag,
                    text1=text1,
                    parameters=parametersfunc,
                    param_wo_type=params,
                    docstring=docstring,
                    returnparam1=returnparam
                )
                return spec
            else:
                spec = self.functiontemplatereturningself.format(
                    functioname=functionname,
                    description=description,
                    text1=text1,
                    parameters=parametersfunc,
                    base_estimator=base_estimator,
                    model_tag=model_tag,
                    param_wo_type=params,
                    docstring=docstring,
                    returnparam1=returnparam
                )

                return spec

    def generate_import_params(self,input_params):
        """
        :param input_params: takes the input passed from the function
        :return:
        """

        input_params = input_params
        spec = self.importfuction.format(
                library=input_params[0],
                module=input_params[1],
                class_nm=input_params[-1]
        )
        return spec


def Sklearngenerator(input_sklibrary,model_tag):
    """

    :param input_sklibrary: input_sklibrary = sklearn.linear_model.LinearRegression(Full model specification)
    :param model_tag: model_tag = any name which you want the tag the model instance like LinReg1
    :return: .py file which is input to generator which generates openAPI specification
    """

    my_class = locate(input_sklibrary)
    method_list = [func for func,value in inspect.getmembers(my_class) if func[0] != '_']
    method_list = [value for value in method_list if value != 'classes_']
    input_params = input_sklibrary.split('.')
    input_module = f'{input_params[0]}.{input_params[1]}'
    base_estimator = input_params[-1]
    module = locate(input_module)
    class_name = input_params[-1]
    openAPI = Generator()
    spec = openAPI.generate_import_params(input_params)
    print(f"Writing python code to file: {input_params[-1]}.py")
    open(f"./tests/generator/{input_params[-1]}.py", 'w').write(spec)
    #spec = openAPI.generate_function(module, class_name,base_estimator)
    #open(f"{input_params[-1]}.py", 'a').write(spec)
    for i in range(len(method_list)):
        module = my_class
        function = method_list[i]
        openAPI = Generator()
        spec = openAPI.generate_function(module,function,base_estimator,model_tag)
        open(f"./tests/generator/{input_params[-1]}.py", 'a').write(spec)

if __name__ == "__main__":
    Sklearngenerator(input_sklibrary,model_tag)




