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

class BICurrencyChangeHandler(BaseHandler):
    @asynchronous
    @gen.coroutine
    def self_get(self):
        tStr = self.get_argument('time','')
        currencyChangeList=[]
        if tStr=='':
            self.write(json.dumps({"result":"请选择日期"}))
            return
        t=time.strptime(tStr,"%Y-%m-%d")
        startTime=datetime(*t[:3])
        endTime=startTime+timedelta(days=1)


        uin = self.get_argument('uin','')

        currencyChangeList=yield app.DBMgr.getCurrencyChangeDB().select_all(uin,startTime,endTime)
        self.render("bi_currency_change_list.html", title="货币变化日志",
                    currencyChangeList=currencyChangeList,
                    time=tStr,
                    Account=self.gmAccount,
                    channelMap=conf.getChannelNameMap())

