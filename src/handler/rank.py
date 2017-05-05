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
        serverId= self.get_argument('server','1')
        levelRankKey="cave_rank_level_%d_%s"%(conf.PLATFORM,serverId)
        levelRank=app.Redis.zrange(levelRankKey ,0,50) # list of keys

        powerRankKey="cave_rank_power_%d_%s"%(conf.PLATFORM,serverId)
        powerRank=app.Redis.zrange(powerRankKey ,0,50) # list of keys
        print(powerRank)
        self.write(json.dumps({ 'level': levelRank,'power':powerRank}))

