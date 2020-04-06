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
    def flatwrite(cls, table,
                  order=None,
                  header=None,
                  output="table",
                  sort_keys=True,
                  show_none="",
                  humanize=None,
                  sep=".",
                  max_width=48
                  ):
        """
        writes the information given in the table
        :param table: the table of values
        :param order: the order of the columns
        :param header: the header for the columns
        :param output: the format (default is table, values are raw, csv, json, yaml, dict
        :param sort_keys: if true the table is sorted
        :param show_none: passed along to the list or dict printer
        :param sep: uses sep as the separator for csv printer
        :param max_width: maximum width for a cell
        :type max_width: int
        :return:
        """

        flat = flatten(table, sep=sep)

        return Printer.write(flat,
                             sort_keys=sort_keys,
                             order=order,
                             header=header,
                             output=output,
                             humanize=humanize,
                             max_width=max_width
                             )

    @classmethod
    def write(cls, table,
              order=None,
              header=None,
              output="table",
              sort_keys=True,
              humanize=None,
              show_none="",
              max_width=48
              ):
        """
        writes the information given in the table
        :param table: the table of values
        :param order: the order of the columns
        :param header: the header for the columns
        :param output: the format (default is table, values are raw, csv, json, yaml, dict
        :param sort_keys: if true the table is sorted
        :param show_none: passed along to the list or dict printer
        :param max_width: maximum width for a cell
        :type max_width: int
        :return: 
        """
        if output == "raw":
            return table
        elif table is None:
            return None
        elif type(table) in [dict, dotdict]:
            return cls.dict(table,
                            order=order,
                            header=header,
                            output=output,
                            sort_keys=sort_keys,
                            humanize=humanize,
                            show_none=show_none,
                            max_width=max_width)

        elif type(table) == list:

            return cls.list(table,
                            order=order,
                            header=header,
                            output=output,
                            sort_keys=sort_keys,
                            humanize=humanize,
                            show_none=show_none,
                            max_width=max_width)
        else:
            Console.error("unkown type {0}".format(type(table)))

    @classmethod
    def list(cls,
             l,
             order=None,
             header=None,
             output="table",
             sort_keys=True,
             humanize=None,
             show_none="",
             max_width=48
             ):
        """
        :param l: l is a list not a dict
        :param order:
        :param header:
        :param output:
        :param sort_keys:
        :param show_none:
        :param max_width: maximum width for a cell
        :type max_width: int
        :return:
        """

        d = {}
        count = 0
        for entry in l:
            name = str(count)
            d[name] = entry
            count += 1
        return cls.dict(d,
                        order=order,
                        header=header,
                        sort_keys=sort_keys,
                        output=output,
                        humanize=humanize,
                        show_none=show_none,
                        max_width=max_width)

    @classmethod
    def dict(cls, d,
             order=None,
             header=None,
             output="table",
             sort_keys=True,
             humanize=None,
             show_none="",
             max_width=48):
        """
        :param d: A a dict with dicts of the same type.
        :type d: dict
        :param order: The order in which the columns are printed.
                      The order is specified by the key names of the dict.
        :type order: list
        :param header: The Header of each of the columns
        :type header: list or tuple of field names
        :param output: type of output (table, csv, json, yaml or dict)
        :type output: string
        :param sort_keys: list
        :type sort_keys: bool
        :param show_none: prints None if True for None values otherwise ""
        :type show_none: string
        :param max_width: maximum width for a cell
        :type max_width: int
        :return:

        """

        if output == "table":
            if d == {}:
                return None
            else:
                return cls.dict_table(d,
                                      order=order,
                                      header=header,
                                      humanize=humanize,
                                      sort_keys=sort_keys,
                                      max_width=max_width)
        elif output == "html": # does not work
            if d == []:
                return "Empty data"
            else:
                return cls.dict_html(d,
                                      order=order,
                                      header=header,
                                      humanize=humanize,
                                      sort_keys=sort_keys,
                                      max_width=max_width)
        elif output == "csv":
            return cls.csv(d,
                           order=order,
                           header=header,
                           humanize=humanize,
                           sort_keys=sort_keys)
        elif output == "json":
            return json.dumps(d, sort_keys=sort_keys, indent=4)
        elif output == "yaml":
            return yaml.dump(convert_from_unicode(d), default_flow_style=False)
        elif output == "dict":
            return d
        else:
            return "UNKOWN FORMAT. Please use table, csv, json, yaml, dict."

    @classmethod
    def csv(cls, d, order=None, header=None, humanize=None,
            sort_keys=True):
        """
        prints a table in csv format

        :param d: A a dict with dicts of the same type.
        :type d: dict
        :param order: The order in which the columns are printed.
                      The order is specified by the key names of the dict.
        :type order:
        :param header: The Header of each of the columns
        :type header: list or tuple of field names
        :param sort_keys: TODO - not yet implemented
        :type sort_keys: bool
        :return: a string representing the table in csv format
        """

        first_element = list(d)[0]

        def _keys():
            return list(d[first_element])

        # noinspection PyBroadException
        def _get(element, key):
            try:
                tmp = str(d[element][key])
            except:
                tmp = ' '
            return tmp

        if d is None or d == {}:
            return None

        if order is None:
            order = _keys()

        if header is None and order is not None:
            header = order
        elif header is None:
            header = _keys()

        table = ""
        content = []
        for attribute in order:
            content.append(attribute)

        table = table + ",".join([str(e) for e in content]) + "\n"

        for job in d:
            content = []
            for attribute in order:
                try:
                    # if attribute in humanize:
                    #    value = parser.parse(d[job][attribute])
                    #    content.append(naturaltime(value))
                    #    pass
                    # else:
                    content.append(d[job][attribute])
                except:
                    content.append("None")
            table = table + ",".join([str(e) for e in content]) + "\n"
        return table

    @classmethod
    def dict_html(cls, d,
                   order=None,
                   header=None,
                   sort_keys=True,
                   show_none="",
                   humanize=None,
                   max_width=48):
        x= Printer.dict_table(d,
                           order=order,
                           header=header,
                           sort_keys=sort_keys,
                           show_none=show_none,
                           humanize=humanize,
                           max_width=max_width)

        return x.get_html_string()

    @classmethod
    def dict_table(cls, d,
                   order=None,
                   header=None,
                   sort_keys=True,
                   show_none="",
                   humanize=None,
                   max_width=48):
        """
        prints a pretty table from an dict of dicts

        :param d: A a dict with dicts of the same type. Each key will be a column
        :param order: The order in which the columns are printed.
                      The order is specified by the key names of the dict.
        :param header: The Header of each of the columns
        :type header: A list of string
        :param sort_keys: Key(s) of the dict to be used for sorting.
                          This specify the column(s) in the table for sorting.
        :type sort_keys: string or a tuple of string (for sorting with multiple columns)
        :param show_none: prints None if True for None values
        :type show_none: string
        :param max_width: maximum width for a cell
        :type max_width: int
        """

        start = DateTime.now()

        def _keys():
            all_keys = []
            for e in d:
                keys = d[e].keys()
                all_keys.extend(keys)
            return list(set(all_keys))

        # noinspection PyBroadException
        def _get(item, key):
            try:
                tmp = str(d[item][key])
                if tmp == "None":
                    tmp = show_none
                elif humanize and key in humanize:
                    tmp = parser.parse(tmp)
                    tmp = DateTime.humanize(start - tmp)
                    #tmp = naturaltime(start - tmp)
            except:
                tmp = ' '
            return tmp

        if d is None or d == {}:
            return None

        if order is None:
            order = _keys()

        if header is None and order is not None:
            header = order
        elif header is None:
            header = _keys()

        x = PrettyTable(header)
        x.max_width = max_width

        if sort_keys:
            if type(sort_keys) is str:
                sorted_list = sorted(d, key=lambda x: d[x][sort_keys])
            elif type(sort_keys) == tuple:
                sorted_list = sorted(d, key=lambda x: tuple(
                    [d[x][sort_key] for sort_key in sort_keys]))
            else:
                sorted_list = d
        else:
            sorted_list = d


        for element in sorted_list:
            values = []
            for key in order:
                value = _get(element, key)
                values.append(value)
            x.add_row(values)
        x.align = "l"
        return x

    @classmethod
    def attribute(cls, d, header=None, order=None, sort_keys=True,
                  humanize=None,
                  output="table"):
        """
        prints a attribute/key value table

        :param d: A a dict with dicts of the same type.
                  Each key will be a column
        :param order: The order in which the columns are printed.
                       The order is specified by the key names of the dict.
        :param header:  The Header of each of the columns
        :type header:   A list of string
        :param sort_keys:   Key(s) of the dict to be used for sorting.
                             This specify the column(s) in the table for sorting.
        :type sort_keys:    string or a tuple of string (for sorting with multiple columns)
        :param output: the output format table, csv, dict, json
        """

        if header is None:
            header = ["Attribute", "Value"]
        if output == "table":
            x = PrettyTable(header)
            if order is not None:
                sorted_list = order
            else:
                sorted_list = list(d)
            if sort_keys:
                sorted_list = sorted(d)

            for key in sorted_list:
                if type(d[key]) == dict:
                    values = d[key]
                    x.add_row([key, "+"])
                    for e in values:
                        x.add_row(["  -", "{}: {}".format(e, values[e])])
                elif type(d[key]) == list:
                    values = list(d[key])
                    x.add_row([key, "+"])
                    for e in values:
                        x.add_row(["  -", e])
                else:
                    x.add_row([key, d[key] or ""])

            x.align = "l"
            return x
        else:
            return cls.dict({output: d}, output=output)

    @classmethod
    def print_list(cls, l, output='table'):
        """
        prints a list
        :param l: the list
        :param output: the output, default is a table
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
    def row_table(cls, d, order=None, labels=None):
        """
        prints a pretty table from data in the dict.

        :param d: A dict to be printed
        :param order: The order in which the columns are printed.
                      The order is specified by the key names of the dict.
        :param labels: The array of labels for the column
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
