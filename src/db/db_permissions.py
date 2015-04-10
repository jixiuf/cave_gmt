#  -*- coding:utf-8 -*-
from tornado import ioloop, gen
class GmToolAccount:
    def __init__(self):
        self.account=""
        self.passwd=""
        self.level = 0
        self.levelDesc = ""
        self.urls=[]
    # def getAccount(self):
    #     return self.account
    # def getPasswd(self):
    #     return self.passwd
    # def getLevel(self):
    #     return self.level
    # def getUrls(self):
    #     return self.urls

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
    def select(self,account):
        query="select p.account,p.password,p.level,g.urls from permission as p, permission_level as g where account = '%s' and p.level = g.level"%(account,)
        def mapRow(row):
            account=GmToolAccount()
            account.account=row[0]
            account.passwd=row[1]
            account.level=row[2]
            account.urls=row[3]
            return account
        res=yield self.dbtemplate.query(None,query,mapRow)
        raise gen.Return(res)

    @gen.coroutine
    def add(self,account,password):
        query="insert ignore into permission(account,password) values('%s','%s')"%(account,password)
        result=yield self.dbtemplate.execSql(None,query)
        raise gen.Return(result)

    @gen.coroutine
    def update_level(self,account,level):
        query="update permission set level=%s where account='%s'"%(level,account)
        result=yield self.dbtemplate.execSql(None,query)
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
    def select(self,callback):
        query="select level,levelDesc,urls from permission_level order by level"
        def mapRow(row):
            account=GmToolAccount()
            account.level=row[0]
            account.levelDesc=row[1]
            account.urls=row[2]
            return account

        res=yield self.dbtemplate.query(None,query,mapRow)
        raise gen.Return(res)
    @gen.coroutine
    def add(self,level,levelDesc,urls):
        query="insert ignore into permission_level(level,levelDesc,urls) values(%d,'%s','%s')"%(level,levelDesc,urls)
        result=yield self.dbtemplate.execSql(None,query)
        raise gen.Return(result)

