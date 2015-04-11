#  -*- coding:utf-8 -*-
import os,sys
modulepath = os.getcwd()+'/..'
sys.path.append(modulepath)

from tornado_mysql import pools
from tornado import ioloop, gen

import dbtemplate.dbtemplate
import utils

from db_present_pack import PresentPackDB
from db_permissions import PermissionDB
from db_permissions import PermissionLevelDB

class DBConfigList:
    def __init__(self,dbConfigObjList):
        self.dbConfigObjList=dbConfigObjList
    def getDatabaseTemplate(self):  # sharding
        dtList=[]
        for dbConfigObj in self.dbConfigObjList:
            dtList.append(dbConfigObj.getDatabaseTemplate())
        return dbtemplate.dbtemplate.DatabaseTemplateSharding(dtList)
    def getDBConfigList(self):
        return self.dbConfigObjList

class DBConfig:
    def __init__(self,user,passwd,host,database,port):
        self.user=user
        self.passwd=passwd
        self.host=host
        self.database=database
        self.port=port
    def __str__(self):
        return "user=%s,passwd=%s,host=%s,database=%s,port=%d"%(self.user,self.passwd,self.host,self.database,self.port)
    def getUser(self):
        return self.user
    def getPasswd(self):
        return self.passwd
    def getHost(self):
        return self.host
    def getDatabase(self):
        return self.database
    def getPort(self):
        return self.port
    def conn(self):
        return pools.Pool(
            dict(host=self.getHost(),
                 port=self.getPort(),
                 user=self.getUser(),
                 passwd=self.getPasswd(),
                 db=self.getDatabase(),
                 charset='utf8',
            ),
            max_idle_connections=1,
            max_recycle_sec=3)
    def getDatabaseTemplate(self) :
        pool=self.conn()
        return dbtemplate.dbtemplate.DatabaseTemplateSingle(pool)


class DBMgr:
    def __init__(self,mode):
        self.mode=mode
    @gen.coroutine
    def load(self):
        self._designDB=self._getDesignConfig().getDatabaseTemplate()
        self._profileDB=self._getProfileConfig().getDatabaseTemplate()
        self._gamedb=self._getGameDBConfig().getDatabaseTemplate()
        self._gmtooldb=self._getGMToolConfig().getDatabaseTemplate()


        self.permissionDB=PermissionDB(self.getGMToolDB())
        yield self.permissionDB.create_table()

        self.permissionLevelDB=PermissionLevelDB(self.getGMToolDB())
        yield self.permissionLevelDB.create_table()

        yield self.permissionDB.init_data()
        yield self.permissionLevelDB.init_data()


        self.presentPackDB=PresentPackDB(self.getGMToolDB())
        yield self.presentPackDB.create_table()
        print "after load application"



    def getGameDB(self):
        return self._gamedb
    def getDesignDB(self):
        return self._designDB
    def getProfileDB(self):
        return self._profileDB
    def getProfileDB(self):
        return self._profileDB
    def getGMToolDB(self):
        return self._gmtooldb
    def _getDBConfigMaster(self,jsonData):
        user=jsonData["master"]['user']
        passwd=jsonData["master"]['passwd']
        host=jsonData["master"]['host']
        database=jsonData["master"]['database']
        port=jsonData["master"].get('port','')
        if port=="":
            port=3306
        if type(port)==str:
            port=int(port)
        return DBConfig(user,passwd,host,database,port)


    def _getDesignConfig(self):
        value=utils.getIniValueFromFile("/data/tapalliance/config/%s_1_1.ini"%(self.mode,),"design_db_config","mysql")
        value=utils.getJson(value)
        return self._getDBConfigMaster(value)


    def _getProfileConfig(self):
        value=utils.getIniValueFromFile("/data/tapalliance/config/%s_1_1.ini"%(self.mode,),"profile_db_config","mysql")
        value=utils.getJson(value)
        return self._getDBConfigMaster(value)
    def _getGMToolConfig(self):
        value=utils.getIniValueFromFile("/data/tapalliance/config/%s_1_1.ini"%(self.mode,),"gmtool_db_config","mysql")
        value=utils.getJson(value)
        return self._getDBConfigMaster(value)


    def _getGameDBConfig(self):
        value=utils.getIniValueFromFile("/data/tapalliance/config/%s_1_1.ini"%(self.mode,),"db_config","mysql")
        value=utils.getJson(value)
        masterConfigList=[]
        for masterSlaveJson in value['sharding']:
            masterConfigList.append(self._getDBConfigMaster(masterSlaveJson))
        return DBConfigList(masterConfigList)

@gen.coroutine
def test_dbmgr_main():
    mgr=DBMgr("dev")
    designConfig=mgr._getDesignConfig()
    print designConfig
    profileConfig=mgr._getProfileConfig()
    print profileConfig
    gmToolConfig=mgr._getGMToolConfig()
    print gmToolConfig

    print "db config start"
    dbConfigObjList=mgr._getGameDBConfig()
    for var in dbConfigObjList.getDBConfigList():
        print var
    print "db config end"
    mgr.load()
    testSelect=yield mgr.getProfileDB().query(None,"select 1",None)
    print "test dbmgr.query",testSelect



if __name__ == '__main__':
    test_dbmgr_main()
    ioloop.IOLoop.instance().start()

