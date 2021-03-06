#  -*- coding:utf-8 -*-
from tornado import  gen

class DynamicVersionUpdate:
    def __init__(self):
        self.channel=0
        self.version=0
        self.comment=''
        self.size=0
        self.url = ""
        self.svnVersion=0
        self.note=0
    def toJsonObj(self):
      data={}
      data["channel"]=self.channel
      data["version"]=self.version
      data["comment"]=self.comment
      data["size"]=self.size
      data["url"]=self.url
      data["svnVersion"]=self.svnVersion
      data["note"]=self.note
      return data


class DynamicVersionUpdateDB:
    def __init__(self,dbtemplate):
        self.dbtemplate=dbtemplate

    @gen.coroutine
    def create_table(self):
        query = "CREATE TABLE IF NOT EXISTS dynamic_ver_update ("\
                "channel int default 0,"\
                "version int default 0,"\
                "url varchar(256) default '',"\
                "size int default 0,"\
                "comment varchar(1024) default '',"\
                "note varchar(128) default '',"\
                "svnVersion int default 0,"\
                "create_time timestamp not null default CURRENT_TIMESTAMP,"\
                "primary key (channel ,version))"\
                "ENGINE = innodb DEFAULT CHARACTER SET utf8;"

        yield self.dbtemplate.execDDL(query)
    @gen.coroutine
    def truncate_table(self):
        query="truncate table dynamic_ver_update "
        yield self.dbtemplate.execDDL(query)



    def mapRow(self,row):
        info=DynamicVersionUpdate()
        info.channel=row[0]
        info.version=row[1]
        info.url = row[2]
        info.size=row[3]
        info.comment=row[4]
        info.note=row[5]
        info.svnVersion=row[6]
        info.createTime=row[7]
        return info

    @gen.coroutine
    def select_max_version(self,channel):
        query="select channel,version,url,size,comment,note,svnVersion,create_time from dynamic_ver_update where channel=%d order by version desc limit 0,1"%(channel)
        res=yield self.dbtemplate.queryObject(query,self.mapRow)
        raise gen.Return(res)
    @gen.coroutine
    def select(self,channel,version):
        query="select channel,version,url,size,comment,note,svnVersion,create_time from dynamic_ver_update where channel=%d and version=%d order by version asc"%(channel,version)
        res=yield self.dbtemplate.queryObject(query,self.mapRow)
        raise gen.Return(res)
    @gen.coroutine
    def select_all(self):
        query="select  channel,version,url,size,comment,note,svnVersion,create_time from dynamic_ver_update"%()
        res=yield self.dbtemplate.query(query,self.mapRow)
        raise gen.Return(res)

    @gen.coroutine
    def add(self,info):
        query="insert ignore into dynamic_ver_update(channel,version,url,size,comment,note,svnVersion,create_time) values(%d,%d,'%s',%d,'%s','%s',%d,now())"%(info.channel,info.version,info.url,info.size,info.comment,info.note,info.svnVersion)
        result=yield self.dbtemplate.execSql(query)
        raise gen.Return(result)

    @gen.coroutine
    def update(self,info):
        query="update dynamic_ver_update set comment='%s',url='%s',note='%s',svnVersion=%d,size=%d where channel=%d and version =%d"%(info.comment,info.url,info.note,info.svnVersion,info.size,info.channel,info.version)
        result=yield self.dbtemplate.execSql(query)
        raise gen.Return(result)
