#  -*- coding:utf-8 -*-
from tornado import  gen
from datetime import datetime, timedelta
class UserAttr:
    def __init__(self):
        self.uin=0
        self.nickName=0
        self.gender=""
        self.avatar= ""
        self.desc= 0
        # self.lastPayTime= datetime.now()

class User:
    def __init__(self):
        self.uin=0
        self.autoIncrementId=0
        self.accountId=""
        self.password  = ""
        self.accountType = 0
        self.server=0
        self.channel=0
        self.uuid=''
        self.osVersion=''
        self.createTime= datetime.now()
    def __str__(self):
        return "player{uin=%d,accountId=%s,password=%s,accountType=%d,server=%d,channel=%d,uuid=%s,osVersion=%s,createtime=%s}"%(self.uin,self.accountId,self.password,self.accountType,self.server,self.channel,self.uuid,self.osVersion,self.createTime)


class UserDB:
    def __init__(self,dbtemplate):
        self.dbtemplate=dbtemplate


    def mapRowAttr(self,row):
        d=UserAttr()
        d.uin           =row[ 0 ]
        d.nickName      =row[ 1 ]
        d.gender        =row[ 2 ]
        d.avatar        =row[ 3 ]
        d.desc          =row[ 4 ]
        d.lastLoginTime =row[ 5 ]
        return d



    def mapRow(self,row):
        d=User()
        d.uin         =row[ 0 ]
        d.suin        =row[ 1 ]
        d.accountId   =row[ 2 ]
        d.password    =row[ 3 ]
        d.accountType =row[ 4 ]
        d.platform    =row[ 5 ]
        d.server      =row[ 6 ]
        d.channel     =row[ 7 ]
        d.uuid        =row[ 8 ]
        d.ip          =row[ 9 ]
        d.os          =row[10 ]
        d.osVersion   =row[11 ]
        d.deviceModel =row[12 ]
        d.createTime  =row[13 ]
        return d

    @gen.coroutine
    def create_table(self):
        query = '''
CREATE TABLE if not exists `user` (
  `Uin` bigint(20) NOT NULL COMMENT '唯一ID',
  `autoIncrementId` bigint(20) NOT NULL AUTO_INCREMENT,
  `AccountId` varchar(64) NOT NULL DEFAULT '' COMMENT '设备ID',
  `Password` varchar(64) NOT NULL DEFAULT '' COMMENT '设备ID',
  `accountType` tinyint(4) NOT NULL DEFAULT '0' COMMENT '性别',
  `platform` smallint(6) NOT NULL DEFAULT '0' COMMENT '平台',
  `server` smallint(6) NOT NULL DEFAULT '0' COMMENT 'serverid',
  `channel` int(11) NOT NULL DEFAULT '0' COMMENT '渠道',
  `uuid` varchar(64) NOT NULL DEFAULT '' COMMENT '设备ID',
  `ip` int(10) unsigned NOT NULL DEFAULT '0' COMMENT 'ip',
  `os` tinyint(4) NOT NULL DEFAULT '0' COMMENT '系统',
  `osVersion` varchar(32) NOT NULL DEFAULT '' COMMENT '系统',
  `deviceModel` varchar(64) NOT NULL DEFAULT '' COMMENT '设备型号  iPhone 4S、iPhone 5S',
  `createTime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '注册时间时间',
  PRIMARY KEY (`Uin`),
  KEY `account_idx` (`AccountId`),
  KEY `uuid` (`uuid`),
  KEY `autoIncrementId_ix` (`autoIncrementId`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8;
'''
        yield self.dbtemplate.execDDL(query)

    @gen.coroutine
    def truncate_table(self):
        query="truncate table user "
        yield self.dbtemplate.execDDL(query)

    @gen.coroutine
    def add(self,uin):
        query="insert into user (uin) values(%d)"%(uin)
        yield self.dbtemplate.execSql(query)

    @gen.coroutine
    def select_all_channel(self):
        query="select uin,autoIncrementId,channel from user "
        def mapRow(row):
            result={}
            result['uin']=row[0]
            result['suin']=row[1]
            result['channel']=row[2]
            return result
        res=yield self.dbtemplate.query(query,mapRow)
        raise gen.Return(res)

    @gen.coroutine
    def select_by_uin(self,uin):
        query="select uin,autoIncrementId,accountId,password,accountType,platform,server,channel,uuid,ip,os,osVersion,deviceModel,createTime from user where uin=%s"%(uin)
        print(query)
        res=yield self.dbtemplate.queryObject(query,self.mapRow)
        raise gen.Return(res)
    @gen.coroutine
    def select_all_nickname(self):
        query="select uin,nickName from UserAttr"
        def mapRow(row):
            result={}
            result['uin']=row[0]
            result['nickname']=row[1]
            return result

        res=yield self.dbtemplate.query(query,mapRow)
        raise gen.Return(res)

    @gen.coroutine
    def select_attr_by_uin(self,uin):
        query="select uin,nickName,gender,avatar,description,lastLoginTime from UserAttr where uin=%s"%(uin)
        res=yield self.dbtemplate.queryObject(query,self.mapRowAttr)
        raise gen.Return(res)
    @gen.coroutine
    def update_attr_nickname_and_desc(self,uin,nickName,desc):
        query="update UserAttr set description='%s',nickName='%s' where uin=%s"%(desc,nickName,uin)
        res=yield self.dbtemplate.execSql(query)
        raise gen.Return(res)


    @gen.coroutine
    def select_uin_by_suin(self,suin):
        query="select uin from user where autoIncrementId=%s"%(suin)
        def mapRowUin(row):
            return row[0]
        res=yield self.dbtemplate.queryObject(query,mapRowUin)
        raise gen.Return(res)

    @gen.coroutine
    def select_uin_list_by_suins(self,suins,asStr): # suins="1,2,3", return []
        if suins.strip()=="":
            raise gen.Return([])
        if asStr==None or asStr ==False:
            mapRow=self.mapRowUinAsInt
        else:
            mapRow=self.mapRowUinAsStr

        query="select uin from user where autoIncrementId in(%s)"%(suins)
        res=yield self.dbtemplate.query(query,mapRow)
        raise gen.Return(res)

    def mapRowUinAsInt(self,row):
        return row[0]
    def mapRowUinAsStr(self,row):
        return str(row[0])


    # select
    @gen.coroutine
    def select_all_ai_uinlist(self):
        query="select uin from AI"
        res=yield self.dbtemplate.query(query,self.mapRowUinAsInt)
        raise gen.Return(res)


    # select
    @gen.coroutine
    def select_uin_list_by_nickname(self,nicknameList,asStr):
        if len(nicknameList)==0:
            raise gen.Return([])

        if asStr==None or asStr ==False:
            mapRow=self.mapRowUinAsInt
        else:
            mapRow=self.mapRowUinAsStr

        newList=[]
        for nickName in nicknameList:
            newList.append( '\''+nickName+'\'')

        query="select uin from UserAttr where nickName in(%s)"%(",".join(newList))
        res=yield self.dbtemplate.query(query,mapRow)
        raise gen.Return(res)

    @gen.coroutine
    def banUin(self,uin):
        now=datetime.now()+timedelta(days=-1)
        end= datetime.now()+ timedelta(days=365)
        query="insert into ban(Type,content,reason,startBanTime,endBanTime) values(2,'%s','gmt','%s','%s')"%(str(uin),now,end)
        yield self.dbtemplate.execSql(query)

    @gen.coroutine
    def unbanUin(self,uin):
        query="delete from ban where content='%s'"%(str(uin))
        yield self.dbtemplate.execSql(query)
    @gen.coroutine
    def banUuid(self,uuid):
        now=datetime.now()+timedelta(days=-1)
        end= datetime.now()+ timedelta(days=365)
        query="insert into ban(Type,content,reason,startBanTime,endBanTime) values(4,'%s','gmt','%s','%s')"%(uuid,now,end)
        yield self.dbtemplate.execSql(query)

    @gen.coroutine
    def updateAccountId(self,uin,accountId):
        query="update user set sessionInfo='' ,uuid='' ,accountId='%s' where uin=%s"%(str(accountId),str(uin))
        print(query)
        yield self.dbtemplate.execSql(query)
    @gen.coroutine
    def isbanned(self,uin):
        query="select content from ban where content='%s' and Type=2 and now()<endBanTime and now()>startBanTime"%(str(uin))
        def mapRowIsBanned(row):
            return row[0]
        res=yield self.dbtemplate.query(query,mapRowIsBanned)
        if res==None or len(res)==0:
            raise gen.Return(False)
        raise gen.Return(True)

    def isbannedUUID(self,uin):
        query="select content from ban where content='%s' and Type=4 and now()<endBanTime and now()>startBanTime"%(str(uin))
        def mapRowIsBanned(row):
            return row[0]
        res=yield self.dbtemplate.query(query,mapRowIsBanned)
        if res==None or len(res)==0:
            raise gen.Return(False)
        raise gen.Return(True)




