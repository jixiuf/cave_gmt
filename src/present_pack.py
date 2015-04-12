#  -*- coding:utf-8 -*-
__author__ = 'jixiufeng'


from base_handler import *
from tornado.web import asynchronous

class PresentPackList(BaseHandler):
    @asynchronous
    @gen.coroutine
    def self_get(self):
        packs=yield self.application.dbmgr.presentPackDB.select_all()
        self.render("present_pack_list.html",title="礼包列表",packs=packs)
class PresentPackHideShow(BaseHandler):
    @asynchronous
    @gen.coroutine
    def self_post(self):
        id=self.get_argument('id')
        hide=self.get_argument('hide')
        self.application.dbmgr.presentPackDB.update_hide(id,hide)
        self.write('success')

class PresentPackAdd(BaseHandler):
    @asynchronous
    @gen.coroutine
    def self_get(self):
        self.render("present_pack_add.html",title="礼包打包")
