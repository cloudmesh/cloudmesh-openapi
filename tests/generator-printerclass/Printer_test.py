"""
Convenient methods and classes to print tables.
"""
import json

import oyaml as yaml
from cloudmesh.common.FlatDict import flatten
from cloudmesh.common.console import Console
from cloudmesh.common.dotdict import dotdict
# from prettytable import PrettyTable
from cloudmesh.common.prettytable import PrettyTable
from cloudmesh.common.util import convert_from_unicode
from humanize import naturaltime
from dateutil import parser
from cloudmesh.common.DateTime import DateTime


class Printer(object):
    """
    A simple Printer class with convenient methods to print dictionary, tables, csv, lists
    """

    @classmethod
    def print_list(cls, l, output='table') -> str:
        """
        prints a list
        :param list l: the list
        :param str output: the output, default is a table
        :return:

        """


        def dict_from_list(l):
            """
            returns a dict from a list for printing
            :param l: the list
            :return:
            """
            d = dict([(idx, item) for idx, item in enumerate(l)])
            return d

        if output == 'table':
            x = PrettyTable(["Index", "Host"])
            for (idx, item) in enumerate(l):
                x.add_row([idx, item])
            x.align = "l"
            x.align["Index"] = "r"
            return x
        elif output == 'csv':
            return ",".join(l)
        elif output == 'dict':
            d = dict_from_list(l)
            return d
        elif output == 'json':
            d = dict_from_list(l)
            result = json.dumps(d, indent=4)
            return result
        elif output == 'yaml':
            d = dict_from_list(l)
            result = yaml.dump(d, default_flow_style=False)
            return result
        elif output == 'txt':
            return "\n".join(l)

    @classmethod
    def row_table(cls, d, order=None, labels=None) -> str:
        """
        prints a pretty table from data in the dict.

        :param dict d: A dict to be printed
        :param str order: The order in which the columns are printed.
                      The order is specified by the key names of the dict.
        :param str labels: The array of labels for the column
        """
        # header
        header = list(d)
        x = PrettyTable(labels)
        if order is None:
            order = header
        for key in order:
            value = d[key]
            if type(value) == list:
                x.add_row([key, value[0]])
                for element in value[1:]:
                    x.add_row(["", element])
            elif type(value) == dict:
                value_keys = list(value)
                first_key = value_keys[0]
                rest_keys = value_keys[1:]
                x.add_row(
                    [key, "{0} : {1}".format(first_key, value[first_key])])
                for element in rest_keys:
                    x.add_row(["", "{0} : {1}".format(element, value[element])])
            else:
                x.add_row([key, value])

        x.align = "l"
        return x
