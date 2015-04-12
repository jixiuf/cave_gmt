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


# class PresentPackInfoHandler(BaseHandler):
#     @asynchronous
#     @gen.coroutine
#     def self_post(self):
#         if self.request.arguments.has_key('status'):
#             # status = self.request.arguments['status'][0]
#             status = self.request.arguments['status'][0]
#         else:
#             status = ''
#         packs=yield self.application.dbmgr.presentPackDB.select_by_status( status)
#         result=[]
#         for item in packs:
#             if item.hide == 1:
#                 continue
#             result.append([
#                 item.id,
#                 '礼包名称：' + str(item.name),
#                 item.content
#             ])
#         self.write(json.dumps(result))
#         self.finish()

