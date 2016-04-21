#  -*- coding:utf-8 -*-
from tornado import  gen
from datetime import datetime, timedelta
class User:
    def __init__(self):
        self.uin=0
        self.autoIncrementId=0
        self.accountId=""
        self.password  = ""
        self.accountType = 0
        self.server=0
        self.channel=0
        self.uuid=''
        self.osVersion=''
        self.createTime= datetime.now()
    def __str__(self):
        return "player{uin=%d,accountId=%s,password=%s,accountType=%d,server=%d,channel=%d,uuid=%s,osVersion=%s,createtime=%s}"%(self.uin,self.accountId,self.password,self.accountType,self.server,self.channel,self.uuid,self.osVersion,self.createTime)


class UserDB:
    def __init__(self,dbtemplate,mode):
        self.dbtemplate=dbtemplate



    def mapRow(self,row):
        d=User()
        d.uin         =row[ 0]
        d.accountId   =row[ 1]
        d.password    =row[ 2]
        d.accountType =row[ 3]
        d.platform    =row[ 4]
        d.server      =row[ 5]
        d.channel     =row[ 6]
        d.uuid        =row[ 7]
        d.ip          =row[ 8]
        d.os          =row[ 9]
        d.osVersion   =row[10]
        d.deviceModel =row[11]
        d.createTime  =row[12]
        return d

    @gen.coroutine
    def select_by_uin(self,uin):
        query="select uin,accountId,password,accountType,platform,server,channel,uuid,ip,os,osVersion,deviceModel,createTime from user where uin=%s"%(uin)
        print query
        res=yield self.dbtemplate.queryObject(query,self.mapRow)
        raise gen.Return(res)
