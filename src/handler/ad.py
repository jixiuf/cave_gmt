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


class AdHandler(BaseHandler):
    @asynchronous
    @gen.coroutine
    def self_get(self):
        content=app.Redis.get("zjh_ad")
        if content!=None:
            data=json.loads(content)
        else:
            data={}
        print("sss",content)
        self.render("adinfo.html", title="修改广告内容",data=data)

    @asynchronous
    @gen.coroutine
    def self_post(self):
        uin = self.get_argument('uin','0')
        content = self.get_argument('content','')

        if len(uin)<=16:
            uin=yield self.suin2uin(uin)

        if uin=='0' or uin==None:
            self.write("玩家不存在")
            return




        redisContent={}
        redisContent['uin']=int(uin)
        redisContent['content']=content

        app.Redis.set("zjh_ad", json.dumps(redisContent))
        self.write("success")


    @gen.coroutine
    def suin2uin(self,uin): #
        if uin=="":
            raise gen.Return(None)
        uinList=yield app.DBMgr.getUserDB().select_uin_list_by_suins(uin,True)
        if len(uinList)==0:
            raise gen.Return(None)
        raise gen.Return(uinList[0])
