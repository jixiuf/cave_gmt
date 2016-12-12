#  -*- coding:utf-8 -*-

__author__ = 'jixiufeng'

import traceback
from handler.base import BaseHandler
from tornado.web import asynchronous
from tornado import  gen
import app
import json

class LoginHandler(BaseHandler):
    @gen.coroutine
    def get(self):
        try:
            msg = self.get_argument('msg','')
            self.account = self.get_secure_cookie('user')
            self.password = self.get_secure_cookie('password')
            succ=yield self.verifyAccount(self.account,self.password)
            if succ:            # 如果有cookie 直接登录
                self.redirect(r'/player/search?msg='+msg)
                return
            else:
                self.render("login.html",title="登录",msg=msg)

        except Exception, error:
            self.application.logger.warning('errorarg\t%s\t%s\t%s' % (self.request.headers.get('channel','xxx'),self.request.headers.get('User-Agent','xxx'),str(self.request.arguments)))
            self.application.logger.warning('errormsg\t%s' % (str(error),))
            self.application.logger.warning('errortrace\t%s' % (str(traceback.format_exc()),))

    @gen.coroutine
    def post(self):
        try:
            account = self.get_argument('account')
            rememberPassword = self.get_argument('remember_password','off')
            password = self.get_argument('password').encode('utf-8')
            result = {}
            succ=yield self.verifyAccount(account,password)
            if succ:
                result['action'] = 'success'
                if rememberPassword=="on":
                    self.set_secure_cookie('user',account)
                    self.set_secure_cookie('password',password)
                else:
                    self.set_secure_cookie('user',account)
                    self.clear_cookie('password')
                    # self.clear_cookie('user')
            else:
                result['action'] = 'wrong'

            self.application.logger.warning("%s"%(account) )
            self.write(json.dumps(result))
            self.finish()

        except Exception, error:
            self.application.logger.warning('errorarg\t%s\t%s\t%s' % (self.request.headers.get('channel','xxx'),self.request.headers.get('User-Agent','xxx'),str(self.request.arguments)))
            self.application.logger.warning('errormsg\t%s' % (str(error),))
            self.application.logger.warning('errortrace\t%s' % (str(traceback.format_exc()),))

class LogoutHandler(BaseHandler):
    @gen.coroutine
    def self_get(self):
        self.account = self.get_secure_cookie('user')
        self.password = self.get_secure_cookie('password')
        self.clear_cookie("user")
        self.clear_cookie("password")
        self.render("login.html",title="登录")

