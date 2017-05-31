#  -*- coding:utf-8 -*-
__author__ = 'jixiufeng'



from datetime import datetime, timedelta
from tornado import  gen
from handler.base import *
from tornado.web import asynchronous
import conf
import redis_notify
# import json
import app
import time

class BugReportHandler(BaseHandler):
    @asynchronous
    @gen.coroutine
    def self_get(self):

        sql="select uin,timePK,content,updateTime,status from BugReport order by status asc,updateTime desc"
        def mapRow(row):
            data={}
            data['uin']=row[0]
            data['timePK']=row[1]
            data['content']=row[2]
            data['updateTime']=row[3]
            data['status']=row[4]
            return data
        bugList=yield app.DBMgr.getProfileDB().query(sql,mapRow)

        self.render("bugreport.html", title="Bug上报处理",bugList=bugList,
                    Account=self.gmAccount,
                    channelMap=conf.getChannelNameMap())

    @asynchronous
    @gen.coroutine
    def self_post(self):
        uin= self.get_argument('uin','0')
        timePK= self.get_argument('timePK','0')

        sql="update BugReport set status=1 where uin=%s and timePK=%s"%(uin,timePK)
        yield app.DBMgr.getProfileDB().execSql(sql)
        self.write('success')
