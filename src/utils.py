#  -*- coding:utf-8 -*-
__author__ = 'zhangjunkai'

import ConfigParser

import json

QINIU_ACCESS_KEY = '4V9Hf9mJb-4oXbM5H_kqXEuV_5aI4v6S1_LaVLKY'
QINIU_SECRET_KEY = 'BX6p6vGQWa-6VuWf6eikNKYN4P3RG_L4H5Sig_vh'

def get_all_urls(handlers):
    num = 0
    all_urls = ''
    for i in handlers[0][1]:
        num += 1
        if num > 3:
            all_urls += i._path + ','
    return all_urls

def getIniValueFromFile(fileName,header,key):
    cf = ConfigParser.ConfigParser()
    cf.read(fileName)
    value=cf.get(header,key)
    return value

def getJson(jsonStr):
    return json.loads(jsonStr)

def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
