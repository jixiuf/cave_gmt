#  -*- coding:utf-8 -*-
import os,sys,re,json
import os.path
modulepath = os.getcwd()+'/..'
sys.path.append(modulepath)

from tornado_mysql import pools
from tornado import ioloop, gen

import dbtemplate.dbtemplate
import utils
import conf

from db_maintain import MaintainDB
from db_notice import NoticeDB
from db_present_pack import PresentPackDB
from db_permissions import PermissionDB
from db_permissions import PermissionLevelDB
# from db_design_leader import DesignBLeaderDB
# from db_design_hero import DesignBHeroDB
from db_user import UserDB
from db_pay import PayOrderDB
from db_bi_user import  BIUserDB
from db_bi import *

from db_mail import MailDB
from db_mail_draft import MailDraftDB
from db_version_update import VersionUpdateDB
from db_server_version import ServerVersionDB
from db_dynamic_version_update import DynamicVersionUpdateDB
from db_award_type import AwardDB

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
    def init(self,mode,locale):
        self.mode=mode
        self.locale=locale

    def get_all_server_id(self):
        list=[]
        with open(conf.getConfigFile()) as data_file:
            value = json.load(data_file)
            if value==None:
                return
            for k in value["game_db_config"]:
                list.append(int(k))


        # reC=re.compile(r'.*%s_0_([0-9]+)\.json'%(self.mode))
        # for f in os.listdir('/data/%s/config/'):
        #     matched=reC.match( f)
        #     if matched:
        #         list.append(int(matched.group(1)))
        return list



    @gen.coroutine
    def load(self):
        self._designDBDict={}
        self._gamedbDict={}

        designConfig=self._getDesignConfig()
        if designConfig!=None:
            self._designDBDict[1]=designConfig.getDatabaseTemplate()

        for i in self.get_all_server_id(): #
            gameDBConfig=self._getGameDBConfig(i)
            if gameDBConfig!=None:
                self._gamedbDict[i]=gameDBConfig.getDatabaseTemplate()

        self._profileDB=self._getProfileConfig().getDatabaseTemplate()
        self._gmtooldb=self._getGMToolConfig().getDatabaseTemplate()


        self.permissionDB=PermissionDB(self.getGMToolDB())
        yield self.permissionDB.create_table()

        self.permissionLevelDB=PermissionLevelDB(self.getGMToolDB())
        yield self.permissionLevelDB.create_table()

        yield self.permissionDB.init_data()
        yield self.permissionLevelDB.init_data(conf.initPermissionLevel)



        self.presentPackDB=PresentPackDB(self.getGMToolDB())
        yield self.presentPackDB.create_table()

        self.maintainDB=MaintainDB(self.getProfileDB())
        yield self.maintainDB.create_table()

        self.noticeDB=NoticeDB(self.getProfileDB())
        # yield self.noticeDB.create_table()


        self.dynamicVersionUpdateDB=DynamicVersionUpdateDB(self.getProfileDB())
        yield self.dynamicVersionUpdateDB.create_table()

        self.versionUpdateDB=VersionUpdateDB(self.getProfileDB())
        yield self.versionUpdateDB.create_table()

        self.serverVersionDB=ServerVersionDB(self.getProfileDB())
        yield self.serverVersionDB.create_table()

        self.mailDraftDB=MailDraftDB(self.getGMToolDB())
        yield self.mailDraftDB.create_table()

        self.mailDraftDB=MailDraftDB(self.getGMToolDB())
        yield self.mailDraftDB.create_table()
        self.biUserDB=BIUserDB(self.getGMToolDB())
        yield self.biUserDB.create_table()


        print "after load application"


    def getUserDB(self):
        return UserDB(self.getProfileDB())
    def getPayOrderDB(self):
        return PayOrderDB(self.getProfileDB())
    def getCurrencyChangeDB(self):
        return CurrencyChangeDB(self.getGMToolDB())
    def getItemChangeDB(self):
        return ItemChangeDB(self.getGMToolDB())
    def getGearGotDB(self):
        return GearGotDB(self.getGMToolDB())
    def getGearFortifyDB(self):
        return GearFortifyDB(self.getGMToolDB())
    def getGearRefineDB(self):
        return GearRefineDB(self.getGMToolDB())
    def getLevelUpDB(self):
        return LevelUpDB(self.getGMToolDB())
    def getPartnerDB(self):
        return PartnerDB(self.getGMToolDB())







    def getMailDB(self,server=1):
        return MailDB(self.getGameDB(server))
    def getMailDraftDB(self):
        return self.mailDraftDB



    # def getDesignHeroDB(self,server=1):
    #     return DesignBLeaderDB(self.getDesignDB(server),self.locale)

    def getAwardDB(self,server=1):
        return AwardDB(self.getDesignDB(server),self.locale)

    def getGameDB(self,server):
        return self._gamedbDict[server]
    def getDesignDB(self,server=1):
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




    def _getDesignConfig(self):
        with open(conf.getConfigFile()) as data_file:
            value = json.load(data_file)
            if value==None:
                return None
            return self._getDBConfigMaster(value["design_db_config"])


    def _getProfileConfig(self):
        with open(conf.getConfigFile()) as data_file:
            value = json.load(data_file)
            if value==None:
                return None
            return self._getDBConfigMaster(value["profile_db_config"])
    def _getGMToolConfig(self):
        with open(conf.getConfigFile()) as data_file:
            value = json.load(data_file)
            if value==None:
                return None
            return self._getDBConfigMaster(value["gmtool_db_config"])

    def _getGameDBConfig(self,server):
        with open(conf.getConfigFile()) as data_file:
            value = json.load(data_file)
            if value==None:
                return None
            masterConfigList=[]
            for masterSlaveJson in value["game_db_config"][str(server)]['sharding']:
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
