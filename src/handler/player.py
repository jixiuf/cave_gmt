#  -*- coding:utf-8 -*-
__author__ = 'jixiufeng'



from datetime import datetime, timedelta
from tornado import  gen
from handler.base import *
from tornado.web import asynchronous
import conf
# import json
# import app

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
        self.render("player_info.html", title="玩家信息" ,user=user,userAttr=userAttr,money=money,channelMap=conf.getChannelNameMap())
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
