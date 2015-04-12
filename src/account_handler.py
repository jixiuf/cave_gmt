#coding=utf-8
__author__ = 'jixiufeng'

from base_handler import *
from tornado.web import asynchronous
import hashlib

class ManageRenderHandler(BaseHandler):
    @asynchronous
    @gen.coroutine
    def self_get(self):
        gmAccountList = yield self.application.dbmgr.permissionDB.select_all()
        permissionLevelList=yield self.application.dbmgr.permissionLevelDB.select()
        self.render("gmt_manage.html",
                    title="账号管理",
                    gmAccountList=gmAccountList,
                    permissionLevelList=permissionLevelList)

class RegistrationRenderHandler(BaseHandler):
    def self_get(self):
        self.render("gmt_registration.html",title="账号开通")

class CompetenceRenderHandler(BaseHandler):

    def self_get(self):
        self.render("gmt_competence.html",title="权限管理")

class AccountCreateHandler(BaseHandler):

    @asynchronous
    @gen.coroutine
    def self_post(self):
        account = self.get_argument('account')
        password = self.get_argument('password')
        hpassword = hashlib.sha1(password).hexdigest()
        gmAccount = yield self.application.dbmgr.permissionDB.select(account)

        if gmAccount!=None:
            self.write(json.dumps({ 'action': 'have account'}))
        else:
            yield self.application.dbmgr.permissionDB.add(account,hpassword)
            self.write(json.dumps({ 'action': 'success'}))


class AccountLevelHandler(BaseHandler):

    @asynchronous
    @gen.coroutine
    def self_post(self):
        account = self.get_argument('account')
        level = self.get_argument('level')
        gmAccount= yield self.application.dbmgr.permissionDB.select(account)

        if gmAccount!=None:
            yield self.application.dbmgr.permissionDB.update_level(account,level)
            self.write(json.dumps({ 'action': 'success'}))
        else:
            self.write(json.dumps({ 'action': 'no account'}))

