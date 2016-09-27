#  -*- coding:utf-8 -*-
__author__ = 'jixiufeng'

import tornado
from tornado import  gen
from tornado.web import asynchronous
from handler.base import BaseHandler
import sys
import json
import time
import redis_notify
import conf
from db.db_dynamic_version_update import DynamicVersionUpdate
from db.db_version_update import VersionUpdate
from db.db_server_version import ServerVersion
import app

class ZJHRoomAIControl(BaseHandler):
    @asynchronous
    @gen.coroutine
    def self_get(self):
        roomList= yield app.DBMgr.getBRoomDB().select_all()
        redisKV=app.Redis.hgetall("zjh_invite_ai")

        result=[]
        for roomInfo in roomList:
            redisV=redisKV.get(str(roomInfo['roomId']),None)
            if redisV==None or redisV=="false":
                roomInfo['allowAI']="false"
            else:
                roomInfo['allowAI']="true"
            result.append(roomInfo)


        self.render("zjh_room_ai_control.html",title="动态更新",result=result)


class ZJHRoomAIControlUpdate(BaseHandler):
    @asynchronous
    def self_post(self):
        roomId=self.get_argument('roomId','1')
        status=self.get_argument('status','true')
        app.Redis.hset("zjh_invite_ai",str(roomId),status)
        time.sleep(0.01)
        self.write(json.dumps({ 'action': 'success'}))
