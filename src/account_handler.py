#coding=utf-8
__author__ = 'jixiufeng'

from base_handler import *
from tornado.web import asynchronous
import hashlib

class ManageRenderHandler(BaseHandler):
    def self_get(self):
        self.render("gmt_manage.html",title="账号管理")

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

class PerssionLevelHandler(BaseHandler):
    @asynchronous
    @gen.coroutine
    def self_post(self):
        levels=yield self.application.dbmgr.permissionLevelDB.select()
        result = []
        for level in levels:
            info = {}
            info['level'] = level.level
            info['name'] = level.levelDesc
            result.append(info)

        res = {
            'action': 'success',
            'result': json.dumps(result)
        }

        self.write(json.dumps(res))
        self.finish()

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

