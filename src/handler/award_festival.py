#  -*- coding:utf-8 -*-
# coding=utf-8
__author__ = 'jixiufeng'


from handler.base import BaseHandler
import utils
from tornado.web import asynchronous
from tornado import  gen
import app
import json
import conf
import time
import redis_notify
from datetime import datetime, timedelta



class FestivalConfig(BaseHandler):
    @asynchronous
    @gen.coroutine
    def self_get(self):
        def mapRow(row):
            data={}
            data['day']=row[0]
            data['name']=row[1]
            data['content']=row[2]
            data['desc']=row[3]
            data['note']=row[4]
            return data
        sql="select `day`,`name`,`content`,`desc` ,`note` from FestivalConfig order by day asc "
        festivalconfigList=yield app.DBMgr.getProfileDB().query(sql,mapRow)
        serverIdList=app.DBMgr.get_all_server_id()
        self.render("award_festival.html",title="节日礼包活动",
                    festivalconfigList=festivalconfigList,
                    Account=self.gmAccount,
                    serverIdList=serverIdList)
    @asynchronous
    @gen.coroutine
    def self_post(self):
        # serverId= self.get_argument('serverid','1')
        day= self.get_argument('day','')
        if day=='':
            return
        t=time.strptime(day,"%Y-%m-%d")
        startTime=datetime(*t[:3])
        yearday=utils.datetime2yearday(startTime)

        opType= self.get_argument('type','send')
        if opType=='delete':
            sql="delete from FestivalConfig where day=%d"%(yearday)
            print(sql)
            yield app.DBMgr.getProfileDB().execSql(sql)

            app.Redis.publish(redis_notify.get_platform_redis_notify_channel(conf.PLATFORM), redis_notify.NOTIFY_TYPE_RELOAD_FESTIVALCONFIG)
            self.write(json.dumps({},cls=utils.DateEncoder))
            return



        # award= self.get_argument('awards')
        awardList= self.get_argument('award_list' ,'[]')
        awardsDesc= self.get_argument('awardsDesc','')
        # name=unicode(self.get_argument('name',''))
        # name=name.replace("\"","")
        # name=name.replace("'","")
        name=day

        desc=unicode(self.get_argument('desc','1'))
        desc=desc.replace("\"","")
        desc=desc.replace("'","")

        sql="insert into FestivalConfig(`day`,`name`,`content`,`desc` ,`note`) values(%s,'%s','%s','%s','%s') on duplicate key update name=values(name),content=values(content),`desc`=values(`desc`),note=values(note) "%(yearday,name,awardList,desc,awardsDesc)
        yield app.DBMgr.getProfileDB().execSql(sql)


        app.Redis.publish(redis_notify.get_platform_redis_notify_channel(conf.PLATFORM), redis_notify.NOTIFY_TYPE_RELOAD_FESTIVALCONFIG)
        self.write(json.dumps({},cls=utils.DateEncoder))
