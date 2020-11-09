import json


def getFieldsDict(_dict, *args):
    new_dict = {}
    for arg in args:
        new_dict[arg] = _dict.get(arg)
    return new_dict


def insertFieldsDict(_dict, **kwargs):
    for key in kwargs:
        _dict[key] = kwargs[key]
    return _dict


def printPrettyJson(_dict):
    print(json.dumps(_dict, indent=4))


def insertFieldsNewDict(_dict, **kwargs):
    new_dict = _dict.copy()
    for key in kwargs:
        new_dict[key] = kwargs[key]
    return new_dict
