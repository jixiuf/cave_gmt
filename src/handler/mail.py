#  -*- coding:utf-8 -*-
# coding=utf-8
__author__ = 'jixiufeng'


from handler.base import BaseHandler
import utils
from tornado.web import asynchronous
from tornado import  gen
import app



class MailEdit(BaseHandler):
    @asynchronous
    @gen.coroutine
    def self_get(self):
        self.render("mail_edit.html",title="邮件编辑")
    @asynchronous
    @gen.coroutine
    def self_post(self):
        awardList= self.get_argument('awards')
        title=self.get_argument('title','')
        content=self.get_argument('content','1')
        # packIcon=self.get_argument('pack_icon')
        playerId=self.userIdTrim(self.get_argument('playerid',''))
        uinList,suinList,nickNameList=self.splitUinList(playerId)
        uinListFromSUinList=yield self.suinList2uinList(suinList)
        uinListFromNickNameList=yield self.nickNameList2uinList(nickNameList)
        uinList.extend(uinListFromSUinList)
        uinList.extend(uinListFromNickNameList) # str list
        for uin in uinList:
            return


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

