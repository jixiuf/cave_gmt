#  -*- coding:utf-8 -*-
__author__ = 'zhangjunkai'

import ConfigParser
import threading

from datetime import datetime
import time

import json
import re,urllib2

QINIU_ACCESS_KEY = '4V9Hf9mJb-4oXbM5H_kqXEuV_5aI4v6S1_LaVLKY'
QINIU_SECRET_KEY = 'BX6p6vGQWa-6VuWf6eikNKYN4P3RG_L4H5Sig_vh'
def timestamp_now():
    return datetime2timestamp(datetime.now())
def datetime2timestamp(dt):
     return int(time.mktime(dt.timetuple()))

def timestamp2datetime(timestamp, convert_to_local=True):
    ''' Converts UNIX timestamp to a datetime object. '''
    if isinstance(timestamp, (int, long, float)):
        dt = datetime.utcfromtimestamp(timestamp)
        if convert_to_local: # 是否转化为本地时间
            dt = dt + datetime.timedelta(hours=8) # 中国默认时区
        return dt
    return timestamp


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

# json.dumps(data,cls=utils.DateEncoder)
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


# localip = Getmyip().getip()
class Getmyip:
    def getip(self):
        try:
            myip = self.visit("http://ns1.dnspod.net:6666")
        except:
            try:
                myip = self.visit("http://www.ip138.com/ips1388.asp")
            except:
                try:
                    myip = self.visit("https://cgi1.apnic.net/cgi-bin/my-ip.php")
                except:
                    myip = "192.168.0.1"
        return myip
    def visit(self,url):
        opener = urllib2.urlopen(url)
        if url == opener.geturl():
            str = opener.read()
        return re.search('\d+\.\d+\.\d+\.\d+',str).group(0)

