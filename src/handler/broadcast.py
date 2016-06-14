#  -*- coding:utf-8 -*-
__author__ = 'jixiufeng'


from datetime import datetime, timedelta
import utils
import redis_notify
from handler.base import BaseHandler
from tornado.web import asynchronous
from tornado import  gen
import app
import conf
import json

class Broadcast(BaseHandler):
    @asynchronous
    @gen.coroutine
    def self_get(self):
        serverIdList= app.DBMgr.get_all_server_id()
        self.render("broadcast.html",title="紧急公告",serverIdList=serverIdList)
    @asynchronous
    @gen.coroutine
    def self_post(self):
        serverIdStr=self.get_argument('serverId')
        content=self.get_argument('content')
        # {144150688393216252 2 24 {"head_icon":1,"nickname":"游客00252","content_type":"normal","sex":1}}
        chatInfo={'chat_type':3,'content':'%s'%content} # chat_type_broadcast
        # chatInfo={'chat_type':3,'content':'%s'%content,'params':'{"head_icon":1,"nickname":"GM","content_type":"normal","sex":1}'} # chat_type_broadcast
        app.Redis.publish(redis_notify.get_server_redis_notify_channel(conf.PLATFORM,serverIdStr), redis_notify.NOTIFY_TYPE_BROADCAST%(json.dumps(chatInfo)))
        self.write('success')