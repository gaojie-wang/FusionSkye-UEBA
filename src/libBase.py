# -*- coding:utf-8 -*-
import os
import json


def get_relation_dir(root_dir):
    return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), root_dir)


def get_config_file_path(config_file, root_dir="conf", check=False):
    full_path = os.path.join(get_relation_dir(root_dir), config_file)
    if check is True:
        if os.path.exists(full_path) is True:
            return full_path
        else:
            print full_path + " not exist"
            return None
    else:
        return full_path


def bind_dict(dict_list):
    out_dict = {}
    for dict_cell in dict_list:
        for m in dict_cell:
            out_dict[m] = single_compose_conf_parm[m]
    return out_dict

def read_file(file_path):
    try:
        with open(file_path, "r") as f_h:
            f_c = f_h.read()
            return f_c
    except Exception:
        return None


def read_json(config_file, root_dir="config"):
    try:
        full_path = get_config_file_path(config_file, root_dir=root_dir)
        if full_path is not None:
            org_content = read_file(full_path)
            try:
                return json.loads(org_content)
            except Exception as e:
                print str(e)
                return {}
        else:
            return {}
    except Exception as e:
        print str(e)
        return {}


def check_os_windows():
    if os.name == "nt":
        return True
    else:
        return False