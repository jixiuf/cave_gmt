# -*- coding:utf-8 -*-
__author__ = 'jixiufeng'

import os.path


import tornado.web
from tornado.options import  options
from logger import *
import db.dbmgr
import ping
from  login_handler import *
from account_handler import *

from tornado.ioloop import IOLoop


class Application(tornado.web.Application):
    """
    Application
    """

    def __init__(self):

        handlers = [
            (r'/ping', ping.PingHandler),
            (r'/', LoginHandler),
            (r'/gmt/register', RegistrationRenderHandler),
            (r'/gmt/manage', ManageRenderHandler),
            (r'/api/account/create', AccountCreateHandler),
            (r'/api/account/update_level', AccountLevelHandler),
            (r'/api/account/get_permission_level', PerssionLevelHandler),



        ]

        settings = dict(
            gzip = True,
            template_path = os.path.join(os.path.split(__file__)[0], '../template'),
            static_path = os.path.join(os.path.split(__file__)[0], '../template', '../static'),
            cookie_secret = 'S6Bp2cVjSAGFXDZqyOh+hfn/fpBnaEzFh22IVmCsVJQ=',
            login_url = '/',
        )

        tornado.web.Application.__init__(self, handlers, **settings)
        self.logger = get_logger('server', os.path.join(options.data_dir, 'server.log'))
        # self.channel_logger = get_logger('channel',os.path.join(options.data_dir,'channel.log'))
        self.gm_logger = get_logger('gminfo',os.path.join(options.data_dir,'gminfo.log'))


        # redis_host = redis_config().split(':')[0]
        # redis_port = redis_config().split(':')[1]
        # self.redis = redis.Redis(host=redis_host, port=redis_port, db=0)
        self.dbmgr=db.dbmgr.DBMgr(options.mode)
        self.dbmgr.load()



    def close(self):
        close_logger(self.logger)
        close_logger(self.gm_logger)


