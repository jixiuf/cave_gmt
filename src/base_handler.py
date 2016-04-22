#  -*- coding:utf-8 -*-
__author__ = 'fanngyuan'

import tornado
import json
from tornado.web import asynchronous
from tornado import  gen
import conf
import traceback
from utils import get_all_urls

from qiniu import Auth, put_file, etag, urlsafe_base64_encode
import qiniu.config

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

class QiniuUptokenHandler(BaseHandler):
    # http://127.0.0.1:8000/api/qiniu/uptoken?file_name=helllo&user=najaplus&password=qHcdGfE6TH
    def self_get(self):
        return self.self_post()
    def self_post(self):

        #构建鉴权对象
        q = Auth(conf.QINIU_ACCESS_KEY,conf.QINIU_SECRET_KEY)
        bucket_name = conf.QINIU_SECRET_BUCKET_NAME

        user = self.get_argument('user', None)
        password = self.get_argument('password', None)
        if user != conf.DYNAMIC_USER and password != conf.DYNAMIC_PASSWORD:
            self.write(json.dumps({"error":"need user and password"}))
            return

        key = self.get_argument('file_name')
        if key==None or key=="":
            self.write(json.dumps({"error":"need file_name param"}))
            return
        else:
            #生成上传 Token，可以指定过期时间等
            token = q.upload_token(bucket_name, key, 3600)
            result = {
                'uptoken': token
            }
            self.write(json.dumps(result))
