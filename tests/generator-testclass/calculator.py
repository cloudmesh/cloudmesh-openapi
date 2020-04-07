

class Calculator:
    """
    A simple calculator that allows you to do basic math operations
    """

    @classmethod
    def multiplyint(cls, x: int, y: int) -> int:
        """
        Multiply int by int.

        :param x: the value of input #1
        :type x: int
        :param y: the value of input #2
        :type y: int
        :return: result of multiplying x by y
        :return type: int
        """
        return x * y

    @classmethod
    def dividefloat(cls, x: int, y: float) -> float:
        """
        Divide int by float.

        :param x: the value of input #1
        :type x: int
        :param y: the value of input #2
        :type y: float
        :return: result of dividing x by y
        :return type: float
        """
        return x / y


if __name__ == '__main__':
    calc = Calculator()
    manswer = calc.multiplyint(1, 2)
    danswer = calc.dividefloat(6, 2.3)
    print(f"multiply answer: {manswer}")
    print(f"divide answer: {danswer}")
