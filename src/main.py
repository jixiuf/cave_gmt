# -*- coding:utf-8 -*-

__author__ = 'jixiufeng'

import signal
import init
import os
import conf
import os.path

import tornado.ioloop
import tornado.httpserver
from tornado.options import options

def main():
    """entry point for process"""

    tornado.options.parse_command_line()
    # if not os.path.exists(conf.LOCAL_UPLOAD_DIR):
    #     os.mkdir(conf.LOCAL_UPLOAD_DIR)

    if options.confdir!="" and options.confdir!=None:
        conf.CONFIG_DIR=options.confdir
    print "python src/main.py -host=%s -port=%s -mode=%s -locale=%s -confdir=%s" % (options.host, options.port, options.mode,options.locale,options.confdir)

    http_server = tornado.httpserver.HTTPServer(init.get_app())
    http_server.listen(options.port)



    tornado.ioloop.IOLoop.instance().start()



if __name__ == '__main__':
    main()

