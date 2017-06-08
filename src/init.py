#  -*- coding:utf-8 -*-
from tornado.options import define
from tornado.options import  options
import os
import conf
import os.path

from app import Application
define("port", default=3002, help="run on the given port", type=int)
define("host", default="127.0.0.1", help="host or ip", type=str)
define("mode", default="dev", help="mode (dev or pro)", type=str)
define("locale", default="zh", help="locale (default chi)", type=str)
define("confdir", default=conf.CONFIG_DIR, help="config file directory", type=str)
define("etcd", default="http://127.0.0.1:2379", help="demo http://127.0.0.1:2379", type=str)



def get_data_dir():
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    if not os.path.exists(data_dir):
        os.mkdir(data_dir)
    return data_dir

def init():
    data_dir=get_data_dir()
    define("data_dir", default=data_dir, help="data_dir", type=str)
    # define("log_file_prefix", default=data_dir+"/tornado.log", help="logdir for tornado", type=str)

def get_app():
    init()
    app = Application()
    return app

def get_test_app():
    init()
    app = Application()
    return app
