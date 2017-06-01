#  -*- coding:utf-8 -*-
from tornado import  gen

class VersionUpdate:
    def __init__(self):
        self.channel=0
        self.os=0
        self.comments=''
        self.url = ""

class VersionUpdateDB:
    def __init__(self,dbtemplate):
        self.dbtemplate=dbtemplate

    @gen.coroutine
    def create_table(self):
        query = "CREATE TABLE IF NOT EXISTS version_update("\
                "channel int default 0 ,"\
                "os int default 0,"\
                "comments varchar(1024) not null default ''  COMMENT '此行随便写注释' ,"\
                "url varchar(256) default '',"\
                "primary key(channel,os))"\
                "ENGINE = innodb DEFAULT CHARACTER SET utf8;"
        yield self.dbtemplate.execDDL(query)
    @gen.coroutine
    def truncate_table(self):
        query="truncate table version_update "
        yield self.dbtemplate.execDDL(query)



    def mapRow(self,row):
        vupdate=VersionUpdate()
        vupdate.channel=row[0]
        vupdate.os=row[1]
        vupdate.url=row[2]
        vupdate.comments=row[3]
        return vupdate

    @gen.coroutine
    def select(self,channel):
        query="select channel,os,url,comments from version_update where channel=%d order by os desc "%(channel)
        res=yield self.dbtemplate.queryObject(query,self.mapRow)
        raise gen.Return(res)
    @gen.coroutine
    def select_all(self):
        query="select channel,os,url,comments from version_update order by channel,os"
        res=yield self.dbtemplate.query(query,self.mapRow)
        raise gen.Return(res)

    @gen.coroutine
    def add(self,vupdate):
        query="insert ignore into version_update(channel,os,comments,url) values(%d,%d,'%s','%s') on duplicate key update url='%s',comments='%s' "%(vupdate.channel,vupdate.os,vupdate.comments,vupdate.url,vupdate.url,vupdate.comments)
        result=yield self.dbtemplate.execSql(query)
        raise gen.Return(result)

    @gen.coroutine
    def update(self,vupdate):
        query="update version_update set comments='%s',url='%s' where channel=%d and os =%d"%(vupdate.comments,vupdate.url,vupdate.channel,vupdate.os)
        result=yield self.dbtemplate.execSql(query)
        raise gen.Return(result)
