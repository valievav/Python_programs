"""
Sort dict by VALUES
"""

from operator import itemgetter
from _collections import OrderedDict

x = {"ddd": 000, "aaa": 111, "ccc": 333, "bbb": 222}


def solution_itemgetter(dict_x: dict)-> None:
    new_dict = dict(sorted(dict_x.items(), key=itemgetter(1)))   # reverse=True
    print(new_dict)


def solution_OrderedDict(x: dict)-> None:  # before Python 3.7
    new_dict = OrderedDict(sorted(x.items(), key=lambda item: item[1]))   # reverse=True
    print(new_dict)


def best_solution_dict_python37(x: dict)-> None:  # AFTER Python 3.7 - regular dict keeps order inserted
    new_dict = dict(sorted(x.items(), key=lambda item: item[1]))  # reverse=True
    print(new_dict)


solution_itemgetter(x)
solution_OrderedDict(x)
best_solution_dict_python37(x)

