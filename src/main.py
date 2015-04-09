#! ../virtual/bin/python
# -*- coding:utf-8 -*-
import os
import os.path

import tornado.ioloop
import tornado.httpserver

from application import Application

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)
define("host", default="127.0.0.1", help="host or ip", type=str)
define("mode", default="dev", help="mode (dev or pro)", type=str)

def get_data_dir():
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    if not os.path.exists(data_dir):
        os.mkdir(data_dir)
    return data_dir

def main():
    """entry point for process"""
    print "you could run this :python main.py -host=localhost -mode=dev -port=8000"
    tornado.options.parse_command_line()
    # if not os.path.exists(conf.LOCAL_UPLOAD_DIR):
    #     os.mkdir(conf.LOCAL_UPLOAD_DIR)
    data_dir=get_data_dir()
    define("data_dir", default=data_dir, help="data_dir", type=str)

    application = Application()
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)

    print "server start at http://%s:%s with mode %s" % (options.host, options.port, options.mode)
    tornado.ioloop.IOLoop.instance().start()



if __name__ == '__main__':
    main()

