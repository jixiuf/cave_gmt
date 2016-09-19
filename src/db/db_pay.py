#  -*- coding:utf-8 -*-
from tornado import  gen
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


    def mapRow(self,row):
        d=PayOrder()
        d.uin          =row[ 0 ]
        d.accountId    =row[ 1 ]
        d.order_id     =row[ 2 ]
        d.sdk_order_id =row[ 3 ]
        d.product_id   =row[ 4 ]
        d.product_name = row[ 5 ]
        d.money        = row[ 6 ]
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
    def select_all(self,sort):
        query="select `uin`, `account_id`, `order_id`, `sdk_order_id`, `product_id`, `product_name`, `money`, `channel`, `payType`, `server`, `status`, `order_type`, `receipt_data`, `create_time` from pay_order  order by %s "%(sort)
        print(query)
        res=yield self.dbtemplate.query(query,self.mapRow)
        raise gen.Return(res)

