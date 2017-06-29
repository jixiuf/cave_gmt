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



class Day7Config(BaseHandler):
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
        sql="select `day`,`name`,`content`,`desc` ,`note` from Day7Config order by day asc "
        day7configList=yield app.DBMgr.getProfileDB().query(sql,mapRow)
        serverIdList=app.DBMgr.get_all_server_id()
        self.render("day7config.html",title="7天登录活动奖励配置",
                    day7configList=day7configList,
                    Account=self.gmAccount,
                    serverIdList=serverIdList)
    @asynchronous
    @gen.coroutine
    def self_post(self):
        # serverId= self.get_argument('serverid','1')
        day= self.get_argument('day','0')
        # award= self.get_argument('awards')
        awardList= self.get_argument('award_list' ,'[]')
        awardsDesc= self.get_argument('awardsDesc','')
        name=unicode(self.get_argument('name',''))
        name=name.replace("\"","")
        name=name.replace("'","")

        desc=unicode(self.get_argument('desc','1'))
        desc=desc.replace("\"","")
        desc=desc.replace("'","")

        sql="insert into Day7Config(`day`,`name`,`content`,`desc` ,`note`) values(%s,'%s','%s','%s','%s') on duplicate key update name=values(name),content=values(content),`desc`=values(`desc`),note=values(note) "%(day,name,awardList,desc,awardsDesc)
        yield app.DBMgr.getProfileDB().execSql(sql)


        app.Redis.publish(redis_notify.get_platform_redis_notify_channel(conf.PLATFORM), redis_notify.NOTIFY_TYPE_RELOAD_DAY7CONFIG)
        self.write(json.dumps({},cls=utils.DateEncoder))

