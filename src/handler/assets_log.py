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

class AssetsLogHandler(BaseHandler):
    @asynchronous
    @gen.coroutine
    def self_get(self):
        tStr = self.get_argument('time','')
        if tStr=='':
            self.write(json.dumps({"result":"请选择日期"}))
            return

        t=time.strptime(tStr,"%Y-%m-%d")
        startTime=datetime(*t[:3])
        endTime=startTime+timedelta(days=1)


        uin = self.get_argument('uin','')

        assetsLogList=yield app.DBMgr.getAssetsLogDB().select_all(uin,startTime,endTime)
        self.render("assets_log_list.html", title="资产流水日志",assetsLogList=assetsLogList,
                    Account=self.gmAccount,

                    channelMap=conf.getChannelNameMap())

