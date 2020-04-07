from cloudmesh.openapi.function.generator import Generator


# noinspection PyPep8Naming
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
openAPI = Generator()
spec = openAPI.generate_openapi(f,
                                "tests/generator/",
                                "../../../tests")
# print(spec)
