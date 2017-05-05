#  -*- coding:utf-8 -*-
__author__ = 'jixiufeng'


from datetime import datetime, timedelta
import utils
import redis_notify
from handler.base import BaseHandler
from tornado.web import asynchronous
from tornado import  gen
import app
import json
import conf
import time

class Rank(BaseHandler):
    @asynchronous
    @gen.coroutine
    def self_get(self):
        serverIdList= app.DBMgr.get_all_server_id()
        self.render("rank.html",
                    Account=self.gmAccount,
                    title="查看排行榜玩家",
                    serverIdList=serverIdList)

    @asynchronous
    @gen.coroutine
    def self_post(self):
        def getvalue(score):
            return conf.REDIS_MAX_SCORE-int(score)
        serverId= self.get_argument('server','1')
        levelRankKey="cave_rank_level_%d_%s"%(conf.PLATFORM,serverId)
        levelRank=app.Redis.zrange(levelRankKey ,0,200,withscores=True,score_cast_func=getvalue) # list of [key,value]
        levelKeys=[]
        levelValues=[]
        for var in levelRank:
            levelKeys.append(str(var[0]))
            levelValues.append(int(var[1])/1000000) # =level*1000000+exp

        powerRankKey="cave_rank_power_%d_%s"%(conf.PLATFORM,serverId)
        powerRank=app.Redis.zrange(powerRankKey ,0,200,withscores=True,score_cast_func=getvalue) # list of [key,value]
        powerKeys=[]
        powerValues=[]
        for var in powerRank:
            powerKeys.append(str(var[0]))
            powerValues.append(int(var[1]))
        self.write(json.dumps({ 'levelKeys': levelKeys,"levelValues":levelValues,'powerKeys':powerKeys,"powerValues":powerValues}))

