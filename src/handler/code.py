#  -*- coding:utf-8 -*-
# coding=utf-8
__author__ = 'jixiufeng'
# 礼包码 激活码

from handler.base import BaseHandler
import utils
from tornado.web import asynchronous
from tornado import  gen
import app
import json
import conf
import time
import redis_notify
from datetime import datetime,timedelta
import random
import string
import math



class CodeMgr(BaseHandler):
    chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789' # 去除1l0oO等难以分辨的字符
    def mapRow1(self,row):
        return row[0]

    @asynchronous
    @gen.coroutine
    def self_get(self):
        hidden= self.get_argument('hidden','')
        serverIdList=app.DBMgr.get_all_server_id()
        self.render("code_mgr.html",title="礼包码生成",
                    hidden=hidden,
                    Account=self.gmAccount,
                    serverIdList=serverIdList)
    @asynchronous
    @gen.coroutine
    def self_post(self):
        serverId= self.get_argument('serverid','1')
        # award= self.get_argument('awards')
        awardList= self.get_argument('award_list' ,'[]')
        awardsDesc= self.get_argument('awardsDesc','')
        name=self.get_argument('name','')
        desc=self.get_argument('desc','')
        limitCnt=self.get_argument('limitCnt','')
        batchLimitCnt=self.get_argument('batchLimitCnt','')
        group=self.get_argument('group','')
        cnt=int(self.get_argument('cnt','1'))
        startTime=self.get_argument('startTime','')
        endTime=self.get_argument('endTime','')
        channelSDK=self.get_argument('channelSDK','') # prefix
        hidden=self.get_argument('hidden','')
        if awardList=='[]':
            self.write(json.dumps({'result':"奖品为空"}))
            return



        mailContent=json.dumps({"title":name,
                                "text":desc,
                                "award_list":json.loads(awardList),
                                "sender":self.account}
                               ,ensure_ascii=False)
        data={}
        data['data']=[]
        data['result']=''
        batchCode=1
        if hidden!='':
            sql="select ifnull(min(batchCode),0) as max_batch_code from CodeBase " # 获取当前最大批号
            maxBatchCode=yield app.DBMgr.getProfileDB().queryObject(sql,self.mapRow1)
            batchCode=maxBatchCode-1
        else:
            sql="select ifnull(max(batchCode),0) as max_batch_code from CodeBase " # 获取当前最大批号
            maxBatchCode=yield app.DBMgr.getProfileDB().queryObject(sql,self.mapRow1)
            batchCode=1+maxBatchCode
            if batchCode<1:
                batchCode=1



        data['batchCode']=batchCode
        codes=[]
        codePrefix=channelSDK+str(batchCode) # 前缀加批号
        codeSuffixLen=5
        maxCodeCnt=int(math.pow(len(CodeMgr.chars),codeSuffixLen)) # 最大只能产生那么多激活码
        if cnt>maxCodeCnt:
            cnt=maxCodeCnt


        i=0
        while True:
            if len(codes)>=cnt or i>maxCodeCnt: # 最多只尝试maxCodeCnt次，以避免死循环
                break
            i=i+1
            code=self.activation_code(codePrefix,codeSuffixLen)
            if not code in codes:
                codes.append(code)

        sqlPrefix="INSERT INTO `CodeBase` (`server`,`code`,`channelCode`,`batchCode`,`startTime`,`endTime`,`limitCnt`,`useCnt`,`batchLimitCnt`,name,`content`,`desc`,`group`) VALUES "

        i=0
        sql=sqlPrefix
        for code in codes:
            data['data'].append(code)
            i=i+1
            sql+=" (%s,'%s','%s','%s','%s','%s',%s,%s,%s,'%s','%s','%s','%s')"%(serverId,code,channelSDK,batchCode,startTime,endTime,limitCnt,0,batchLimitCnt,name,mailContent,desc,group)
            if i%300==0 or i==len(codes):
                yield app.DBMgr.getProfileDB().execSql(sql)
                sql=sqlPrefix
            else:
                sql+=","
        self.write(json.dumps(data,cls=utils.DateEncoder))


    def activation_code(self,prefix,length=10):
        '''
        id + L + 随机码
        string模块中的3个函数：string.letters，string.printable，string.printable
        '''
        # chars=string.ascii_letters+string.digits
        return prefix + ''.join([random.choice(CodeMgr.chars) for i in range(length)])

class CodeList(BaseHandler):

    def mapRow1(self,row):
        return row[0]

    @asynchronous
    @gen.coroutine
    def self_get(self):
        sql="select ifnull(max(batchCode),0) as max_batch_code from CodeBase " # 获取当前最大批号
        maxBatchCode=yield app.DBMgr.getProfileDB().queryObject(sql,self.mapRow1)
        batchCodeList=range(1,1+maxBatchCode)
        batchCodeList.reverse()

        serverIdList=app.DBMgr.get_all_server_id()
        self.render("code_list.html",title="礼包码列表",
                    Account=self.gmAccount,
                    batchCodeList=batchCodeList,
                    serverIdList=serverIdList)

    def mapRow(self,row):
        data={}
        data['server']=row[0]
        data['code']=row[1]
        data['channelCode']=row[2]
        data['batchCode']=row[3]
        data['startTime']=row[4]
        data['endTime']=row[5]
        data['limitCnt']=row[6]
        data['useCnt']=row[7]
        data['batchLimitCnt']=row[8]
        data['name']=row[9]
        data['content']=row[10]
        data['desc']=row[11]
        data['group']=row[12]
        return data

    @asynchronous
    @gen.coroutine
    def self_post(self):
        serverId= self.get_argument('serverid','1')
        batchCode= self.get_argument('batchCode','1')
        channelCode= self.get_argument('channelCode','')
        sql="select `server`,`code`,`channelCode`,`batchCode`,`startTime`,`endTime`,`limitCnt`,`useCnt`,`batchLimitCnt`,name,`content`,`desc`,`group` from `CodeBase` where server=%s and batchCode=%s "%(serverId,batchCode)
        if channelCode!='':
            sql= sql+"channelCode='%s'"%(channelCode)


        list=yield app.DBMgr.getProfileDB().query(sql,self.mapRow)

        data={}
        data['cnt']=len(list)   # 共有多少个码
        data['data']=list
        totalUseCnt=0           # 这批码 共领取了多少次

        for code in list:
            totalUseCnt=totalUseCnt+code['useCnt']
            data['limitCnt']=code['limitCnt'] # 一个码允许使用次数
            data['batchLimitCnt']=code['batchLimitCnt'] # 本批码允许一个玩家领取的最大次数
            data['startTime']=code['startTime']
            data['endTime']=code['endTime']
            data['desc']=code['desc']
            data['name']=code['name']
            data['channelCode']=code['channelCode']
            data['server']=code['server']
            data['group']=code['group']
        data['totalUseCnt']=totalUseCnt
        self.write(json.dumps(data,cls=utils.DateEncoder))



class CodeDel(BaseHandler):
    @asynchronous
    @gen.coroutine
    def self_post(self):
        batchCode= self.get_argument('batchCode','1')
        sql="delete from CodeBase where batchCode=%s"%(batchCode)
        yield app.DBMgr.getProfileDB().execSql(sql)
        self.write("success")
