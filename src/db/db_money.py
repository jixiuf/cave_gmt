#  -*- coding:utf-8 -*-
__author__ = 'jixiufeng'

#  -*- coding:utf-8 -*-
from tornado import  gen
from datetime import datetime, timedelta
import db.dbtemplate.dbtemplate
class Money:
    def __init__(self):
        self.uin=0
    def __str__(self):
        return "Money{uin=%d}"%(self.uin)


class MoneyDB:
    def __init__(self,dbtemplate):
        self.dbtemplate=dbtemplate


    @gen.coroutine
    def truncate_table(self):
        query="truncate table Money"
        yield self.dbtemplate.execDDL(query)

    def mapRow(self,row):
        money          =Money()
        money.uin      =row[ 0 ]
        money.gold     =row[ 1 ]
        money.gem      =row[ 2 ]
        money.speaker  =row[ 3 ]
        money.vipValue =row[ 4 ]
        money.kickCard =row[ 5 ]
        money.watch    =row[ 6 ]
        money.car      =row[ 7 ]
        money.house    =row[ 8 ]
        money.boat     =row[ 9 ]
        return money

    @gen.coroutine
    def select_by_uin(self,uin):
        query="select uin, gold, gem, speaker, vipValue, kickCard, watch, car, house, boat from Money where uin=%s"%(uin)
        res=yield self.dbtemplate.queryObject(query,self.mapRow,db.dbtemplate.dbtemplate.Uint64Sum(int(uin)))
        if res!=None:
            lastPayTime=yield self.select_lastPayTime(uin)
            res.lastPayTime=lastPayTime
        raise gen.Return(res)
    @gen.coroutine
    def update(self,uin,gold ,gem,speaker,vipValue,kickCard,watch,car,house,boat):
        query="update Money set gold=%d,gem=%d,speaker=%d,vipValue=%d,kickCard=%d,watch=%d,car=%d,house=%d,boat=%d  where uin=%s"%(
            int(gold),int(gem),int(speaker),int(vipValue),int(kickCard),int(watch),int(car),int(house),int(boat),str(uin))
        print(query)
        yield self.dbtemplate.execSql(query,db.dbtemplate.dbtemplate.Uint64Sum(int(uin)))


    @gen.coroutine
    def select_lastPayTime(self,uin):
        query="select lastPayTime from Vip where uin=%s"%(str(uin))
        def mapRowVip(row):
            return row[0]
        res=yield self.dbtemplate.queryObject(query,mapRowVip,db.dbtemplate.dbtemplate.Uint64Sum(int(uin)))
        raise gen.Return(res)

