#  -*- coding:utf-8 -*-
__author__ = 'jixiufeng'

from base_handler import *
from tornado.web import asynchronous
from utils import DateEncoder
import sys
import time
import redis_notify
import conf
from db.db_dynamic_version_update import DynamicVersionUpdate
from db.db_version_update import VersionUpdate
from db.db_server_version import ServerVersion

class GameUpdateRenderHandler(BaseHandler):
    @asynchronous
    def self_get(self):
        result = {
            'channels': json.dumps(conf.getChannelList()),
            'defaultChannelName':json.dumps(conf.getChannelNameMap()),
        }
        print(result)
        self.render("game_update.html",title="动态更新",result=result)

class DynamicHandler(tornado.web.RequestHandler):

    def post(self):
        self.permission_verify()

    def permission_verify(self):
        user = self.get_argument('user', None)
        password = self.get_argument('password', None)

        platform = self.get_argument('platform', str(conf.PLATFORM))
        channel = self.get_argument('channel', None)
        version = self.get_argument('version', None)
        url = self.get_argument('url', None)
        size = self.get_argument('size', None)
        if size=="":
            size="0"
        comment = self.get_argument('comment', None)
        note = self.get_argument('note', None)
        svnVersion = self.get_argument('svnVersion', None)
        if svnVersion=="":
            svnVersion="0"


        if user == conf.DYNAMIC_USER and password == conf.DYNAMIC_PASSWORD:
            if channel == None or version == None or  url == None or size == None or comment == None or note == None or svnVersion == None:
                self.failed('need 8 arguments')
            else:
                self.success(platform,channel,version,url,size,comment,note,svnVersion)
        else:
            self.failed('verification dose note pass')

    @asynchronous
    @gen.coroutine
    def success(self,platform,channel,version,url,size,comment,note,svnVersion):
        info=yield self.application.dbmgr.dynamicVersionUpdateDB.select(int(channel),int(version))
        if info==None:
            info=DynamicVersionUpdate()
            info.channel=int(channel)
            info.version=int(version)
            info.url=url
            info.size=int(size)
            info.comment=comment
            info.note=note
            info.svnVersion=int(svnVersion)
            yield self.application.dbmgr.dynamicVersionUpdateDB.add(info)
        else:
            info.url=url
            info.size=int(size)
            info.comment=comment
            info.note=note
            info.svnVersion=int(svnVersion)
            yield self.application.dbmgr.dynamicVersionUpdateDB.update(info)
        res = {
            'status': 'success'
        }
        self.application.redis.publish(redis_notify.get_platform_redis_notify_channel(platform), redis_notify.NOTIFY_TYPE_RELOAD_SERVER_VERSION)
        self.write(res)

    def failed(self, info):
        res = {
            'status': 'failed',
            'info': info
        }
        self.write(res)

class GameDynamicRenderHandler(BaseHandler):
    def self_get(self):
        self.render("game_dynamic.html",title="动态更新",channel=conf.CHANNEL_PLATFORM_MAP)

class VersionUpdateHandler(BaseHandler):
    @asynchronous
    @gen.coroutine
    def self_post(self):
        update_info = json.loads(self.get_argument('updateInfo'))
        version = self.get_argument('version')
        try:
            for i in update_info:
                info=yield self.application.dbmgr.dynamicVersionUpdateDB.select(i,int(version))
                if info==None:
                    info=DynamicVersionUpdate()
                    info.channel=i
                    info.version=int(version)
                    info.url=update_info[i]['url']
                    info.size=int(update_info[i]['size'])
                    # info.comment=comment
                    info.note=update_info[i]['reason']
                    # info.svnVersion=int(svnVersion)
                    yield self.application.dbmgr.dynamicVersionUpdateDB.add(info)
                else:
                    info.url=update_info[i]['url']
                    info.size=int(update_info[i]['size'])
                    info.comment=comment
                    info.note=update_info[i]['reason']
                    # info.svnVersion=int(svnVersion)
                    yield self.application.dbmgr.dynamicVersionUpdateDB.update(info)
            action = 'success'
            self.application.redis.publish(redis_notify.get_platform_redis_notify_channel(platform), redis_notify.NOTIFY_TYPE_RELOAD_SERVER_VERSION)
        except:
            tuple = sys.exc_info()
            if tuple[1][0] == 1062:
                action = 'wrong channel-version'
            else:
                self.application.logger.info("dynamic_upload MarqueeManageHandler error")

        self.write(json.dumps({ 'action': action }))

class GameAddressRenderHandler(BaseHandler):
    @asynchronous
    @gen.coroutine
    def self_get(self):

        channels = conf.getChannelList()
        res=yield self.application.dbmgr.versionUpdateDB.select_all()
        info = {}
        for rec in res:
            info[rec.channel] = {
                'url': rec.url,
                'comment': rec.comments.decode('utf-8')
            }
        result = {
            'channels': json.dumps(channels),
            'info': json.dumps(info),
            'defaultChannelName':json.dumps(conf.getChannelNameMap()),
        }
        self.render("game_address.html",title="下载地址",result=result)

class GameAddressHandler(BaseHandler):
    @asynchronous
    @gen.coroutine
    def self_post(self):
        info=VersionUpdate()
        info.channel=int(self.get_argument('channel'))
        info.os=self.get_argument('os',0)
        info.comments = self.get_argument('comment')
        info.url = self.get_argument('gameUrl')

        yield self.application.dbmgr.versionUpdateDB.add(info)
        self.write(json.dumps({ 'action': 'success' }))

# class CacheDynamicHandler(BaseHandler):

#     def self_post(self):
#         self.application.redis.publish('centerserver_notify_queue', '{"type":9, "time":%s}'%(int(time.time()*1000)))
#         self.write(json.dumps({ 'action': 'success' }))

# #game test use
# class GameDeleteHandler(BaseHandler):

#     def self_post(self):
#         self.application.dynamic_db.truncate()
#         self.application.redis.publish('centerserver_notify_queue', '{"type":9, "time":%s}'%(int(time.time()*1000)))
#         self.write(json.dumps({ 'action': 'success' }))

#game server version update page
class GameServerVersionRenderHandler(BaseHandler):
    @asynchronous
    @gen.coroutine
    def self_get(self):

        channel_map = conf.getChannelPlatformMap()
        channels = conf.getChannelList()

        data = {}
        for i in channels:
            dynamicRec=yield self.application.dbmgr.dynamicVersionUpdateDB.select_max_version(i)
            if dynamicRec!= None:
                data[dynamicRec.channel]=dynamicRec.toJsonObj()

        versionData={}
        versionRecs= yield self.application.dbmgr.serverVersionDB.select_all()
        for rec in versionRecs:
            versionData[rec.platform]=rec.toJsonObj()
        res = {
            'data': data,
            'versionData': versionData,
            'channels': channel_map,
            'defaultChannelName':conf.getChannelNameMap(),

        }
        print(res)
        self.render("server_version_update.html",title="服务器版本号更新",result=json.dumps(res))

class ServerVersionHandler(BaseHandler):

    @asynchronous
    @gen.coroutine
    def self_post(self):
        version = int(self.get_argument('version'))
        platform=int(self.get_argument('platform'))

        sv=yield self.application.dbmgr.serverVersionDB.select(platform)
        sv.platform=platform
        sv.maxVesion=version/(1000*1000)
        sv.midVersion=(version/(1000) -sv.maxVesion*1000)
        sv.minVersion=version%1000
        yield self.application.dbmgr.serverVersionDB.update(sv)


        self.application.redis.publish(redis_notify.get_platform_redis_notify_channel(platform), redis_notify.NOTIFY_TYPE_RELOAD_SERVER_VERSION)
#       for i in a:
#           self.application.redis.publish('centerserver_notify_queue', '{"type":7, "time":%s}'%(int(time.time()*1000)))
#       self.application.redis.publish('centerserver_notify_queue', '{"type":9, "time":%s}'%(int(time.time()*1000)))

        # self.application.server_db.select_using(self.redis_push)

    # def redis_push(self,res):
    #     for i in res:
    #         self.application.redis.publish('notify_queue_%s_%s'%(i[0],i[2]), '{"type":7, "time":%s}'%(int(time.time()*1000)))

    #     self.application.redis.publish('centerserver_notify_queue', '{"type":7, "time":%s}'%(int(time.time()*1000)))
    #     self.application.redis.publish('centerserver_notify_queue', '{"type":9, "time":%s}'%(int(time.time()*1000)))

