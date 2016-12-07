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
class BIPlayerRender(BaseHandler):
    @asynchronous
    @gen.coroutine
    def self_get(self):
        self.render("zjh_bi_player.html",
                    Account=self.gmAccount,
                    channelMap=conf.getChannelNameMap(),
                    title="用户信息统计(新增-活跃-付费)")
# 账户管理 按渠道

# 新增用户按（渠道查日期）
# 活跃用户（指定渠道 查日期） 今天登录过游戏的人

# 付费用户（指定渠道 查日期）
# 新增付费用户（指定渠道 选日期） 当天

# 定单列表 按渠道
class BIPlayer(BaseHandler):
    def mapRow(self,row):
        return row[0]           # cnt

    @asynchronous
    @gen.coroutine
    def self_post(self):
        tStr = self.get_argument('time','')
        channelStr = self.get_argument('channel','0')
        if self.gmAccount.channel!=0 and channelStr!=str(self.gmAccount.channel):
            self.write(json.dumps({"result":"wrong channel"+str(self.gmAccount.channel)}))
            return


        if tStr=='':
            self.write(json.dumps({"result":"请选择日期"}))
            return

        t=time.strptime(tStr,"%Y-%m-%d")
        startTime=datetime(*t[:3])
        endTime=startTime+timedelta(days=1)

        try:
            result=[]
            sql="select count(uin) as new_user_cnt from LoginLog where IsNew=1 and Time>'%s' and Time<'%s' "%(startTime.strftime("%Y-%m-%d %H:%M:%S"), endTime.strftime("%Y-%m-%d %H:%M:%S"))
            if channelStr!='0':
                sql+= " and channel=%s"%(channelStr)

            print(sql)
            newUserCnt=yield app.DBMgr.getGMToolDB().query(sql,self.mapRow)
            result.append({'name':'当日新增玩家','cnt':newUserCnt})


            sql="select count(distinct uin) as active_user_cnt from LoginLog where Time>'%s' and Time<'%s' "%(startTime.strftime("%Y-%m-%d %H:%M:%S"), endTime.strftime("%Y-%m-%d %H:%M:%S"))
            if channelStr!='0':
                sql+= " and channel=%s"%(channelStr)
            activeUserCnt=yield app.DBMgr.getGMToolDB().query(sql,self.mapRow)
            result.append({'name':'当日活跃玩家',"cnt":activeUserCnt})
            print(sql)

            payUserCnt=yield app.DBMgr.getPayOrderDB().select_user_cnt(startTime,endTime,channelStr)
            result.append({'name':'当日付费玩家','cnt':payUserCnt})

            payNewUserCnt=yield app.DBMgr.getPayOrderDB().select_new_user_cnt(startTime,endTime,channelStr)
            result.append({'name':'当日新增付费玩家','cnt':payNewUserCnt})





            self.write(json.dumps({'result':'',"data":result}))
        except Exception, error:
            self.application.logger.warning('errorarg\t%s\t%s\t%s' % (self.request.headers.get('channel','xxx'),self.request.headers.get('User-Agent','xxx'),str(self.request.arguments)))
            self.application.logger.warning('errormsg\t%s' % (str(error),))
            self.application.logger.warning('errortrace\t%s' % (str(traceback.format_exc()),))
            self.write(json.dumps({"result":"err"}))

