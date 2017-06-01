# -*- coding:utf-8 -*-

__author__ = 'jixiufeng'

import signal
import init
import os
import conf
import os.path
import sys
import traceback

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

    App=init.get_app()
    http_server = tornado.httpserver.HTTPServer(App)
    try:
        http_server.listen(options.port)
    except Exception, error:
        print('errormsg\t%s' % (str(error)))
        print('errortrace\t%s' % (str(traceback.format_exc()),))
        App.stop()
        return




    tornado.ioloop.IOLoop.instance().start()



if __name__ == '__main__':
    main()

