#  -*- coding:utf-8 -*-
from tornado import  gen
from datetime import datetime, timedelta
class Player:
    def __init__(self):
        self.uin=0
        self.accountId=""
        self.accountName  = ""
        self.gender = 0
        self.server=0
        self.channel=0
        self.uuid=''
        self.osVersion=''
        self.createTime= datetime.now()
    def __str__(self):
        return "player{uin=%d,accountId=%s,accountName=%s,gender=%d,server=%d,channel=%d,uuid=%s,osVersion=%s,createtime=%s}"%(self.uin,self.accountId,self.accountName,self.gender,self.server,self.channel,self.uuid,self.osVersion,self.createTime)


class PlayerDB:
    def __init__(self,dbtemplate,mode):
        self.dbtemplate=dbtemplate
        if mode=="pro":
            self.tableShardingCount=1024
        else:
            self.tableShardingCount=2



    # @gen.coroutine
    # def create_table(self):
        # query = "create table if not exists present_pack ("\
        #         "id BIGINT(20) NOT NULL AUTO_INCREMENT, " \
        #         "`name` varchar(255) NOT NULL DEFAULT '' COMMENT 'title'," \
        #         "`Content` varchar(255) NOT NULL DEFAULT '' COMMENT 'content'," \
        #         "`icon` varchar(255) NOT NULL DEFAULT '' COMMENT 'picture Url',"\
        #         "`version` bigint(20) NOT NULL," \
        #         "`created_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP," \
        #         "`extra` varchar(255) DEFAULT '',"\
        #         "`status` varchar(16)  NOT NULL default '',"\
        #         "`hide` tinyint NOT NULL default 0,"\
        #         "primary key(id))"\
        #         "ENGINE = InnoDB CHARACTER SET = utf8"
        # yield self.dbtemplate.execDDL(query)
    def mapRow(self,row):
        d=Player()
        d.uin         =row[0 ]
        d.accountId   =row[1 ]
        d.accountName =row[2 ]
        d.gender      =row[3 ]
        d.server      =row[4 ]
        d.channel     =row[5 ]
        d.uuid        =row[6 ]
        d.osVersion   =row[7 ]
        d.createTime  =row[8 ]
        return d

    @gen.coroutine
    def select_by_uin(self,uin):
        shardingIdx=uin%self.tableShardingCount
        query="select uin,accountId,accountName,gender,serverId,channel,uuid,osVersion,createTime from player_%.4d where uin=%s"%(shardingIdx,uin)
        print query
        res=yield self.dbtemplate.queryObject(query,self.mapRow)
        raise gen.Return(res)
