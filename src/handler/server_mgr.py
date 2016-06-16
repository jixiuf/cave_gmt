#  -*- coding:utf-8 -*-
__author__ = 'jixiufeng'


from datetime import datetime, timedelta
import utils
import redis_notify
from handler.base import BaseHandler
from tornado.web import asynchronous
from tornado import  gen
import app
import conf
import time

class ServerMgr(BaseHandler):
    @asynchronous
    @gen.coroutine
    def self_get(self):
        serverIdList= app.DBMgr.get_all_server_id()
        maintainList=yield app.DBMgr.maintainDB.select_all()
        supervisorAddrJson=conf.getAllSupervisorAddrList()
        etcdServerListMap={}
        for serverId in serverIdList:
            etcdServerListMap[str(serverId)]=app.getEtcdServerList(conf.PLATFORM,serverId)
        self.render("server_mgr.html",title="服务器管理",serverIdList=serverIdList,supervisorAddrJson=supervisorAddrJson,etcdServerListMap=etcdServerListMap)

class ServerStopping(BaseHandler):
    @asynchronous
    @gen.coroutine
    def self_post(self):
        serverIdStr=self.get_argument('serverId')
        processIdStr=self.get_argument('processId')
        if processIdStr=='' or processIdStr=="0":
            app.Redis.publish(redis_notify.get_server_redis_notify_channel(conf.PLATFORM,serverIdStr), redis_notify.NOTIFY_TYPE_SERVER_STOPPING)
        else:
            app.Redis.publish(redis_notify.get_process_redis_notify_channel(conf.PLATFORM,serverIdStr,processIdStr), redis_notify.NOTIFY_TYPE_SERVER_STOPPING)
        time.sleep(0.1)
        self.write('success')

        # maintainList=yield app.DBMgr.maintainDB.select_all()
        # self.render("maintain.html",title="维护公告",maintainList=maintainList)
class KickUser(BaseHandler):
    @asynchronous
    @gen.coroutine
    def self_post(self):
        serverIdStr=self.get_argument('serverId','0')
        if serverIdStr=='':
            serverIdStr='0'
        processIdStr=self.get_argument('processId','0')
        if processIdStr=='':
            processIdStr="0"
        uin=self.get_argument('uin','0') # 0表示踢所有人
        if  serverIdStr=="0":
            redisChan=redis_notify.get_platform_redis_notify_channel(conf.PLATFORM)
        elif processIdStr=="0":
            redisChan=redis_notify.get_server_redis_notify_channel(conf.PLATFORM,serverIdStr)
        elif int(processIdStr)!=0:
            redisChan=redis_notify.get_process_redis_notify_channel(conf.PLATFORM,serverIdStr,processIdStr)
        else:
            redisChan=redis_notify.get_platform_redis_notify_channel(conf.PLATFORM)

        app.Redis.publish(redisChan, redis_notify.NOTIFY_TYPE_KICK_USER%uin)
        time.sleep(0.1)
        self.write('success')

