#  -*- coding:utf-8 -*-
__author__ = 'jixiufeng'

__author__ = 'jixiufeng'

from tornado import  gen
from handler.base import *
from tornado.web import asynchronous
import json
import app
import redis_notify

class DesignReload(BaseHandler):
    @asynchronous
    @gen.coroutine
    def self_get(self):
        app.Redis.publish(redis_notify.get_platform_redis_notify_channel(conf.PLATFORM), redis_notify.NOTIFY_TYPE_RELOAD_DESIGN_DATA)
        self.write(json.dumps({ 'action': 'success' }))
