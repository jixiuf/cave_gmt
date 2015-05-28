#  -*- coding:utf-8 -*-
from tornado import  gen
class Maintain:
    def __init__(self):
        self.serverId=0
        self.content=""
        # self.startTime
        # self.endTime

class PresentPackDB:
    def __init__(self,dbtemplate):
        self.dbtemplate=dbtemplate

    @gen.coroutine
    def create_table(self):
        query = "CREATE TABLE IF NOT EXISTS maintain ("\
        "serverid int NOT NULL  COMMENT 'serverid' ,"\
        "content varchar(1024) NOT NULL  COMMENT '维护公告' default '',"\
        "startTime timestamp not null default 0 comment '邮件开始时间',"\
        "endTime timestamp not null default 0 comment '邮件结束时间',"\
        "PRIMARY KEY (serverId)) ENGINE = innodb DEFAULT CHARACTER SET utf8;"

        yield self.dbtemplate.execDDL(query)
    def mapRow(self,row):
        d=Maintain()
        d.serverId      = row[0]
        d.content    = row[1]
        d.startTime = row[2]
        d.endTime    = row[3]
        return d
    @gen.coroutine
    def truncate_table(self):
        query="truncate table maintain"
        yield self.dbtemplate.execDDL(query)

    @gen.coroutine
    def add(self,serverId,content,startTime,endTime):
        query="insert into maintain(serverId,content,startTime,endTime) values('%s','%s','%s',%s,'%s','%s')"%(serverId,content,'',endTime,'',status)
        yield self.dbtemplate.execSql(query)

    @gen.coroutine
    def select_all(self):
        query="select id,serverId,content,startTime,endTime,extra,status,hide from maintain order by id desc"
        res=yield self.dbtemplate.query(query,self.mapRow)
        raise gen.Return(res)

