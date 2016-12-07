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


class DeskInfoHandler(BaseHandler):
    @asynchronous
    @gen.coroutine
    def self_get(self):
        self.render("deskinfo.html",
                    Account=self.gmAccount,

                    title="玩家所在牌桌信息查询")

    @asynchronous
    @gen.coroutine
    def self_post(self):

        suin = self.get_argument('suin','')
        sleepSeconds = self.get_argument('sleepSeconds','')
        if len(suin)>16:
            self.doSearch(suin,int(sleepSeconds))
            raise gen.Return("")

        if suin!='':
            uin=yield self.suin2uin(suin)
            if uin==None:
                self.write(json.dumps({'result':'player not found'}))
                raise gen.Return("")

            yield self.doSearch(uin,int(sleepSeconds))
        else:
            self.write(json.dumps({'result':'player not found'}))
            raise gen.Return("")


    @gen.coroutine
    def doSearch(self,uin,sleepSeconds):
        app.Redis.publish(redis_notify.get_platform_redis_notify_channel(conf.PLATFORM), redis_notify.NOTIFY_TYPE_DESKINFO%(uin))
        if sleepSeconds>0:
            time.sleep(sleepSeconds)

        kv=app.Redis.hgetall("zjh_desk")
        result=[]
        for k in kv:
            result.append(json.loads(kv[k]))
            app.Redis.hdel("zjh_desk",k)

        self.write(json.dumps({'result':'',"data":result}))

    @gen.coroutine
    def suin2uin(self,suin): #
        if suin=="":
            raise gen.Return(None)
        uinList=yield app.DBMgr.getUserDB().select_uin_list_by_suins(suin,True)
        if len(uinList)==0:
            raise gen.Return(None)
        raise gen.Return(uinList[0])
