#  -*- coding:utf-8 -*-
from tornado.options import define
import os
import os.path

from app import Application
define("port", default=8000, help="run on the given port", type=int)
define("host", default="127.0.0.1", help="host or ip", type=str)
define("mode", default="dev", help="mode (dev or pro)", type=str)
define("locale", default="chi", help="locale (default chi)", type=str)


def get_data_dir():
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    if not os.path.exists(data_dir):
        os.mkdir(data_dir)
    return data_dir

def init():
    data_dir=get_data_dir()
    define("data_dir", default=data_dir, help="data_dir", type=str)

def get_app():
    init()
    app = Application()
    return app

def get_test_app():
    init()
    app = Application()
    return app
