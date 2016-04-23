#  -*- coding:utf-8 -*-
__author__ = 'jixiufeng'


from datetime import datetime, timedelta
import utils
import redis_notify
from base_handler import BaseHandler
from tornado.web import asynchronous
from tornado import  gen

class Maintain(BaseHandler):
    @asynchronous
    @gen.coroutine
    def self_get(self):
        serverIdList= self.application.dbmgr.get_all_server_id()
        maintainList=yield self.application.dbmgr.maintainDB.select_all()
        self.render("maintain.html",title="维护公告",maintainList=maintainList,serverIdList=serverIdList)
    @asynchronous
    @gen.coroutine
    def self_post(self):
        serverIdStr=self.get_argument('serverId')
        content=self.get_argument('content')
        now=datetime.now()
        day7FromNow=now+ timedelta(days=7)
        yield self.application.dbmgr.maintainDB.add(serverIdStr,content,now,day7FromNow)
        self.application.redis.publish(redis_notify.get_platform_redis_notify_channel(conf.PLATFORM), redis_notify.NOTIFY_TYPE_RELOAD_MAINTAIN)
        self.write('success')
class MaintainDelete(BaseHandler):
    @asynchronous
    @gen.coroutine
    def self_post(self):
        serverIdStr=self.get_argument('serverId')
        info={}
        yield self.application.dbmgr.maintainDB.delete(serverIdStr)
        self.application.redis.publish(redis_notify.get_platform_redis_notify_channel(conf.PLATFORM), redis_notify.NOTIFY_TYPE_RELOAD_MAINTAIN)
        self.write('success')

        # maintainList=yield self.application.dbmgr.maintainDB.select_all()
        # self.render("maintain.html",title="维护公告",maintainList=maintainList)
