#  -*- coding:utf-8 -*-
import os,sys,re,json
modulepath = os.getcwd()+'/..'
sys.path.append(modulepath)

from tornado_mysql import pools
from tornado import ioloop, gen

import dbtemplate.dbtemplate
import utils

from db_maintain import MaintainDB
from db_present_pack import PresentPackDB
from db_permissions import PermissionDB
from db_permissions import PermissionLevelDB
from db_design_leader import DesignBLeaderDB
from db_design_hero import DesignBHeroDB
from db_player import PlayerDB
from db_gamedb_user_attr import UserAttrDB

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
    def __init__(self,mode,locale):
        self.mode=mode
        self.locale=locale
    # def get_all_server_id(self):
    #     list=[]
    #     reC=re.compile(r'.*%s_0_([0-9]+)\.json'%(self.mode))
    #     for f in os.listdir('/data/castle/config/'):
    #         matched=reC.match( f)
    #         if matched:
    #             list.append(int(matched.group(1)))
    #     return list



    @gen.coroutine
    def load(self):
        self._designDBDict={}
        self._gamedbDict={}
        # for i in self.get_all_server_id(): #
        #     designConfig=self._getDesignConfig(i)
        #     if designConfig!=None:
        #         self._designDBDict[i]=designConfig.getDatabaseTemplate()
        #     gameDBConfig=self._getGameDBConfig(i)
        #     if gameDBConfig!=None:
        #         self._gamedbDict[i]=gameDBConfig.getDatabaseTemplate()

        self._profileDB=self._getProfileConfig().getDatabaseTemplate()
        self._gmtooldb=self._getGMToolConfig().getDatabaseTemplate()


        self.permissionDB=PermissionDB(self.getGMToolDB())
        yield self.permissionDB.create_table()

        self.permissionLevelDB=PermissionLevelDB(self.getGMToolDB())
        yield self.permissionLevelDB.create_table()

        yield self.permissionDB.init_data()
        yield self.permissionLevelDB.init_data()



        self.presentPackDB=PresentPackDB(self.getGMToolDB())
        yield self.presentPackDB.create_table()

        self.maintainDB=MaintainDB(self.getProfileDB())
        yield self.maintainDB.create_table()

        print "after load application"


    def getUserAttrDB(self,server=1):
        return UserAttrDB(self.getGameDB(server))
    def getPlayerDB(self):
        return PlayerDB(self.getProfileDB(),self.mode)

    def getDesignHeroDB(self,server=1):
        return DesignBLeaderDB(self.getDesignDB(server),self.locale)

    def getDesignLeaderDB(self,server=1):
        return DesignBHeroDB(self.getDesignDB(server),self.locale)

    def getGameDB(self,server):
        return self._gamedbDict[server]
    def getDesignDB(self,server):
        return self._designDBDict[server]
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
        if type(port)==str or type(port)==unicode :
            port=int(port)
        return DBConfig(user,passwd,host,database,port)


    def _getDesignConfig(self,server):
        with open("/data/castle/config/%s.json"%(self.mode)) as data_file:
            value = json.load(data_file)
            if value==None:
                return None
            return self._getDBConfigMaster(value["design_db_config"])


    def _getProfileConfig(self):
        with open("/data/castle/config/%s.json"%(self.mode)) as data_file:
            value = json.load(data_file)
            if value==None:
                return None
            return self._getDBConfigMaster(value["profile_db_config"])
    def _getGMToolConfig(self):
        with open("/data/castle/config/%s.json"%(self.mode)) as data_file:
            value = json.load(data_file)
            if value==None:
                return None
            return self._getDBConfigMaster(value["gmtool_db_config"])

    def _getGameDBConfig(self,server):
        with open("/data/castle/config/%s.json"%(self.mode)) as data_file:
            value = json.load(data_file)
            if value==None:
                return None
            masterConfigList=[]
            for masterSlaveJson in value["game_db_config"]['sharding']:
                masterConfigList.append(self._getDBConfigMaster(masterSlaveJson))
            return DBConfigList(masterConfigList)

@gen.coroutine
def test_dbmgr_main():
    mgr=DBMgr("dev")
    designConfig=mgr._getDesignConfig(1)
    print designConfig
    profileConfig=mgr._getProfileConfig()
    print profileConfig
    gmToolConfig=mgr._getGMToolConfig()
    print gmToolConfig

    print "db config start"
    dbConfigObjList=mgr._getGameDBConfig(1)
    for var in dbConfigObjList.getDBConfigList():
        print var
    print "db config end"
    mgr.load()
    testSelect=yield mgr.getProfileDB().query(None,"select 1",None)
    print "test dbmgr.query",testSelect



if __name__ == '__main__':
    test_dbmgr_main()
    ioloop.IOLoop.instance().start()
