#  -*- coding:utf-8 -*-
__author__ = 'jixiufeng'

#  -*- coding:utf-8 -*-
__author__ = 'jixiufeng'

import traceback
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
        print("tStr",tStr)
        if tStr=='':
            self.write(json.dumps({"result":"请选择日期"}))
            return

        t=time.strptime(tStr,"%Y-%m-%d")
        startTime=datetime(*t[:3])
        endTime=startTime+timedelta(days=1)

        roomList= yield app.DBMgr.getBRoomDB().select_all()
        try:
            result=[]
            for roomInfo in roomList:
                sql="select count( distinct uin) as cnt from ZJHDeskEnterLog where RoomId=%d and Time>'%s' and Time<'%s' "%(
                    roomInfo['roomId'],startTime.strftime("%Y-%m-%d %H:%M:%S"), endTime.strftime("%Y-%m-%d %H:%M:%S"))
                cnt=yield app.DBMgr.getGMToolDB().query(sql,self.mapRow)
                roomInfo['cnt']=cnt
                result.append(roomInfo)
            self.write(json.dumps({'result':'',"data":result}))
        except Exception, error:
            self.application.logger.warning('errorarg\t%s\t%s\t%s' % (self.request.headers.get('channel','xxx'),self.request.headers.get('User-Agent','xxx'),str(self.request.arguments)))
            self.application.logger.warning('errormsg\t%s' % (str(error),))
            self.application.logger.warning('errortrace\t%s' % (str(traceback.format_exc()),))
            self.write(json.dumps({"result":"err"}))

