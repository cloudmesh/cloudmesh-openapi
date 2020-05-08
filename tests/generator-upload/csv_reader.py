import numpy as np
from cloudmesh.common.util import path_expand

def print_csv2np(filename: str) -> str:
    """
    reads a previously uploaded csv file into a numpy array and prints it

    :param filename: base filename
    :type filename: str
    :return: result
    :return type: str
    """

    x = np.genfromtxt(path_expand('~/.cloudmesh/upload-file/' + filename), delimiter=',')
    return str(x)
