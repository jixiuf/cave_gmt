#  -*- coding:utf-8 -*-
__author__ = 'jixiufeng'


from base import *

from chardet import detect
import datetime
from tornado.web import asynchronous
import redis_notify

class NoticeManageRenderHandler(BaseHandler):

    def self_get(self):
        serverIdList= app.DBMgr.get_all_server_id()
        self.render("notice_manage.html",title="公告管理",
                    Account=self.gmAccount,
                    serverIdList=serverIdList)

class NoticeAddRenderHandler(BaseHandler):
    def self_get(self):
        serverIdList= app.DBMgr.get_all_server_id()
        self.render("notice_add.html",title="公告添加",
                    Account=self.gmAccount,
                    serverIdList=serverIdList)

class NoticeEditRenderHandler(BaseHandler):

    def self_get(self):
        self.render("notice_edit.html",
                    Account=self.gmAccount,
                    title="公告发布")

class NoticeInfoHandler(BaseHandler):

    @asynchronous
    @gen.coroutine
    def self_post(self):
        now=datetime.datetime.now()
        serverIdStr=self.get_argument('serverId')
        res = yield app.DBMgr.noticeDB.select(serverIdStr,now)

        result = []

        for i in res:
            if i['updateTime']:
                update=i['updateTime'].strftime("%Y-%m-%d")
                i['updateTime'] = update
            if i['startTime']:
                start=i['startTime'].strftime("%Y-%m-%d")
                i['startTime'] = start
            if i['endTime']:
                end=i['endTime'].strftime("%Y-%m-%d")
                i['endTime'] = end
            result.append(i)
        self.write(json.dumps(result))

class NoticeAddInfoHandler(BaseHandler):

    @asynchronous
    @gen.coroutine
    def self_post(self):
        now=datetime.datetime.now()
        serverIdStr=self.get_argument('serverId')
        res = yield app.DBMgr.noticeDB.get_notice(serverIdStr,now)

        result = []

        for i in res:
            if i['updateTime']:
                update=i['updateTime'].strftime("%Y-%m-%d")
                i['updateTime'] = update
            if i['startTime']:
                start=i['startTime'].strftime("%Y-%m-%d")
                i['startTime'] = start
            if i['endTime']:
                end=i['endTime'].strftime("%Y-%m-%d")
                i['endTime'] = end
            result.append(i)
        self.write(json.dumps(result))
        self.finish()

class NoticeAddHandler(BaseHandler):

    @asynchronous
    @gen.coroutine
    def self_post(self):
        now=datetime.datetime.now()
        title=self.request.arguments['title'][0]
        content=self.request.arguments['content'][0]
        start=self.request.arguments['start'][0]
        end=self.request.arguments['finish'][0]
        serverId=self.request.arguments['serverId'][0]

        yield app.DBMgr.noticeDB.add(title,content,serverId,now,start,end)

class NoticeUpdateHandler(BaseHandler):

    @asynchronous
    @gen.coroutine
    def self_post(self):
        url=json.loads(self.request.arguments['url'][0])
        remove_id=json.loads(self.request.arguments['remove_id'][0])
        update=json.loads(self.request.arguments['update'][0])

        yield app.DBMgr.noticeDB.remove_url()
        if remove_id:
            ids = str(','.join(remove_id))
            yield app.DBMgr.noticeDB.remove_notice( ids)
        if update:
            for i in update.keys():
                yield app.DBMgr.noticeDB.set_sequence( int(i), int(update[i]))
        if url:
            url_first = str(url['0'])
            url_second = str(url['1'])
            yield app.DBMgr.noticeDB.update_url( url_first, url_second)
        app.Redis.publish(redis_notify.get_platform_redis_notify_channel(conf.PLATFORM), redis_notify.NOTIFY_TYPE_RELOAD_NOTICE)


