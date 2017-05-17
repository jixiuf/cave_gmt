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
    chars='abcdefghjkmnpqrstuvwxyzABCDEFGHIJKLMNPQRSTUVWXYZ23456789' # 去除1l0oO等难以分辨的字符
    def mapRow1(self,row):
        return row[0]

    @asynchronous
    @gen.coroutine
    def self_get(self):
        serverIdList=app.DBMgr.get_all_server_id()
        self.render("code_mgr.html",title="礼包码管理（生成）",
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
        if awardList=='[]':
            self.write(json.dumps({'result':"奖品为空"}))
            return



        mailContent=json.dumps({"title":name,
                                "text":desc,
                                "award_list":json.loads(awardList),
                                "sender":self.account}
                               ,ensure_ascii=False)
        print(mailContent)
        data={}
        data['data']=[]
        data['result']=''
        sql="select ifnull(max(batchCode),0) as max_batch_code from CodeBase " # 获取当前最大批号
        maxBatchCode=yield app.DBMgr.getProfileDB().queryObject(sql,self.mapRow1)
        batchCode=1+maxBatchCode
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

        for code in codes:
            sql="INSERT INTO `CodeBase` (`server`,`code`,`channelCode`,`batchCode`,`startTime`,`endTime`,`limitCnt`,`useCnt`,`batchLimitCnt`,`content`,`desc`,`group`) VALUES (%s,'%s','%s','%s','%s','%s',%s,%s,%s,'%s','%s','%s')"%(serverId,code,channelSDK,batchCode,startTime,endTime,limitCnt,0,batchLimitCnt,mailContent,desc,group)
            yield app.DBMgr.getProfileDB().execSql(sql)
            data['data'].append(code)
        self.write(json.dumps(data,cls=utils.DateEncoder))


    def activation_code(self,prefix,length=10):
        '''
        id + L + 随机码
        string模块中的3个函数：string.letters，string.printable，string.printable
        '''
        # chars=string.ascii_letters+string.digits
        return prefix + ''.join([random.choice(CodeMgr.chars) for i in range(length)])
