#  -*- coding:utf-8 -*-
__author__ = 'jixiufeng'


import utils
from base_handler import *
from tornado.web import asynchronous

class Maintain(BaseHandler):
    @asynchronous
    @gen.coroutine
    def self_get(self):
        # packs=yield self.application.dbmgr.presentPackDB.select_all()
        self.render("maintain.html",title="维护公告")
    def self_post(self):
        serverIdStr=self.get_argument('serverId')
        content=self.get_argument('content')
        # packs=yield self.application.dbmgr.presentPackDB.select_all()
        self.render("maintain.html",title="维护公告")
