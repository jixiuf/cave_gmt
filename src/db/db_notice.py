#  -*- coding:utf-8 -*-
__author__ = 'jixiufeng'

from tornado import  gen
class NoticeDB:

    def __init__(self,dbtemplate):
        self.dbtemplate=dbtemplate

    def mapRow(self,row):
        d={}
        d['id']         = row[0]
        d['title']      = row[1]
        d['content']    = row[2]
        d['url']        = row[3]
        d['updateTime'] = row[4]
        d['startTime']  = row[5]
        d['endTime']    = row[6]
        d['sequenceId'] = row[7]
        return d
    @gen.coroutine
    def select(self,serverId,now):
        query="select id,title,content,url,updateTime,startTime,endTime,sequenceId from notice where sequenceId > 0 and serverId=%d order by sequenceId"%int(serverId)
        res=yield self.dbtemplate.query(query,self.mapRow)
        raise gen.Return(res)

    @gen.coroutine
    def get_notice(self,serverId,now):
        query="select id,title,content,url,updateTime,startTime,endTime,sequenceId from notice where sequenceId = 0 and serverId='%s' order by updateTime"%int(serverId)
        res=yield self.dbtemplate.query(query,self.mapRow)
        raise gen.Return(res)

    @gen.coroutine
    def add(self,title,content,serverId,updateTime,startTime,endTime):
        query="insert into notice(title,content,serverid,updateTime,startTime,endTime) values('%s','%s',%d,'%s','%s','%s')"%(title,content,int(serverId),updateTime,startTime,endTime)
        yield self.dbtemplate.execSql(query)


    @gen.coroutine
    def remove_url(self):
        query="update notice set url='' where sequenceId in (1,2)"
        yield self.dbtemplate.execSql(query)

    @gen.coroutine
    def remove_notice(self,ids):
        query="update notice set sequenceId='0' where id in (%s)"%(ids)
        yield self.dbtemplate.execSql(query)

    @gen.coroutine
    def set_sequence(self,id,sequenceId):
        query="update notice set sequenceId=%s where id=%s"%(sequenceId,id)
        yield self.dbtemplate.execSql(query)

    @gen.coroutine
    def update_url(self,urlfirst,urlsecound):
        query="update notice set url='%s' where sequenceId='1'"%(urlfirst)
        yield self.dbtemplate.execSql(query)
        query="update notice set url='%s' where sequenceId='2'"%(urlsecound)
        yield self.dbtemplate.execSql(query)

