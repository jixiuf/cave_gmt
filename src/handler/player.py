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
        msg = self.get_argument('msg','')
        self.render("player_search.html",
                    msg=msg,
                    Account=self.gmAccount,
                    title="玩家信息查询")

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
            uin=yield self.nickName2uin(nickName)
            yield self.doSearch(uin)
        else:
            self.write("player not found")


    @gen.coroutine
    def doSearch(self,uin):
        if uin==None:
            self.write("player not found")
            return

        user=yield app.DBMgr.getUserDB().select_by_uin(uin)
        if user==None:
            self.write("player_user not found")
            return

        userAttr=yield app.DBMgr.getUserDB().select_attr_by_uin(uin)
        money=yield app.DBMgr.getMoneyDB(user.server).select_by_uin(uin)
        isBanned=yield app.DBMgr.getUserDB().isbanned(uin)
        isBannedUUID=yield app.DBMgr.getUserDB().isbannedUUID(user.uuid)

        self.render("player_info.html",
                    Account=self.gmAccount,
                    title="玩家信息" ,user=user,userAttr=userAttr,money=money,channelMap=conf.getChannelNameMap(),isBanned=isBanned,isBannedUUID=isBannedUUID)
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
        uin      = int(self.get_argument('uin','0'))
        server   = int(self.get_argument('server','0'))
        gold     = int(self.get_argument('gold','0'))
        gem      = int(self.get_argument('gem','0'))
        vipValue = int(self.get_argument('vipValue','0'))
        car      = int(self.get_argument('car','0'))
        watch    = int(self.get_argument('watch','0'))
        house    = int(self.get_argument('house','0'))
        boat     = int(self.get_argument('boat','0'))
        speaker  = int(self.get_argument('speaker','0'))
        kickCard = int(self.get_argument('kickCard','0'))
        lastPayTime = self.get_argument('lastPayTime','0')
        desc = self.get_argument('desc',"")
        nickName = self.get_argument('nickName','')
        if uin==0:
            self.write("fail")
            return

        yield app.DBMgr.getMoneyDB(int(server)).update(uin,gold,gem,speaker,vipValue,kickCard,watch,car,house,boat,lastPayTime)
        yield app.DBMgr. getUserDB().update_attr_nickname_and_desc(uin,nickName,desc)
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
        time.sleep(0.13)
        app.Redis.publish(redis_notify.get_platform_redis_notify_channel(conf.PLATFORM), redis_notify.NOTIFY_TYPE_RELOAD_BAN)
        app.Redis.publish(redis_notify.get_platform_redis_notify_channel(conf.PLATFORM), redis_notify.NOTIFY_TYPE_CLEAR_RANK_USER%uin)
        self.write("success")
        return
class PlayerUnBanHandler(BaseHandler):
    @asynchronous
    @gen.coroutine
    def self_post(self):
        uin  = self.get_argument('uin','')
        if uin==0 or uin=='':
            self.write("fail")
            return
        yield app.DBMgr.getUserDB().unbanUin(uin)
        time.sleep(0.13)
        app.Redis.publish(redis_notify.get_platform_redis_notify_channel(conf.PLATFORM), redis_notify.NOTIFY_TYPE_RELOAD_BAN)
        self.write("success")
        return
class PlayerBanUUIDHandler(BaseHandler):
    @asynchronous
    @gen.coroutine
    def self_post(self):
        uuid  = self.get_argument('uuid','')
        if uuid=='':
            self.write("fail")
            return
        yield app.DBMgr.getUserDB().banUuid(uuid)
        time.sleep(0.03)
        app.Redis.publish(redis_notify.get_platform_redis_notify_channel(conf.PLATFORM), redis_notify.NOTIFY_TYPE_RELOAD_BAN)
        self.write("success")
        return

cachedAIUinMap={}
class PlayerListHandler(BaseHandler):
    @asynchronous
    @gen.coroutine
    def self_post(self):
        self.self_get()

    @asynchronous
    @gen.coroutine
    def self_get(self):
        sortField  = self.get_argument('sort',"gold")
        page  = int(self.get_argument('page',1))
        reverse  = self.get_argument('reverse',"True")
        if reverse=="True":
            reverse=True
        else:
            reverse=False
        aiUinMap=yield self.select_all_ai_uinlist()
        moneyList=yield app.DBMgr.getMoneyDB().select_all()
        userList=yield app.DBMgr.getUserDB().select_all_channel()
        nickNameList=yield app.DBMgr.getUserDB().select_all_nickname()
        result={}
        for money in moneyList:
            rec={}
            rec['uin']=money.uin
            rec['gold']=money.gold
            rec['gem']=money.gem
            rec['speaker']=money.speaker
            rec['vipValue']=money.vipValue
            rec['kickCard']=money.kickCard
            rec['watch']=money.watch
            rec['car']=money.car
            rec['boat']=money.boat
            rec['rmb']=money.rmb
            rec['house']=money.house
            rec['lastPayTime']=money.lastPayTime
            if money.uin in aiUinMap:
                rec['isAI']=True
            else:
                rec['isAI']=False
            result[money.uin]=rec
        for userInfo in userList:
            if userInfo['uin'] in result:
                rec=result.get(userInfo['uin'])
                rec['suin']=userInfo['suin']
                rec['channel']=userInfo['channel']
                result[userInfo['uin']]=rec
        for nickNameInfo in nickNameList:
            if nickNameInfo['uin'] in result:
                rec=result.get(nickNameInfo['uin'])
                rec['nickname']=nickNameInfo['nickname']
                result[nickNameInfo['uin']]=rec
                #

        list=[]
        for info in result:
            list.append(result[info])
        def sortFunc(e1 ,e2 ):
            return e1.get(sortField,0)-e2.get(sortField,0)



        pageCnt=500
        list=sorted(list,cmp=sortFunc,reverse=reverse)
        totalPages=len(list)/pageCnt
        len(list)%pageCnt>0
        totalPages=totalPages+1
        list=list[pageCnt*(page-1):pageCnt*(page)]

        self.render("player_list.html",
                    Account=self.gmAccount,
                    title="玩家列表",result=list,sortField=sortField,page=page,totalPages=totalPages,reverse=reverse)



    @gen.coroutine
    def select_all_ai_uinlist(self):
        global cachedAIUinMap
        if len(cachedAIUinMap)!=0:
            raise gen.Return(cachedAIUinMap)
        list=yield app.DBMgr.getUserDB().select_all_ai_uinlist()
        for v in list:
            cachedAIUinMap[v]=v
        raise gen.Return(cachedAIUinMap)


