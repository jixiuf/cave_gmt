#  -*- coding:utf-8 -*-
__author__ = 'jixiufeng'

#  -*- coding:utf-8 -*-
from tornado import  gen
from datetime import datetime, timedelta
import db.dbtemplate.dbtemplate
import json

class MailDraftDB:
    def __init__(self,dbtemplate):
        self.dbtemplate=dbtemplate

    @gen.coroutine
    def create_table(self):
        query='''CREATE TABLE if not exists `MailDraft` (
  `MailId` bigint(20) NOT NULL COMMENT '唯一ID',
  `uin` bigint(20) NOT NULL COMMENT '此邮件的拥有者',
  `fromUin` bigint(20) NOT NULL COMMENT '此邮件的发送者',
  `mailType` smallint(6) NOT NULL DEFAULT '0' COMMENT '邮件类型',
  `createTime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '',
  `startTime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '邮件开始时间',
  `endTime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '邮件结束时间',
  `awardStr` varchar(64) NOT NULL DEFAULT '' COMMENT '奖励内容',
  `awardDesc` varchar(1024) NOT NULL DEFAULT '' COMMENT '',
  `content` varchar(1024) NOT NULL DEFAULT '' COMMENT 'mail内容',
  `reason` varchar(64) NOT NULL DEFAULT '' COMMENT 'mail reason',
  status tinyint NOT NULL DEFAULT '' COMMENT '是否已发送',
  PRIMARY KEY (`uin`,`MailId`),
  UNIQUE KEY `MailId` (`MailId`),
  KEY `startTime` (`startTime`),
  KEY `endTime` (`endTime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
'''
        yield self.dbtemplate.execDDL(query)

    @gen.coroutine
    def truncate_table(self):
        query="truncate table MailDraft"
        yield self.dbtemplate.execDDL(query)

    @gen.coroutine
    def add(self,mailId,uin,startTime,endTime,awardStr,awardDesc,content):
        query="insert into MailDraft (mailId,uin,fromUin,mailType,startTime,endTime,awardStr,awardDesc,content,reason,createTime,status) values(%d,%s,0,0,'%s','%s','%s','%s','%s','system',now(),0)"%(mailId,uin,startTime,endTime,awardStr,awardDesc,content)
        print(query)
        yield self.dbtemplate.execSql(query,db.dbtemplate.dbtemplate.Uint64Sum(uin))
    def mapRow(self,row):
        d={}
        d['mailId']    =row[0]
        d['uin']       =row[1]
        d['fromUin']   =row[2]
        d['mailType']  =row[3]
        d['startTime'] =row[4]
        d['endTime']   =row[5]
        d['awardStr']  =row[6]
        d['awardDesc'] =row[7]
        d['content']   =json.loads(row[8])
        d['reason']    =row[9]
        d['status']    =row[10]
        return d
    @gen.coroutine
    def delete(self,mailId):
        query="delete from MailDraft where mailid=%d"%(int(mailId))
        yield self.dbtemplate.execSql(query)
    @gen.coroutine
    def select_all(self):
        query="select mailId,uin,fromUin,mailType,startTime,endTime,awardStr,awardDesc,content,reason,status from MailDraft order by createTime desc"
        res=yield self.dbtemplate.query(query,self.mapRow)
        raise gen.Return(res)

    @gen.coroutine
    def select_by_mailid(self,mailId):
        query="select mailId,uin,fromUin,mailType,startTime,endTime,awardStr,awardDesc,content,reason,status from MailDraft where mailid=%d"%(int(mailId))
        res=yield self.dbtemplate.queryObject(query,self.mapRow,mailId)
        raise gen.Return(res)

    @gen.coroutine
    def updateStatusReaded(self,mailId):
        query="update MailDraft set status=1 where mailId=%d"%(int(mailId))
        yield self.dbtemplate.execSql(query)
