#  -*- coding:utf-8 -*-
__author__ = 'jixiufeng'



from datetime import datetime, timedelta
from tornado import  gen
from handler.base import *
from tornado.web import asynchronous
import conf
import redis_notify
# import json
import app
import time

class GameConfigHandler(BaseHandler):
    @asynchronous
    @gen.coroutine
    def self_get(self):

        sql="select gameConfigKey,gameConfigKeyType,gameConfigValue,gameConfigTitle ,gameConfigDesc from GameConfig order by gameConfigKey asc"
        def mapRow(row):
            data={}
            data['gameConfigKey']=row[0]
            data['gameConfigKeyType']=row[1]
            data['gameConfigValue']=row[2]
            data['gameConfigTitle']=row[3]
            data['gameConfigDesc']=row[4]
            return data
        list=yield app.DBMgr.getProfileDB().query(sql,mapRow)

        self.render("gameconfig.html", title="游戏配置控制",list=list,
                    Account=self.gmAccount,
                    channelMap=conf.getChannelNameMap())

    @asynchronous
    @gen.coroutine
    def self_post(self):
        gameConfigKey= self.get_argument('gameConfigKey','0')
        gameConfigValue= self.get_argument('gameConfigValue','0')
        gameConfigValue=gameConfigValue.replace("'","\\'")
        gameConfigValue=gameConfigValue.replace(";","")

        sql="update GameConfig set gameConfigValue='%s' where gameConfigKey=%s"%(gameConfigValue.strip(),gameConfigKey)
        print(sql)
        yield app.DBMgr.getProfileDB().execSql(sql)

        app.Redis.publish(redis_notify.get_platform_redis_notify_channel(conf.PLATFORM), redis_notify.NOTIFY_TYPE_GAMECONFIG_RELOAD)

        self.write('success')
