#  -*- coding:utf-8 -*-
__author__ = 'zhangjunkai'

import ConfigParser
import threading

from datetime import datetime

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
    readedFile=cf.read(fileName)
    if readedFile==[]:
        return None
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

class DateEncoder(json.JSONEncoder ):
  def default(self, obj):
    if isinstance(obj, datetime):
      return obj.__str__()
    return json.JSONEncoder.default(self, obj)


def secondDiff(endTime ="0:0:00"):
    """
    当前时至到 endTime 需要多少秒
    """

    now=datetime.now()
    start_dt = datetime.strptime("%d:%d:%d"%(now.hour,now.minute,now.second), '%H:%M:%S')
    end_dt = datetime.strptime(endTime, '%H:%M:%S')
    diff = (end_dt - start_dt)
    return diff.seconds
# t=RepeatTimer(5,5,callback)
# t.start()
class RepeatTimer():
    def __init__(self,delay,interval,hFunction):
        self.delay=delay
        self.interval=interval
        self.hFunction = hFunction
        self.thread = threading.Timer(self.delay,self.handle_function)

    def handle_function(self):
        self.hFunction()
        self.thread = threading.Timer(self.interval,self.handle_function)
        self.thread.start()

    def start(self):
        self.thread.start()

    def cancel(self):
        self.thread.cancel()
