#  -*- coding:utf-8 -*-
from tornado import  gen
from datetime import datetime, timedelta
import dbtemplate.dbtemplate
class UserAttr:
    def __init__(self):
        self.uin=0
        self.lastOfflineTime= datetime.now()
        self.energy= 0
        self.nickName=''
        self.gold=0
        self.gem=0
        self.sdkGem=0
        self.rmb=0
        self.relics=0
        self.air=0
        self.rebornCount=0
    def __str__(self):
        return "UserAttr{uin=%d,lastoffTime=%s,energy=%d,nickName=%s,gold=%f,gem=%f,sdkGem=%f,rmb=%f,relics=%f,air=%f,rebornCount=%d}"%(self.uin,self.lastoffTime,self.energy,self.nickName,self.gold,self.gem,self.sdkGem,self.rmb,self.relics,self.air,self.rebornCount)


class UserAttrDB:
    def __init__(self,dbtemplate):
        self.dbtemplate=dbtemplate
    def mapRow(self,row):
        d=UserAttr()
        d.uin         =row[0 ]
        d.lastoffTime =row[1 ]
        d.energy      =row[2 ]
        d.nickName    =row[3 ]
        d.gold        =row[4 ]
        d.gem         =row[5 ]
        d.sdkGem      =row[6 ]
        d.rmb         =row[7 ]
        d.relics      =row[8 ]
        d.air         =row[9 ]
        d.rebornCount =row[10 ]
        return d

    @gen.coroutine
    def select_by_uin(self,uin):
        query="select uin,lastoffTime,energy,nickName,gold,gem,sdkGem,rmb,relics,air,rebornCount from user_attr where uin=%s"%(uin)
        res=yield self.dbtemplate.queryObject(query,self.mapRow,dbtemplate.dbtemplate.Uint64Sum(uin))
        raise gen.Return(res)
