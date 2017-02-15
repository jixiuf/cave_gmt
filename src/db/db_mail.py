#  -*- coding:utf-8 -*-
__author__ = 'jixiufeng'

#  -*- coding:utf-8 -*-
from tornado import  gen
from datetime import datetime, timedelta
import db.dbtemplate.dbtemplate
class Mail:
    def __init__(self):
        self.uin=0
        self.startTime= datetime.now()
        self.endTime= datetime.now()+ timedelta(days=7)
    def __str__(self):
        return "mail{uin=%d}"%(self.uin)


class MailDB:
    def __init__(self,dbtemplate):
        self.dbtemplate=dbtemplate


    @gen.coroutine
    def truncate_table(self):
        query="truncate table mail"
        yield self.dbtemplate.execDDL(query)

    @gen.coroutine
    def add(self,mailId,uin,startTime,endTime,awardStr,conent):
        query="insert into MailSystem (mailId,uin,FromUin,MailType,StartTime,EndTime,AwardStr,Content,Reason) values(%d,%s,0,0,'%s','%s','%s','%s','system')"%(mailId,uin,startTime,endTime,awardStr,conent)
        print(query)
        yield self.dbtemplate.execSql(query,db.dbtemplate.dbtemplate.Uint64Sum(uin))

