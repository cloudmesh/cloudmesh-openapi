import sys
import Generator as generator

def sampleFunction(x: int, y: float) -> float:
    """
    Multiply int and float sample.
    :param x: x value
    :type x: int
    :param y: y value
    :type y: float
    :return: result
    :return type: float
    """
    return x * y

f = sampleFunction
openAPI = generator.Generator()
spec = openAPI.generate_openapi(f)
# print(spec)
