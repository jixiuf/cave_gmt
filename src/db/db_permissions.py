#  -*- coding:utf-8 -*-
from tornado import ioloop, gen
class GmToolAccount:
    def __init__(self):
        self.account=""
        self.passwd=""
        self.level = 0
        self.urls=[]

    def getAccount(self):
        return self.account
    def getPasswd(self):
        return self.passwd
    def getLevel(self):
        return self.level
    def getUrls(self):
        return self.urls

class PermissionsDB:
    def __init__(self,dbtemplate):
        self.dbtemplate=dbtemplate

    @gen.coroutine
    def create_table(self):
        query = "create table if not exists permissions ("\
                "id BIGINT(20) NOT NULL AUTO_INCREMENT, " \
                "`account` varchar(255) NOT NULL DEFAULT '' COMMENT 'account'," \
                "`password` varchar(255) NOT NULL DEFAULT '' COMMENT 'password'," \
                "`create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP," \
                "`dupdate_time` timestamp NOT NULL DEFAULT '0000-00-00'," \
                "`level` smallint(6) NOT NULL DEFAULT '0' COMMENT 'level'," \
                "primary key(id),"\
                "unique key `account` (`account`))"\
                "ENGINE = InnoDB CHARACTER SET = utf8"
        yield self.dbtemplate.execDDL(query)
    @gen.coroutine
    def truncate_table(self):
        query="truncate table permissions "
        yield self.dbtemplate.execDDL(query)

    @gen.coroutine
    def select(self,account):
        query="select p.account,p.password,p.level,g.urls from permissions as p, gmtool_level as g where account = '%s' and p.level = g.level"%(account,)
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
        query="insert ignore into permissions(account,password) values('%s','%s')"%(account,password)
        result=yield self.dbtemplate.execSql(None,query)
        raise gen.Return(result)

    @gen.coroutine
    def update_level(self,account,level):
        query="update permissions set level=%s where account='%s'"%(level,account)
        result=yield self.dbtemplate.execSql(None,query)
        raise gen.Return(result)
