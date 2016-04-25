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

class PlayerSearchRenderHandler(BaseHandler):
    @asynchronous
    @gen.coroutine
    def self_get(self):
        self.render("player_search.html", title="玩家信息查询")

class PlayerSearchHandler(BaseHandler):
    @asynchronous
    @gen.coroutine
    def self_get(self):

        uin = self.get_argument('playerId','')
        suin = self.get_argument('playerSId','')
        nickName = self.get_argument('nickName','')
        if uin!='':
            yield self.doSearch(uin)
        elif suin!='':
            uin=yield self.suin2uin(suin)
            yield self.doSearch(uin)
        elif nickName!='':
            uin=yield self.nickName2uin(suin)
            yield self.doSearch(uin)
        else:
            self.write("player not found")


    @gen.coroutine
    def doSearch(self,uin):
        if uin==None:
            self.write("player not found")

        user=yield app.DBMgr.getUserDB().select_by_uin(uin)
        userAttr=yield app.DBMgr.getUserDB().select_attr_by_uin(uin)
        money=yield app.DBMgr.getMoneyDB(user.server).select_by_uin(uin)
        isBanned=yield app.DBMgr.getUserDB().isbanned(uin)

        self.render("player_info.html", title="玩家信息" ,user=user,userAttr=userAttr,money=money,channelMap=conf.getChannelNameMap(),isBanned=isBanned)
    @gen.coroutine
    def suin2uin(self,suin): #
        if suin=="":
            raise gen.Return(None)
        uinList=yield app.DBMgr.getUserDB().select_uin_list_by_suins(suin,True)
        if len(uinList)==0:
            raise gen.Return(None)
        raise gen.Return(uinList[0])
    @gen.coroutine
    def nickName2uin(self,nickName): #
        if nickName=="":
            raise gen.Return(None)
        uinList=yield app.DBMgr.getUserDB().select_uin_list_by_nickname([nickName],True)
        if len(uinList)==0:
            raise gen.Return(None)
        raise gen.Return(uinList[0])
class PlayerInfoUpdateHandler(BaseHandler):
    @asynchronous
    @gen.coroutine
    def self_post(self):
        uin      = int(self.get_argument('uin',0))
        server   = int(self.get_argument('server',0))
        gold     = int(self.get_argument('gold',0))
        gem      = int(self.get_argument('gem',0))
        vipValue = int(self.get_argument('vipValue',0))
        car      = int(self.get_argument('car',0))
        watch    = int(self.get_argument('watch',0))
        house    = int(self.get_argument('house',0))
        boat     = int(self.get_argument('boat',0))
        speaker  = int(self.get_argument('speaker',0))
        kickCard = int(self.get_argument('kickCard',0))
        if uin==0:
            self.write("fail")
            return

        yield app.DBMgr.getMoneyDB(int(server)).update(uin,gold,gem,speaker,vipValue,kickCard,watch,car,house,boat)
        time.sleep(0.03)
        app.Redis.publish(redis_notify.get_server_redis_notify_channel(conf.PLATFORM,server), redis_notify.NOTIFY_TYPE_RELOAD_MONEY%(str(uin)))
        self.write("success")

class PlayerBanHandler(BaseHandler):
    @asynchronous
    @gen.coroutine
    def self_post(self):
        uin  = int(self.get_argument('uin',0))
        if uin==0:
            self.write("fail")
            return
        yield app.DBMgr.getUserDB().banUin(uin)
        time.sleep(0.03)
        app.Redis.publish(redis_notify.get_platform_redis_notify_channel(conf.PLATFORM), redis_notify.NOTIFY_TYPE_RELOAD_BAN)
        self.write("success")
        return
class PlayerUnBanHandler(BaseHandler):
    @asynchronous
    @gen.coroutine
    def self_post(self):
        uin  = int(self.get_argument('uin',0))
        if uin==0:
            self.write("fail")
            return
        yield app.DBMgr.getUserDB().unbanUin(uin)
        time.sleep(0.03)
        app.Redis.publish(redis_notify.get_platform_redis_notify_channel(conf.PLATFORM), redis_notify.NOTIFY_TYPE_RELOAD_BAN)
        self.write("success")
        return
