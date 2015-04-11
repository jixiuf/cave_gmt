#  -*- coding:utf-8 -*-
__author__ = 'fanngyuan'

import tornado
import json
from tornado.web import asynchronous
from tornado import  gen
import traceback
from utils import get_all_urls

class BaseHandler(tornado.web.RequestHandler):
    def __init__(self, *args, **kwargs):
        super(BaseHandler, self).__init__(*args, **kwargs)


    @gen.coroutine
    def permission_verify(self):
        self.account = self.get_secure_cookie('user')
        gmAccount =  yield self.application.dbmgr.permissionDB.select(self.account)
        if gmAccount==None:
            self.no_permissions()
        else:
            if gmAccount.level == 1:
                urls = get_all_urls(self.application.handlers).split(',')
            else:
                urls = gmAccount.urls.split(',')
            self.check_permissions(urls)

    def have_permissions(self):
        self.application.gm_logger.info('infoarg\t%s\t%s\t%s\t%s' % (self.account,self.request.uri,self.request.headers.get('User-Agent','xxx'),str(self.request.arguments)))
        self.service()

    def no_permissions(self):
        if self.type == 'get':
            self.redirect('/')
        if self.type == 'post':
            self.write('wrong permissions')

    def check_permissions(self,urls):
        count = 0
        for i in urls:
            count += 1
            if i == self.request.uri.split('?')[0]:
                self.have_permissions()
                return
            if count == len(urls):
                self.no_permissions()

    @gen.coroutine
    def get(self):
        try:
            self.service = self.self_get
            self.type = 'get'
            yield self.permission_verify()
        except Exception, error:
            self.application.logger.warning('errorarg\t%s\t%s\t%s' % (self.request.headers.get('channel','xxx'),self.request.headers.get('User-Agent','xxx'),str(self.request.arguments)))
            self.application.logger.warning('errormsg\t%s' % (str(error),))
            self.application.logger.warning('errortrace\t%s' % (str(traceback.format_exc()),))

    @gen.coroutine
    def post(self):
        try:
            self.service = self.self_post
            self.type = 'post'
            yield self.permission_verify()
        except Exception, error:
            self.application.logger.warning('errorarg\t%s\t%s\t%s' % (self.request.headers.get('channel','xxx'),self.request.headers.get('User-Agent','xxx'),str(self.request.arguments)))
            self.application.logger.warning('errormsg\t%s' % (str(error),))
            self.application.logger.warning('errortrace\t%s' % (str(traceback.format_exc()),))

