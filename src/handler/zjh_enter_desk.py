#  -*- coding:utf-8 -*-
__author__ = 'jixiufeng'

#  -*- coding:utf-8 -*-
__author__ = 'jixiufeng'

import tornado
from tornado import  gen
from tornado.web import asynchronous
from handler.base import BaseHandler
import sys
import json
from datetime import datetime, timedelta
import time
import redis_notify
import conf
from db.db_dynamic_version_update import DynamicVersionUpdate
from db.db_version_update import VersionUpdate
from db.db_server_version import ServerVersion
import app

#
class ZjhEnterDeskDayPlayerCntRender(BaseHandler):
    @asynchronous
    @gen.coroutine
    def self_get(self):
        self.render("zjh_enter_desk_player_cnt.html",title="统计每天各房间玩家数")

class ZjhEnterDeskDayPlayerCnt(BaseHandler):
    def mapRow(self,row):
        return row[0]           # cnt

    @asynchronous
    @gen.coroutine
    def self_post(self):
        tStr = self.get_argument('time','')
        t=time.strptime(tStr,"%Y-%m-%d")
        startTime=datetime(*t[:3])
        endTime=startTime+timedelta(days=1)

        roomList= yield app.DBMgr.getBRoomDB().select_all()
        result=[]
        for roomInfo in roomList:
            sql="select count( distinct uin) as cnt from ZJHDeskEnterLog where RoomId=%d and Time>'%s' and Time<'%s' "%(
                roomInfo['roomId'],startTime.strftime("%Y-%m-%d %H:%M:%S"), endTime.strftime("%Y-%m-%d %H:%M:%S"))
            cnt=yield app.DBMgr.getGMToolDB().query(sql,self.mapRow)
            roomInfo['cnt']=cnt
            result.append(roomInfo)
        print(result)
        self.write(json.dumps(result))
