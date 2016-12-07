#coding=utf-8
__author__ = 'jixiufeng'

from tornado import  gen
from handler.base import *
from tornado.web import asynchronous
import hashlib
import json
import app

class AccountManageRenderHandler(BaseHandler):
    @asynchronous
    @gen.coroutine
    def self_get(self):
        msg = self.get_argument('msg','')
        gmAccountList = yield app.DBMgr.permissionDB.select_all()
        permissionLevelList=yield app.DBMgr.permissionLevelDB.select()
        gmAccount2 =  yield app.DBMgr.permissionDB.select(self.account)
        self.render("account_manage.html",
                    title="账号管理",
                    Account=gmAccount2,
                    msg=msg,
                    gmAccountList=gmAccountList,
                    permissionLevelList=permissionLevelList)

class AccountRegistrationRenderHandler(BaseHandler):
    def self_get(self):
        channelMap=conf.getChannelNameMap()
        self.render("account_registration.html",title="账号开通",
                    Account=self.gmAccount,
                    channelMap=channelMap)

class AccountCreateHandler(BaseHandler):

    @asynchronous
    @gen.coroutine
    def self_post(self):
        account = self.get_argument('account')
        password = self.get_argument('password')
        channel = int(self.get_argument('channel'))
        hpassword = hashlib.sha1(password).hexdigest()
        gmAccount = yield app.DBMgr.permissionDB.select(account)

        if gmAccount!=None:
            self.write(json.dumps({ 'action': 'have account'}))
        else:
            yield app.DBMgr.permissionDB.add(account,channel,hpassword)
            self.write(json.dumps({ 'action': 'success'}))


class AccountLevelHandler(BaseHandler):

    @asynchronous
    @gen.coroutine
    def self_post(self):
        account = self.get_argument('account')
        level = self.get_argument('level',0)
        delete = self.get_argument('delete',"false")
        if delete=="true":
            yield app.DBMgr.permissionDB.delete(account)
            self.write(json.dumps({ 'action': 'success'}))
            return
        else:
            gmAccount= yield app.DBMgr.permissionDB.select(account)
            if gmAccount!=None:
                yield app.DBMgr.permissionDB.update_level(account,level)
                self.write(json.dumps({ 'action': 'success'}))
            else:
                self.write(json.dumps({ 'action': 'no account'}))

