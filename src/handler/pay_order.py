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

class PayOrderHandler(BaseHandler):
    @asynchronous
    @gen.coroutine
    def self_get(self):
        sort = self.get_argument('sort','')
        where= self.get_argument('where','')
        print(self.gmAccount)
        channel= self.gmAccount.channel
        if channel!=0:
            if where=='':
                where="channel=%d"%(channel)
            else:
                where+=" and channel=%d"%(channel)
        else:
            print("channel",channel)


        print("ww",where)

        if sort=="":
            sort="create_time desc"

        payOrderList=yield app.DBMgr.getPayOrderDB().select_all(sort,where)
        self.render("pay_order_list.html", title="定单信息列表",
                    Account=self.gmAccount,
                    payOrderList=payOrderList,channelMap=conf.getChannelNameMap())

