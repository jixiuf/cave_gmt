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
        channel= self.get_argument('channel','0')
        if self.gmAccount.channel!='0':
            if not channel in self.gmAccount.getChannelList():
                channel= self.gmAccount.channel

        if channel!='0':
            if where=='':
                where="channel in (%s)"%(channel)
            else:
                where+=" and channel in (%s)"%(channel)
        # else:

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

class PayOrderBIHandler(BaseHandler):
    @asynchronous
    @gen.coroutine
    def self_get(self):

        list=yield app.DBMgr.getPayOrderDB().select_group_product()
        totalMoney=0
        totalCnt=0
        for e in list:
            totalMoney=totalMoney+ e.get('sum')
            totalCnt=totalCnt+e.get('cnt')


        list2=yield app.DBMgr.getPayOrderDB().select_group_uin()
        data1={}
        data2={}
        data3={}
        data4={}
        for e in list2:
            # totalMoney=totalMoney+e.get('sum')
            # totalCnt=totalCnt+e.get('cnt')
            print(e)

            if e.get('sum')<100:
                data1['cnt']=data1.get('cnt',0)+e.get('cnt')
                data1['sum']=data1.get('sum',0)+e.get('sum')
                data1['usercnt']=data1.get('usercnt',0)+1
            elif e.get('sum')<500:
                data2['cnt']=data2.get('cnt',0)+e.get('cnt')
                data2['sum']=data2.get('sum',0)+e.get('sum')
                data2['usercnt']=data2.get('usercnt',0)+1
            elif e.get('sum')<1000:
                data3['cnt']=data3.get('cnt',0)+e.get('cnt')
                data3['sum']=data3.get('sum',0)+e.get('sum')
                data3['usercnt']=data3.get('usercnt',0)+1
            else:
                data4['cnt']=data4.get('cnt',0)+e.get('cnt')
                data4['sum']=data4.get('sum',0)+e.get('sum')
                data4['usercnt']=data4.get('usercnt',0)+1


        self.render("pay_order_stat.html", title="充值统计",
                    Account=self.gmAccount,
                    # defaultChannel=channel,
                    data1=data1,
                    data2=data2,
                    data3=data3,
                    data4=data4,
                    totalCnt=totalCnt,
                    totalMoney=totalMoney,
                    list=list,channelMap=conf.getChannelNameMap())
class PayOrderUserBIHandler(BaseHandler):
    @asynchronous
    @gen.coroutine
    def self_get(self):


        self.render("pay_order_uin.html", title="充值统计",
                    Account=self.gmAccount,
                    # defaultChannel=channel,
                    totalCnt=totalCnt,
                    totalMoney=totalMoney,
                    list2=list2,channelMap=conf.getChannelNameMap())
