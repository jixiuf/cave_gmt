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
import json

class Broadcast(BaseHandler):
    @asynchronous
    @gen.coroutine
    def self_get(self):
        serverIdList= app.DBMgr.get_all_server_id()
        sql="select server,id,content,startTime,endTime,`interval` from Marquee order by server asc,id desc"
        def mapRow(row):
            data={}
            data['server']=row[0]
            data['id']=row[1]
            data['content']=row[2]
            data['startTime']=row[3]
            data['endTime']=row[4]
            data['interval']=row[5]

            if data['content']!="":
                data['content']=json.loads(data['content'])['content']

            return data
        print(sql)
        marqueeList=yield app.DBMgr.getProfileDB().query(sql,mapRow)
        print(marqueeList)

        self.render("broadcast.html",title="紧急广播/跑马灯",
                    marqueeList=marqueeList,
                    Account=self.gmAccount,
                    serverIdList=serverIdList)
    @asynchronous
    @gen.coroutine
    def self_post(self):
        typ=self.get_argument('type')
        serverIdStr=self.get_argument('serverId')
        content=self.get_argument('content')
        content=content.replace("'","")
        content=content.replace("\"","")
        print(content)

        startTime=self.get_argument('startTime',datetime.now())
        endTime=self.get_argument('endTime',datetime.now())
        interval=self.get_argument('interval',10)
        if typ=="now":
            # {144150688393216252 2 24 {"head_icon":1,"nickname":"游客00252","content_type":"normal","sex":1}}
            chatInfo={'chat_type':3,'content':'%s'%content,'params':'{}'} # chat_type_broadcast
            # chatInfo={'chat_type':3,'content':'%s'%content,'params':'{"head_icon":0,"nickname":"系统广播","content_type":"normal","sex":1}'} # chat_type_broadcast
            app.Redis.publish(redis_notify.get_server_redis_notify_channel(conf.PLATFORM,serverIdStr), redis_notify.NOTIFY_TYPE_BROADCAST%(json.dumps(chatInfo)))
        else:
            chatInfo={"chat_type":3,"content":"%s"%content,"params":"{}"} # chat_type_broadcast
            print(chatInfo)
            sql="insert into Marquee( server,id,content,startTime,endTime,`interval`,nextTime) value(%s,%s,'%s','%s','%s',%s,'%s') "% (
                serverIdStr,utils.timestamp_now(),json.dumps(chatInfo,ensure_ascii=False,cls=utils.DateEncoder ),startTime,endTime,interval,startTime)
            print(sql)
            yield app.DBMgr.getProfileDB().execSql(sql)
            app.Redis.publish(redis_notify.get_server_redis_notify_channel(conf.PLATFORM,serverIdStr), redis_notify.NOTIFY_TYPE_MARQUEE)


        self.write('success')


class MarqueeDelete(BaseHandler):
    @asynchronous
    @gen.coroutine
    def self_post(self):
        id= self.get_argument('id','0')
        serverIdStr=self.get_argument('serverId')
        sql="delete from Marquee where id=%s"%(id)
        print(sql)
        yield app.DBMgr.getProfileDB().execSql(sql)
        app.Redis.publish(redis_notify.get_server_redis_notify_channel(conf.PLATFORM,serverIdStr), redis_notify.NOTIFY_TYPE_MARQUEE)
        self.write('success')

