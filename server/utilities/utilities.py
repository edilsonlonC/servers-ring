import json
import os
import path
import string
import random


def getRandomString(length):
    string_for_generate = string.ascii_letters + string.digits
    result_string = "".join((random.choice(string_for_generate) for i in range(length)))
    return result_string


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


def isInRange(_id, _range):

    if isinstance(_range[0], list):
        first_range = _range[0]
        second_range = _range[1]
        if (
            _id > first_range[0]
            and _id <= first_range[1]
            or _id > second_range[0]
            and _id <= second_range[1]
        ):
            return True
    else:
        if _id > _range[0] and _id <= _range[1]:
            return True
    return False


def makeDirIfNotExist(foldername):
    if not os.path.exists(foldername):
        os.mkdir(foldername)


def savePart(folder_name, id_file, _bytes):
    with open(f"{ folder_name }/{ id_file }", "wb") as _file:
        _file.write(_bytes)
