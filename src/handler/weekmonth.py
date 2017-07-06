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



class WeekMonth(BaseHandler):
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
        sql="select gameConfigKey,gameConfigValue,gameConfigTitle,gameConfigDesc,gameConfigExtra from GameConfig where gameConfigKey=4 or gameConfigKey=5 order by gameConfigKey asc"
        list=yield app.DBMgr.getProfileDB().query(sql,mapRow)
        weekInfo={'gameConfigKey':4,'gameConfigValue':'','gameConfigTitle':'周卡首日奖励','gameConfigDesc':''}
        monthInfo={'gameConfigKey':5,'gameConfigValue':'','gameConfigTitle':'月卡首日奖励','gameConfigDesc':''}
        if len(list)>0:
            weekInfo=list[0]
            if weekInfo['gameConfigExtra']!='':
                extra=json.loads(weekInfo['gameConfigExtra'])
                weekInfo['name']=extra.get('name')
            else:
                weekInfo['name']=''

        if len(list)>1:
            monthInfo=list[1]
            if monthInfo['gameConfigExtra']!='':
                extra=json.loads(monthInfo['gameConfigExtra'])
                monthInfo['name']=extra.get('name')
            else:
                monthInfo['name']=''



        serverIdList=app.DBMgr.get_all_server_id()
        self.render("weekmonth.html",title="月卡周卡配置",
                    weekInfo=weekInfo,
                    monthInfo=monthInfo,
                    Account=self.gmAccount,
                    serverIdList=serverIdList)
    @asynchronous
    @gen.coroutine
    def self_post(self):
        # serverId= self.get_argument('serverid','1')
        id= self.get_argument('id','0')
        name= self.get_argument('name','0')
        # award= self.get_argument('awards')
        awardList= self.get_argument('award_list' ,'[]')
        awardsDesc= self.get_argument('awardsDesc','')
        title=''
        if id=='4':
            title=u'周卡首日奖励'
        else:
            title=u'月卡首日奖励'
        extra=json.dumps({"name":name,
                          "content":json.loads(awardList),}
                         ,ensure_ascii=False)


        sql="insert into GameConfig(`gameConfigKey`,`gameConfigValue`,`gameConfigTitle`,`gameConfigDesc`,gameConfigType,gameConfigEditable,gameConfigExtra) values(%s,'%s','%s','%s',1,0,'%s') on duplicate key update gameConfigTitle=values(gameConfigTitle),gameConfigDesc=values(gameConfigDesc),gameConfigValue=values(gameConfigValue),gameConfigExtra=values(gameConfigExtra) "%(id,awardList,title,awardsDesc,extra)
        yield app.DBMgr.getProfileDB().execSql(sql)


        app.Redis.publish(redis_notify.get_platform_redis_notify_channel(conf.PLATFORM), redis_notify.NOTIFY_TYPE_GAMECONFIG_RELOAD)
        self.write(json.dumps({},cls=utils.DateEncoder))

