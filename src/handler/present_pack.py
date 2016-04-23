#  -*- coding:utf-8 -*-
__author__ = 'jixiufeng'


from handler.base import BaseHandler
import utils
from tornado.web import asynchronous
from tornado import  gen
import app


class PresentPackList(BaseHandler):
    @asynchronous
    @gen.coroutine
    def self_get(self):
        # playerInfo=yield app.DBMgr.getUserDB().select_by_uin(144150423530676224)
        # playerInfo=yield app.DBMgr.getUserAttrDB(1).select_by_uin(144150423530676224)
        # print playerInfo
        packs=yield app.DBMgr.presentPackDB.select_all()
        self.render("present_pack_list.html",title="礼包列表",packs=packs)
class PresentPackHideShow(BaseHandler):
    @asynchronous
    @gen.coroutine
    def self_post(self):
        id=self.get_argument('id')
        hide=self.get_argument('hide')
        app.DBMgr.presentPackDB.update_hide(id,hide)
        self.write('success')

class PresentPackAdd(BaseHandler):
    @asynchronous
    @gen.coroutine
    def self_get(self):
        self.render("present_pack_add.html",title="礼包打包")
    @asynchronous
    @gen.coroutine
    def self_post(self):
        awardList= self.get_argument('awards')
        packName=self.get_argument('pack_name','')
        packVersion=self.get_argument('version','1')
        # packIcon=self.get_argument('pack_icon')
        status=self.get_argument('status','')
        yield app.DBMgr.presentPackDB.add(packName,awardList,packVersion,status)
        # self.render("present_pack_add.html",title="礼包打包")
