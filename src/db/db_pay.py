#  -*- coding:utf-8 -*-
from tornado import  gen
import time
from datetime import datetime, timedelta
class PayOrder:
    def __init__(self):
        self.uin=0
        self.accountId=""
        self.order_id  = ""
        self.sdk_order_id  = ""
        self.product_id  = ""
        self.product_name  = ""
        self.money  = 0
        self.channel= 0
        self.payType= 0
        self.server= 0
        self.status= 0
        self.order_type= 0
        self.receipt_data= ""
        self.createTime= datetime.now()


class PayOrderDB:
    def __init__(self,dbtemplate):
        self.dbtemplate=dbtemplate

    def mapOne(self,row):
        return row[0]           # cnt

    def mapRow(self,row):
        d=PayOrder()
        d.uin          =row[ 0 ]
        d.accountId    =row[ 1 ]
        d.order_id     =row[ 2 ]
        d.sdk_order_id =row[ 3 ]
        d.product_id   =row[ 4 ]
        d.product_name = row[ 5 ]
        d.money        = row[ 6 ]/100
        d.channel      = row[ 7 ]
        d.payType      = row[ 8 ]
        d.server       = row[ 9 ]
        d.status       = row[10 ]
        d.order_type   = row[11 ]
        d.receipt_data = row[12 ]
        d.create_time  =row[13 ]
        return d

    @gen.coroutine
    def truncate_table(self):
        query="truncate table pay_order "
        yield self.dbtemplate.execDDL(query)

    @gen.coroutine
    def select_all(self,sort,where):
        query="select `uin`, `account_id`, `order_id`, `sdk_order_id`, `product_id`, `product_name`, `money`, `channel`, `payType`, `server`, `status`, `order_type`, `receipt_data`, `create_time` from pay_order "
        if where!="":
            query+=" where "+where

        query+="  order by %s "%(sort)
        print(query)
        res=yield self.dbtemplate.query(query,self.mapRow)
        raise gen.Return(res)


    @gen.coroutine
    def select_user_cnt(self,startTime ,endTime,channel):
        query="select count(`uin`) as user_cnt from pay_order where create_time>'%s' and create_time<'%s'"%(startTime.strftime("%Y-%m-%d %H:%M:%S"), endTime.strftime("%Y-%m-%d %H:%M:%S"))
        if channel!='0' and channel!=None:
            query+= " and channel=%s"%(channel)


        res=yield self.dbtemplate.queryObject(query,self.mapOne)
        raise gen.Return(res)

# 新增付费用户（指定渠道 选日期） 当天
    @gen.coroutine
    def select_new_user_cnt(self,startTime ,endTime,channel):
        channelCheck=' '
        if channel!='0' and channel!=None:
            channelCheck= "  and p1.channel=%s"%(channel)


        query="select count(distinct p1.uin ) from pay_order p1    where p1.create_time>'%s' and p1.create_time<'%s' %s and not exists(select   `uin`  from pay_order p2 where p2.create_time<'%s'  and p2.uin=p1.uin)"%(
            startTime.strftime("%Y-%m-%d %H:%M:%S"), endTime.strftime("%Y-%m-%d %H:%M:%S"),channelCheck,startTime.strftime("%Y-%m-%d %H:%M:%S"))

        res=yield self.dbtemplate.queryObject(query,self.mapOne)
        raise gen.Return(res)


    @gen.coroutine
    def select_sum(self,startTime ,endTime,channel):
        query="select ifnull(sum(`money`),0)/100 as money from pay_order where create_time>'%s' and create_time<'%s'"%(startTime.strftime("%Y-%m-%d %H:%M:%S"), endTime.strftime("%Y-%m-%d %H:%M:%S"))
        if channel!='0' and channel!=None:
            query+= " and channel=%s"%(channel)

        res=yield self.dbtemplate.queryObject(query,self.mapOne)
        raise gen.Return(int(res))

