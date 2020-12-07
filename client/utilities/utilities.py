import json
import os


def printPrettyJson(_dict):
    print(json.dumps(_dict, indent=2))


def makedirIfNotExist(folder_name):
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)


def file_exist(filename):
    return os.path.exists(filename)


def get_newname(filename):
    list_dir = os.listdir()
    name, ext = filename.rsplit(".", 1)
    same_names = list()
    for l_d in list_dir:
        if name in l_d:
            same_names.append(l_d)
    for sm in range(len(same_names)):
        new_name = f"{name}({sm+1}).{ext}"
        if not new_name in same_names:
            return new_name
