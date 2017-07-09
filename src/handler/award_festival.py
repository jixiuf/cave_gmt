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


# 节日礼包
class AwardFestival(BaseHandler):
    @asynchronous
    @gen.coroutine
    def self_get(self):
        def mapRow(row):
            data={}
            data['gameConfigKey']=row[0]
            data['gameConfigValue']=row[1]
            data['gameConfigTitle']=row[2]
            data['gameConfigDesc']=row[3]
            data['gameConfigExtra']=row[4]
            return data
        sql="select gameConfigKey,gameConfigValue,gameConfigTitle,gameConfigDesc,gameConfigExtra from GameConfig where gameConfigKey in (9) order by gameConfigKey asc"
        list=yield app.DBMgr.getProfileDB().query(sql,mapRow)
        for data in list:
            if data!=None:
                if data['gameConfigExtra']!='':
                    extra=json.loads(data['gameConfigExtra'])
                    data['startTime']=extra['startTime']
                    data['endTime']=extra['endTime']
                    data['name']=extra.get('name')
                    data['desc']=extra.get('desc')
                    if data['name']=='':
                        data['name']='空'
                else:
                    data['startTime']=''
                    data['endTime']=''
                    data['name']='空'
                    data['desc']='空'



        serverIdList=app.DBMgr.get_all_server_id()
        self.render("award_festival.html",title="节日登录礼包",
                    list=list,
                    Account=self.gmAccount,
                    serverIdList=serverIdList)
    @asynchronous
    @gen.coroutine
    def self_post(self):
        # serverId= self.get_argument('serverid','1')
        id= self.get_argument('id','6')
        name= self.get_argument('name','节日登录礼包')
        desc= self.get_argument('desc','节日登录礼包')
        awardList= self.get_argument('award_list' ,'[]')
        awardsDesc= self.get_argument('awardsDesc','')
        title=u'节日登录礼包'
        startTime=self.get_argument('startTime','')
        endTime=self.get_argument('endTime','')
        extra=json.dumps({"startTime":startTime,
                          "name":name,
                          "content":json.loads(awardList),
                          "desc":desc,
                          "endTime":endTime}
                         ,ensure_ascii=False)



        sql="insert into GameConfig(`gameConfigKey`,`gameConfigValue`,`gameConfigTitle`,`gameConfigDesc`,gameConfigType,gameConfigEditable,gameConfigExtra) values(%s,'%s','%s','%s',1,0,'%s') on duplicate key update gameConfigTitle=values(gameConfigTitle),gameConfigDesc=values(gameConfigDesc),gameConfigValue=values(gameConfigValue),gameConfigExtra=values(gameConfigExtra) "%(id,awardList,title,awardsDesc,extra)
        yield app.DBMgr.getProfileDB().execSql(sql)


        app.Redis.publish(redis_notify.get_platform_redis_notify_channel(conf.PLATFORM), redis_notify.NOTIFY_TYPE_GAMECONFIG_RELOAD)
        self.write(json.dumps({},cls=utils.DateEncoder))

