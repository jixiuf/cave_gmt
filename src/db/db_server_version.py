#  -*- coding:utf-8 -*-
from tornado import  gen

class ServerVersion:
    def __init__(self):
        self.platform=0
        self.comments=""
        self.maxVesion=0
        self.midVersion = 0
        self.minVersion = 0
        self.showVersion = ""

class ServerVersionDB:
    def __init__(self,dbtemplate):
        self.dbtemplate=dbtemplate

    @gen.coroutine
    def create_table(self):
        query = "CREATE TABLE IF NOT EXISTS server_version ("\
          "platform int default 0 comment '平台号',"\
          "comments varchar(256) not null default '此行随便写注释'  COMMENT '' ,"\
          "max_version int default 0 not null,"\
          "mid_version int default 0 not null,"\
          "min_version int default 0 not null,"\
          "show_version varchar(13) default '' not null,"\
          "primary key(platform))"\
        "ENGINE = innodb DEFAULT CHARACTER SET utf8;"
        yield self.dbtemplate.execDDL(query)
    @gen.coroutine
    def truncate_table(self):
        query="truncate table server_version "
        yield self.dbtemplate.execDDL(query)



    def mapRow(self,row):
        sv=ServerVersion()
        sv.platform=row[0]
        sv.comments=row[1]
        sv.maxVesion=row[2]
        sv.midVersion=row[3]
        sv.minVersion=row[4]
        sv.showVersion=row[5]
        return sv

    @gen.coroutine
    def select(self,platform):
        query="select platform,comments,max_version,mid_version,min_version,show_version from server_version where platform=%d"%(platform)
        res=yield self.dbtemplate.queryObject(query,self.mapRow)
        raise gen.Return(res)
    @gen.coroutine
    def select_all(self):
        query="select platform,comments,max_version,mid_version,min_version,show_version from server_version "
        res=yield self.dbtemplate.query(query,self.mapRow)
        raise gen.Return(res)

    @gen.coroutine
    def add(self,sv):
        query="insert ignore into server_version(platform,comments,max_version,mid_version,min_version,show_version) values(%d,'%s',%d,%d,%d,'%s')"%(sv.platform,sv.comments,sv.maxVesion,sv.midVersion,sv.minVersion,sv.showVersion)
        print(query)
        result=yield self.dbtemplate.execSql(query)
        raise gen.Return(result)

    @gen.coroutine
    def update(self,sv):
        query="update server_version set comments='%s',max_version=%d,mid_version=%d,min_version=%d,show_version='%s' where platform=%d"%(sv.comments,sv.maxVesion,sv.midVersion,sv.minVersion,sv.showVersion,sv.platform)
        result=yield self.dbtemplate.execSql(query)
        raise gen.Return(result)
