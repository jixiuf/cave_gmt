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
        timeStart = self.get_argument('timeStart','')
        timeEnd= self.get_argument('timeEnd','')
        channel= int(self.get_argument('channel','0'))
        if self.gmAccount.channel!=0:
            channel=self.gmAccount.channel

        print(self.gmAccount)
        if channel!=0:
            if where=='':
                where="channel=%d"%(channel)
            else:
                where+=" and channel=%d"%(channel)
        else:
            print("channel",channel)

        if timeStart!='':
            if where=='':
                where="create_time>'%s'"%(timeStart+(" 00:00:00"))
            else:
                where+=" and create_time>'%s'"%(timeStart+(" 00:00:00"))
        if timeEnd!='':
            if where=='':
                where="create_time<'%s'"%(timeEnd+(" 00:00:00"))
            else:
                where+=" and create_time<'%s'"%(timeEnd+(" 00:00:00"))


        if sort=="":
            sort="create_time desc"

        payOrderList=yield app.DBMgr.getPayOrderDB().select_all(sort,where)
        moneyTotal=0
        for idx in payOrderList:
            moneyTotal+=idx.money

        self.render("pay_order_list.html", title="定单信息列表",
                    Account=self.gmAccount,
                    timeStart=timeStart,
                    defaultChannel=channel,
                    timeEnd=timeEnd,
                    moneyTotal=moneyTotal,
                    payOrderList=payOrderList,channelMap=conf.getChannelNameMap())

