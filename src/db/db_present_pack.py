#  -*- coding:utf-8 -*-
from tornado import ioloop, gen
class PresentPackDB:
    def __init__(self,dbtemplate):
        self.dbtemplate=dbtemplate

    @gen.coroutine
    def create_table(self):
        query = "create table if not exists present_pack ("\
                "id BIGINT(20) NOT NULL AUTO_INCREMENT, " \
                "`name` varchar(255) NOT NULL DEFAULT '' COMMENT 'title'," \
                "`Content` varchar(255) NOT NULL DEFAULT '' COMMENT 'content'" \
                "`icon` varchar(255) NOT NULL DEFAULT '' COMMENT 'picture Url',"\
                "`version` bigint(20) NOT NULL," \
                "`created_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP," \
                "`extra` varchar(255) DEFAULT NULL,"\
                "`status` int(11) NOT NULL,"\
                "primary key(id))"\
                "ENGINE = InnoDB CHARACTER SET = utf8"
        yield self.dbtemplate.execDDL(query)
    def mapRow(self,row):
        d={}
        d['id']=row[0]
        d['name']=row[1]
        d['content']=row[2]
        d['icon']=row[3]
        d['version']=row[4]
        d['extra']=row[5]
        d['status']=row[6]
        d['hide']=row[7]
        return d
    @gen.coroutine
    def truncate_table(self):
        query="truncate table present_pack"
        yield self.dbtemplate.execDDL(query)

    @gen.coroutine
    def add(self,name,content,version,status):
        query="insert into present_pack(name,content,icon,version,extra,status) values('"+name+"','"+content+"','%s',%s,'%s',%s)"%('',version,'',status)
        yield self.dbtemplate.execSql(None,query)

    @gen.coroutine
    def select_all(self):
        query="select id,name,content,icon,version,extra,status,hide from present_pack order by id desc"
        res=yield self.dbtemplate.query(None,query,self.mapRow)
        raise gen.Return(res)

    @gen.coroutine
    def select_by_status(self,status):
        query="select id,name,content,icon,version,extra,status,hide from present_pack where status = 0 or status = %s order by id desc"%(action,)
        res=yield self.dbtemplate.query(None,query,self.mapRow)
        raise gen.Return(res)

    @gen.coroutine
    def get(self,id):
        cursor.execute("select id,name,content,icon,version,extra,status,hide from present_pack where id=%s"%(id,))
        res=yield self.dbtemplate.query(None,query,self.mapRow)
        raise gen.Return(res)

    @gen.coroutine
    def update_hide(self,id,hide):
        query="update present_pack set hide=%s where id=%s"%(hide,id)
        yield self.dbtemplate.execSql(None,query)
