#  -*- coding:utf-8 -*-

__author__ = 'jixiufeng'

from base_handler import *
from tornado.web import asynchronous
from tornado import  gen
import hashlib

class LoginHandler(BaseHandler):
    def get(self):
        try:
            self.render("login.html",title="登录")
        except Exception, error:
            self.application.logger.warning('errorarg\t%s\t%s\t%s' % (self.request.headers.get('channel','xxx'),self.request.headers.get('User-Agent','xxx'),str(self.request.arguments)))
            self.application.logger.warning('errormsg\t%s' % (str(error),))
            self.application.logger.warning('errortrace\t%s' % (str(traceback.format_exc()),))

    @gen.coroutine
    def post(self):
        try:
            account = self.get_argument('account')
            self.password = self.get_argument('password').encode('utf-8')
            gmAccount=yield self.application.dbmgr.permissionDB.select(account)
            hpassword = hashlib.sha1(self.password).hexdigest()
            result = {}
            self.application.logger.warning("%s"%(account) )
            if gmAccount==None:
                result['action'] = 'wrong'
            else:
                if gmAccount.passwd == hpassword and gmAccount.passwd!="":
                    self.set_secure_cookie("user", gmAccount.account)
                    result['action'] = 'success'
                else:
                    result['action'] = 'wrong'

            self.write(json.dumps(result))
            self.finish()

        except Exception, error:
            self.application.logger.warning('errorarg\t%s\t%s\t%s' % (self.request.headers.get('channel','xxx'),self.request.headers.get('User-Agent','xxx'),str(self.request.arguments)))
            self.application.logger.warning('errormsg\t%s' % (str(error),))
            self.application.logger.warning('errortrace\t%s' % (str(traceback.format_exc()),))

