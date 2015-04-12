# -*- coding:utf-8 -*-
__author__ = 'jixiufeng'

import tornado.web

class PingHandler(tornado.web.RequestHandler):
    """ handler """
    def get(self):
        self.write('pong')
    def post(self):
        self.write("pong")
