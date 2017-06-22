#  -*- coding:utf-8 -*-
__author__ = 'jixiuf'
# usage:
# python get_exportjson_related_files.py a.ExportJson

import json
import sys
def getJson(filename):
    with open(filename) as data_file:
        value = json.load(data_file)
        return value

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("need 1 param: name.ExportJson")

    filename = sys.argv[1]
    js=getJson(filename)
    result=[]
    for v in js["config_file_path"]:
        result.append(v)
    for v in js["config_png_path"]:
        result.append(v)

    print("\n".join(result))



