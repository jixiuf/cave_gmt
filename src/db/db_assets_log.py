#  -*- coding:utf-8 -*-
from tornado import  gen
from datetime import datetime, timedelta
class AssetsLog:
    def __init__(self):
        self.uin=0
        self.SUin=""
        self.AssetsType  = 0
        self.BeforeValue  = 0
        self.AfterValue=0
        self.ChangeValue=0
        self.Reason=""
        self.Time = datetime.now()


class AssetsLogDB:
    def __init__(self,dbtemplate):
        self.dbtemplate=dbtemplate


    def mapRow(self,row):
        d             =AssetsLog()
        d.uin         =row[ 0 ]
        d.SUin        =row[ 1 ]
        d.AssetsType  =row[ 2 ]
        d.BeforeValue =row[ 3 ]
        d.AfterValue  =row[ 4 ]
        d.ChangeValue = row[ 5 ]
        d.Reason      = row[ 6 ]
        d.Time        = row[ 7 ]
        return d

    @gen.coroutine
    def truncate_table(self):
        query="truncate table Assets "
        yield self.dbtemplate.execDDL(query)

    @gen.coroutine
    def select_all(self,uin,startTime,endTime):
        query="select Uin,SUin,AssetsType,BeforeValue,AfterValue,ChangeValue,Reason,Time from AssetsLog  where uin=%s and Time>'%s' and Time<'%s' order by time desc"%(uin,startTime,endTime)
        res=yield self.dbtemplate.query(query,self.mapRow)
        raise gen.Return(res)

