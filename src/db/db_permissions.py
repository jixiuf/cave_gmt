#  -*- coding:utf-8 -*-
from tornado import  gen
import os,sys
# modulepath = os.getcwd()+'/..'
# sys.path.append(modulepath)
import hashlib

def NewGmToolAccountPermissionLevel(level,levelDesc,urls):
    a=GmToolAccount()
    a.level=level
    a.levelDesc=levelDesc
    a.urls=urls
    return a

class GmToolAccount:
    def getChannelList(self):   # string list
        return self.channel.split(",")

    def isAdmin(self):
        return self.level==1

    def __init__(self):
        self.account=""
        self.channel=''
        self.passwd=""
        self.level = 0
        self.levelDesc = ""
        self.urls=''
    def __str__(self):
        return "GMAccount{account=%s,channel=%s,passwd=%s,level=%d,levelDesc=%s,urls=%s}"%(self.account,self.channel,self.passwd,self.level,self.levelDesc,self.urls)

class PermissionDB:
    def __init__(self,dbtemplate):
        self.dbtemplate=dbtemplate

    @gen.coroutine
    def create_table(self):
        query = "create table if not exists permission ("\
                "id BIGINT(20) NOT NULL AUTO_INCREMENT, " \
                "`account` varchar(255) NOT NULL DEFAULT '' COMMENT 'account'," \
                "`channel` varchar(255) NOT NULL DEFAULT '' COMMENT 'channel'," \
                "`password` varchar(255) NOT NULL DEFAULT '' COMMENT 'password'," \
                "`create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP," \
                "`update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP," \
                "`level` smallint(6) NOT NULL DEFAULT '0' COMMENT 'level'," \
                "primary key(id),"\
                "unique key `account` (`account`))"\
                "ENGINE = InnoDB CHARACTER SET = utf8"
        yield self.dbtemplate.execDDL(query)
    @gen.coroutine
    def truncate_table(self):
        query="truncate table permission "
        yield self.dbtemplate.execDDL(query)

    @gen.coroutine
    def init_data(self):
        defaultAccount=yield self.select_all()
        if defaultAccount==None or defaultAccount==[]:
            yield self.add('admin',0,hashlib.sha1('admin').hexdigest())
            yield self.update_level('admin',1,'0')


    def mapRow(self,row):
        account=GmToolAccount()
        account.account=row[0]
        account.channel=row[1]
        account.passwd=row[2]
        account.level=row[3]
        account.urls=row[4]
        return account

    @gen.coroutine
    def select(self,account):
        query="select p.account,p.channel,p.password,p.level,g.urls from permission as p, permission_level as g where account = '%s' and p.level = g.level"%(account,)
        res=yield self.dbtemplate.queryObject(query,self.mapRow)
        raise gen.Return(res)
    @gen.coroutine
    def select_all(self):
        query="select p.account,p.channel,p.password,p.level,g.urls from permission as p, permission_level as g where p.level = g.level order by p.update_time desc"
        res=yield self.dbtemplate.query(query,self.mapRow)
        raise gen.Return(res)

    @gen.coroutine
    def add(self,account,channel,password):
        query="insert ignore into permission(account,channel,password,update_time) values('%s',%d,'%s',now())"%(account,int(channel),password)
        result=yield self.dbtemplate.execSql(query)
        raise gen.Return(result)

    @gen.coroutine
    def update_level(self,account,level,channel):
        query="update permission set level=%s ,channel='%s',update_time=now() where account='%s' "%(level,channel,account)
        result=yield self.dbtemplate.execSql(query)
        raise gen.Return(result)
    @gen.coroutine
    def delete(self,account):
        query="delete from permission  where account='%s' "%(account)
        result=yield self.dbtemplate.execSql(query)
        raise gen.Return(result)


class PermissionLevelDB:
    def __init__(self,dbtemplate):
        self.dbtemplate=dbtemplate

    @gen.coroutine
    def create_table(self):
        query = "create table if not exists permission_level ("\
                "`level` smallint(6) NOT NULL DEFAULT '0' COMMENT 'level'," \
                "`levelDesc` varchar(255) NOT NULL DEFAULT '' COMMENT 'levelDesc'," \
                "`create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP," \
                "`update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP," \
                "`urls` varchar(1024) NOT NULL DEFAULT '' COMMENT 'urls'," \
                "primary key(level))"\
                "ENGINE = InnoDB CHARACTER SET = utf8"
        yield self.dbtemplate.execDDL(query)

    @gen.coroutine
    def truncate_table(self):
        query="truncate table permission_level"
        yield self.dbtemplate.execDDL(query)

    @gen.coroutine
    def init_data(self,accountList):
        levelRows=yield self.select()
        if len(levelRows)==0:
            for account in accountList:
                yield self.add(account.level,account.levelDesc,account.urls)

    def mapRow(self,row):
        account=GmToolAccount()
        account.level=row[0]
        account.levelDesc=row[1]
        account.urls=row[2]
        return account
    @gen.coroutine
    def select(self):
        query="select level,levelDesc,urls from permission_level order by level"
        res=yield self.dbtemplate.query(query,self.mapRow)
        raise gen.Return(res)
    @gen.coroutine
    def add(self,level,levelDesc,urls):
        query="insert ignore into permission_level(level,levelDesc,urls) values(%d,'%s','%s')"%(level,levelDesc,urls)
        result=yield self.dbtemplate.execSql(query)
        raise gen.Return(result)

