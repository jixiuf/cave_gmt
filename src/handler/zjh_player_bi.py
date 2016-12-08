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
from db.db_bi_user import BIUser
import app

@gen.coroutine
def fetch_data(dayStr,channelStr):
    t=time.strptime(dayStr,"%Y-%m-%d")
    startTime=datetime(*t[:3])
    endTime=startTime+timedelta(days=1)

    biUser=BIUser()
    biUser.channel=int(channelStr)
    biUser.day=dayStr
    def mapRow(row):
        return row[0]           # cnt

    try:
        result=[]
        sql="select count(uin) as new_user_cnt from LoginLog where IsNew=1 and Time>'%s' and Time<'%s' "%(startTime.strftime("%Y-%m-%d %H:%M:%S"), endTime.strftime("%Y-%m-%d %H:%M:%S"))
        if channelStr!='0':
            sql+= " and channel=%s"%(channelStr)

        biUser.newUserCnt=yield app.DBMgr.getGMToolDB().queryObject(sql,mapRow)


        sql="select count(distinct uin) as active_user_cnt from LoginLog where Time>'%s' and Time<'%s' "%(startTime.strftime("%Y-%m-%d %H:%M:%S"), endTime.strftime("%Y-%m-%d %H:%M:%S"))
        if channelStr!='0':
            sql+= " and channel=%s"%(channelStr)
        biUser.activeUserCnt=yield app.DBMgr.getGMToolDB().queryObject(sql,mapRow)

        biUser.payUserCnt=yield app.DBMgr.getPayOrderDB().select_user_cnt(startTime,endTime,channelStr)

        biUser.payNewUserCnt=yield app.DBMgr.getPayOrderDB().select_new_user_cnt(startTime,endTime,channelStr)
        biUser.money=yield app.DBMgr.getPayOrderDB().select_sum(startTime,endTime,channelStr)

    except Exception, error:
        print('errormsg\t%s' % (str(error),))
        print('errortrace\t%s' % (str(traceback.format_exc()),))
    raise gen.Return(biUser)

@gen.coroutine
def update_data():
    now=datetime.now()
    dayStr = "%d-%0.2d-%0.2d"%(now.year,now.month,now.day)

    biUser=yield fetch_data(dayStr,'0')
    yield app.DBMgr.biUserDB.add(biUser)
    for channel in conf.getChannelList():
        biUser=yield fetch_data(dayStr,str(channel))
        yield app.DBMgr.biUserDB.add(biUser)

    raise gen.Return("")

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
    @asynchronous
    @gen.coroutine
    def self_post(self):

        now=datetime.now()
        dayStr = "%d-%0.2d-%0.2d"%(now.year,now.month,now.day)

        channelStr = self.get_argument('channel','0')
        if self.gmAccount.channel!=0 and channelStr!=str(self.gmAccount.channel):
            self.write(json.dumps({"result":"wrong channel"+str(self.gmAccount.channel)}))
            return

        biUser=yield fetch_data(dayStr,channelStr)
        list=yield app.DBMgr.biUserDB.select_all(channelStr)
        if len(list)>0:
            if list[0].day!=biUser.day:
                list.insert(0,biUser)
        else:
            list.insert(0,biUser)

        result=[]
        biUserTotal=BIUser()
        biUserTotal.channel=int(channelStr)
        biUserTotal.day="合计"

        for tmpBIUser in list:
            result.append(tmpBIUser.toJsonObj())
            biUserTotal.newUserCnt+=tmpBIUser.newUserCnt
            biUserTotal.activeUserCnt+=tmpBIUser.activeUserCnt
            biUserTotal.payUserCnt+=tmpBIUser.payUserCnt
            biUserTotal.payNewUserCnt+=tmpBIUser.payNewUserCnt
            biUserTotal.money+=tmpBIUser.money
        result.insert(0,biUserTotal.toJsonObj())


        self.write(json.dumps({'result':'',"data":result}))

