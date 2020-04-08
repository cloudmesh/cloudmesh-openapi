from pprint import pprint

from sklearn.linear_model import LinearRegression

func = LinearRegression

attribute = dir(func)

print(func.__name__)
print(func.__doc__)

for a in attribute:
    if "__" not in a:
        print(">>>>", a)
        eval(f"print(func.{a})")

# print (func.__annotations__)
pprint(dir(func))

pprint(dir(func.fit))
pprint(func.fit.__doc__)
