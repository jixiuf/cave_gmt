#  -*- coding:utf-8 -*-
__author__ = 'jixiufeng'

from base_handler import *
from tornado.web import asynchronous
# from utils import get_channel_map
import sys
import time
from conf import *

class GameUpdateRenderHandler(BaseHandler):
    @asynchronous
    def self_get(self):
        self.render("game_update.html",title="动态更新",result=json.dumps(PLATFORM_SERVER_LIST))

class GameDynamicRenderHandler(BaseHandler):
    def self_get(self):
        self.render("game_dynamic.html",title="动态更新",channel=CHANNEL_PLATFORM_MAP)

class VersionUpdateHandler(BaseHandler):

    def self_post(self):
        update_info = json.loads(self.get_argument('updateInfo'))
        version = self.get_argument('version')
        try:
            for i in update_info:
                self.application.dynamic_db.add_by_channel(i,version,update_info[i]['url'],update_info[i]['size'],update_info[i]['reason'])
            action = 'success'
        except:
            tuple = sys.exc_info()
            if tuple[1][0] == 1062:
                action = 'wrong channel-version'
            else:
                self.application.logger.info("dynamic_upload MarqueeManageHandler error")

        self.write(json.dumps({ 'action': action }))

class GameAddressRenderHandler(BaseHandler):
    @asynchronous
    def self_get(self):
        channel_map = json.loads(get_channel_map())
        channels = []
        for i in channel_map:
            if i == '112':
                continue
            channels.append(int(i))
        channels.sort()
        self.channels = channels
        self.application.game_addres_db.select(self.resolve)

    def resolve(self,res):
        info = {}
        for i in res:
            channel = int(i[0])
            url = i[1]
            comment = i[2].decode('utf-8')
            info[channel] = {
                'url': url,
                'comment': comment
            }
        result = {
            'channels': json.dumps(self.channels),
            'info': json.dumps(info)
        }
        self.render("game_address.html",title="下载地址",result=result)

class GameAddressHandler(BaseHandler):

    def self_post(self):
        channel = self.get_argument('channel')
        game_url = self.get_argument('gameUrl')
        comment = self.get_argument('comment')
        self.application.game_addres_db.add_by_channel(channel,game_url,comment)
        self.write(json.dumps({ 'action': 'success' }))

class CacheDynamicHandler(BaseHandler):

    def self_post(self):
        self.application.redis.publish('centerserver_notify_queue', '{"type":9, "time":%s}'%(int(time.time()*1000)))
        self.write(json.dumps({ 'action': 'success' }))

#game test use
class GameDeleteHandler(BaseHandler):

    def self_post(self):
        self.application.dynamic_db.truncate()
        self.application.redis.publish('centerserver_notify_queue', '{"type":9, "time":%s}'%(int(time.time()*1000)))
        self.write(json.dumps({ 'action': 'success' }))

#game server version update page
class GameServerVersionRenderHandler(BaseHandler):
    @asynchronous
    def self_get(self):
        self.count = 0
        self.res_number = 0
        self.result = {}

        self.application.server_version_db.select_all(self.get_version_data)

        channel_map = json.loads(get_channel_map())
        self.channel_map = channel_map
        channels = []
        for i in channel_map:
#           if i == '112':
#               continue
            channels.append(int(i))
        channels.sort()
        self.channels = channels

        for i in self.channels:
            self.application.dynamic_db.select(i,self.get_dynamic_data)

    def get_version_data(self, res):
        self.res_number += 1
        data = {}
        for i in res:
            data[i[0]] = {
                'comments': i[1],
                'max_version': i[2],
                'mid_version': i[3],
                'min_version': i[4],
                'show_version': i[5]
            }

        self.version_data = data
        self.check_res()

    def get_dynamic_data(self, res):
        self.count += 1
        data = {}
        if len(res):
            res = res[0]

            data['channel'] = res[0]
            data['version'] = res[1]
            data['url'] = res[2]
            data['size'] = res[3]
            data['comment'] = res[4]
            data['note'] = res[5]
            data['svnVersion'] = res[6]

            self.result[data['channel']] = data

        if self.count == len(self.channels):
            self.res_number += 1
            self.check_res()

    def check_res(self):
        if self.res_number == 2:
            self.show()

    def show(self):
        res = {
            'data': self.result,
            'versionData': self.version_data,
            'channels': self.channel_map
        }
        self.render("server_version_update.html",title="服务器版本号更新",result=json.dumps(res))

class ServerVersionHandler(BaseHandler):

    def self_post(self):
        version = self.get_argument('version')
        show_version = self.get_argument('showVersion')
        platform = self.get_argument('platform')

        self.application.server_version_db.update_version(version,show_version,platform)
#       self.application.redis.publish('centerserver_notify_queue', '{"type":7, "time":%s}'%(int(time.time()*1000)))
#       for i in a:
#           self.application.redis.publish('centerserver_notify_queue', '{"type":7, "time":%s}'%(int(time.time()*1000)))
#       self.application.redis.publish('centerserver_notify_queue', '{"type":9, "time":%s}'%(int(time.time()*1000)))

        self.application.server_db.select_using(self.redis_push)

    def redis_push(self,res):
        for i in res:
            self.application.redis.publish('notify_queue_%s_%s'%(i[0],i[2]), '{"type":7, "time":%s}'%(int(time.time()*1000)))

        self.application.redis.publish('centerserver_notify_queue', '{"type":7, "time":%s}'%(int(time.time()*1000)))
        self.application.redis.publish('centerserver_notify_queue', '{"type":9, "time":%s}'%(int(time.time()*1000)))

#game dynamic
class DynamicHandler(tornado.web.RequestHandler):

    def post(self):
        self.permission_verify()

    def permission_verify(self):
        user = self.get_argument('user', None)
        password = self.get_argument('password', None)

        channel = self.get_argument('channel', None)
        version = self.get_argument('version', None)
        url = self.get_argument('url', None)
        size = self.get_argument('size', None)
        comment = self.get_argument('comment', None)
        note = self.get_argument('note', None)
        svnVersion = self.get_argument('svnVersion', None)

        if user == DYNAMIC_USER and password == DYNAMIC_PASSWORD:
            if channel == None or version == None or url == None or size == None or comment == None or note == None or svnVersion == None:
                self.failed('need 8 arguments')
            else:
                self.success(channel,version,url,size,comment,note,svnVersion)
        else:
            self.failed('verification dose note pass')

    def success(self,channel,version,url,size,comment,note,svnVersion):
        self.application.dynamic_db.add_channel_dynamic(channel,version,url,size,comment,note,svnVersion)
        res = {
            'status': 'success'
        }
        self.write(res)

    def failed(self, info):
        res = {
            'status': 'failed',
            'info': info
        }
        self.write(res)
