from tests.generator import LogisticRegression


function_names = [func for func in dir(LogisticRegression) if not func.startswith('__')]

print(function_names)




