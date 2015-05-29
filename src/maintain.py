#  -*- coding:utf-8 -*-
__author__ = 'jixiufeng'


from datetime import datetime, timedelta
import utils
from base_handler import *
from tornado.web import asynchronous

class Maintain(BaseHandler):
    @asynchronous
    @gen.coroutine
    def self_get(self):
        maintainList=yield self.application.dbmgr.maintainDB.select_all()
        self.render("maintain.html",title="维护公告",maintainList=maintainList)
    @asynchronous
    @gen.coroutine
    def self_post(self):
        serverIdStr=self.get_argument('serverId')
        content=self.get_argument('content')
        now=datetime.now()
        day7FromNow=now+ timedelta(days=7)
        yield self.application.dbmgr.maintainDB.add(serverIdStr,content,now,day7FromNow)
        self.write('success')
class MaintainDelete(BaseHandler):
    @asynchronous
    @gen.coroutine
    def self_post(self):
        serverIdStr=self.get_argument('serverId')
        info={}
        yield self.application.dbmgr.maintainDB.delete(serverIdStr)
        self.write('success')

        # maintainList=yield self.application.dbmgr.maintainDB.select_all()
        # self.render("maintain.html",title="维护公告",maintainList=maintainList)
