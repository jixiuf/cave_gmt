#  -*- coding:utf-8 -*-
__author__ = 'jixiufeng'


import utils
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
    @asynchronous
    @gen.coroutine
    def self_post(self):
        awardList= utils.getJson(self.get_argument('awards'))
        content=''

        for award in awardList:
            awardSubId=award["award_sub_id"]
            if awardSubId=="":
                awardSubId="0"
            awardCount=str(award["award_count"])
            if awardCount.isdigit():
                awardCount=awardCount
            elif utils.is_float(awardCount):
                awardCount=awardCount
            else:
                self.application.logger.warning('present_pack_award_count_not_number,%s',awardCount)
                continue
            content= content+str(award["award_type_id"])+":"+awardSubId+":"+str(awardCount)+"|"
        if len(content)!=0:
            content=content[:-1]


        if content=="":
            return

        packName=self.get_argument('pack_name')
        packVersion=self.get_argument('version')
        # packIcon=self.get_argument('pack_icon')
        status=self.get_argument('status')
        yield self.application.dbmgr.presentPackDB.add(packName,content,packVersion,status)
        # self.render("present_pack_add.html",title="礼包打包")

class PresentPackIdList(BaseHandler):
    @asynchronous
    @gen.coroutine
    def self_get(self):
        self.render("present_pack_add.html",title="礼包打包")

