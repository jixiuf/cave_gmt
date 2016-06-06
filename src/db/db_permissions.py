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
    def isAdmin(self):
        return self.level==1

    def __init__(self):
        self.account=""
        self.passwd=""
        self.level = 0
        self.levelDesc = ""
        self.urls=''

class PermissionDB:
    def __init__(self,dbtemplate):
        self.dbtemplate=dbtemplate

    @gen.coroutine
    def create_table(self):
        query = "create table if not exists permission ("\
                "id BIGINT(20) NOT NULL AUTO_INCREMENT, " \
                "`account` varchar(255) NOT NULL DEFAULT '' COMMENT 'account'," \
                "`password` varchar(255) NOT NULL DEFAULT '' COMMENT 'password'," \
                "`create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP," \
                "`update_time` timestamp NOT NULL DEFAULT '0000-00-00'," \
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
        defaultAccount=yield self.select('admin')
        if defaultAccount==None:
            yield self.add('admin',hashlib.sha1('admin').hexdigest())
            yield self.update_level('admin',1)


    def mapRow(self,row):
        account=GmToolAccount()
        account.account=row[0]
        account.passwd=row[1]
        account.level=row[2]
        account.urls=row[3]
        return account

    @gen.coroutine
    def select(self,account):
        query="select p.account,p.password,p.level,g.urls from permission as p, permission_level as g where account = '%s' and p.level = g.level"%(account,)
        res=yield self.dbtemplate.queryObject(query,self.mapRow)
        raise gen.Return(res)
    @gen.coroutine
    def select_all(self):
        query="select p.account,p.password,p.level,g.urls from permission as p, permission_level as g where p.level = g.level order by p.update_time desc"
        res=yield self.dbtemplate.query(query,self.mapRow)
        raise gen.Return(res)

    @gen.coroutine
    def add(self,account,password):
        query="insert ignore into permission(account,password,update_time) values('%s','%s',now())"%(account,password)
        result=yield self.dbtemplate.execSql(query)
        raise gen.Return(result)

    @gen.coroutine
    def update_level(self,account,level):
        query="update permission set level=%s ,update_time=now() where account='%s' "%(level,account)
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
                "`update_time` timestamp NOT NULL DEFAULT '0000-00-00'," \
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

