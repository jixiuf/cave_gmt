#  -*- coding:utf-8 -*-
# coding=utf-8
__author__ = 'jixiufeng'


from handler.base import BaseHandler
import utils
from tornado.web import asynchronous
from tornado import  gen
import app
import json
import time
from datetime import datetime, timedelta



class MailEdit(BaseHandler):
    @asynchronous
    @gen.coroutine
    def self_get(self):
        self.render("mail_edit.html",title="邮件编辑")
    @asynchronous
    @gen.coroutine
    def self_post(self):
        award= self.get_argument('awards')
        awardDesc= self.get_argument('awardDesc','')
        title=self.get_argument('title','')
        content=self.get_argument('content','1')
        mailContent=json.dumps({"title":title,"text":content,"sender":self.account})
        startTime=self.get_argument('startTime',datetime.now())
        endTime=self.get_argument('startTime',datetime.now()+ timedelta(days=7))
        # packIcon=self.get_argument('pack_icon')
        playerId=self.userIdTrim(self.get_argument('playerid',''))
        if playerId=="":
            uinList=[0]
        else:
            uinList,suinList,nickNameList=self.splitUinList(playerId)
            uinListFromSUinList=yield self.suinList2uinList(suinList)
            uinListFromNickNameList=yield self.nickNameList2uinList(nickNameList)
            uinList.extend(uinListFromSUinList)
            uinList.extend(uinListFromNickNameList) # str list
        for uin in uinList:
            mailId= int(time.time()*1000000)
            yield app.DBMgr.getMailDraftDB().add(mailId,uin,startTime,endTime,award,awardDesc,mailContent)
            time.sleep(0.001)


    @gen.coroutine
    def suinList2uinList(self,suinList): #
        if len(suinList)==0:
            raise gen.Return([])
        uinList=yield app.DBMgr.getUserDB().select_uin_list_by_suins(",".join(suinList),True)
        raise gen.Return(uinList)
    @gen.coroutine
    def nickNameList2uinList(self,nickNameList): #
        if len(nickNameList)==0:
            raise gen.Return([])
        uinList=yield app.DBMgr.getUserDB().select_uin_list_by_nickname(nickNameList,True)
        raise gen.Return(uinList)


    def splitUinList(self,userIdListStr): # return uinStrList,suinStrList,nickNameStrList
        userIdListStr=self.userIdTrim(userIdListStr)
        userIdStrList=userIdListStr.split(",")
        uinList=[]
        suinList=[]
        nickNameList=[]
        for userId in userIdStrList:
            if userId!="":
                if len(userId)<12 and userId.isdigit(): # 认为是短id
                    suinList.append(userId)
                elif userId.isdigit():
                    uinList.append(userId)
                else:
                    nickNameList.append(userId)
        return uinList,suinList,nickNameList


    def userIdTrim(self,userIdListStr):
        if userIdListStr==None:
            return ""

        # self.render("present_pack_add.html",title="礼包打包")
        userIdListStr=userIdListStr.replace(" ","")
        userIdListStr=userIdListStr.replace(u"　","")
        userIdListStr=userIdListStr.replace("\t","")
        userIdListStr=userIdListStr.replace("\n",",")
        userIdListStr=userIdListStr.replace("\r",",")
        userIdListStr=userIdListStr.replace(u"，",",")
        while ",," in userIdListStr:
            userIdListStr=userIdListStr.replace(",,",",")
        return userIdListStr


class MailDraftList(BaseHandler):

    @asynchronous
    @gen.coroutine
    def self_get(self):
        mailList=yield app.DBMgr.getMailDraftDB().select_all()
        print(mailList)
        self.render("mail_draft_list.html",title="邮件草稿列表",mailList=mailList)
class MailDraftSend(BaseHandler):

    @asynchronous
    @gen.coroutine
    def self_post(self):
        mailId= self.get_argument('mailId',0)
        if mailId==0:
            self.write('mail id is empty')
            return


        ml=yield app.DBMgr.getMailDraftDB().select_by_mailid(mailId)
        if ml==None:
            self.write('mail doesnot exsits')
            return

        newMailId= int(time.time()*1000000)
        yield app.DBMgr.getMailDB().add(newMailId,ml['uin'],ml['startTime'],ml['endTime'],ml['awardStr'],json.dumps(ml['content']))
        yield app.DBMgr.getMailDraftDB().updateStatusReaded(mailId)
        self.write('success')
class MailDraftDelete(BaseHandler):

    @asynchronous
    @gen.coroutine
    def self_post(self):
        mailId= self.get_argument('mailId',0)
        if mailId==0:
            self.write('mail id is empty')
            return


        ml=yield app.DBMgr.getMailDraftDB().select_by_mailid(mailId)
        if ml==None:
            self.write('mail doesnot exsits')
            return

        yield app.DBMgr.getMailDraftDB().delete(mailId)
        self.write('success')
