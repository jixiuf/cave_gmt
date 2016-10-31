# -*- coding:utf-8 -*-

__author__ = 'jixiufeng'

import signal
import init
import os
import os.path

import tornado.ioloop
import tornado.httpserver
from tornado.options import options

def main():
    """entry point for process"""
    print "you could run this :python main.py -host=localhost -mode=dev -port=3002"

    tornado.options.parse_command_line()
    # if not os.path.exists(conf.LOCAL_UPLOAD_DIR):
    #     os.mkdir(conf.LOCAL_UPLOAD_DIR)

    http_server = tornado.httpserver.HTTPServer(init.get_app())
    http_server.listen(options.port)

    print "server start at http://%s:%s with mode %s" % (options.host, options.port, options.mode)
    tornado.ioloop.IOLoop.instance().start()



if __name__ == '__main__':
    main()

