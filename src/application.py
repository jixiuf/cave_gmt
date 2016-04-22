# -*- coding:utf-8 -*-
__author__ = 'jixiufeng'

import os.path


import redis
import tornado.web
from conf import *
from tornado.options import  options
from logger import *
import db.dbmgr
import ping

from  login_handler import *
from account_handler import *
from present_pack import *
from maintain import *
from version_handle import *

from tornado.ioloop import IOLoop


class Application(tornado.web.Application):
    """
    Application
    """

    def __init__(self):

        handlers = [
            (r'/ping', ping.PingHandler),
            (r'/', LoginHandler),
            (r'/account/register', RegistrationRenderHandler),
            (r'/account/manage', ManageRenderHandler),
            (r'/api/account/create', AccountCreateHandler),
            (r'/api/account/delete', AccountCreateHandler),
            (r'/api/account/update_level', AccountLevelHandler),

            (r'/present_pack/list', PresentPackList),
            (r'/present_pack/show_or_hide', PresentPackHideShow),
            (r'/present_pack/add', PresentPackAdd),
            (r'/present_pack/id_list', PresentPackIdList),

            (r'/maintain/mgr', Maintain),
            (r'/maintain/delete', MaintainDelete),

            (r'/game/update', GameUpdateRenderHandler),
            # (r'/game/dynamic', GameDynamicRenderHandler),
            (r'/game/address', GameAddressRenderHandler),

            (r'/api/game/dynamic', DynamicHandler),
            (r'/api/version/update', VersionUpdateHandler),
            (r'/api/game/address', GameAddressHandler),

            (r'/game/server_version_update', GameServerVersionRenderHandler),
            (r'/api/server/version', ServerVersionHandler),
            # (r'/game/server_version_update_notice', ServerMgrUpdateServerVerionNoticeRenderHandler),

            (r'/api/qiniu/uptoken', QiniuUptokenHandler),


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


        self.dbmgr=db.dbmgr.DBMgr(options.mode,options.locale)
        self.dbmgr.load()
        self.redis=self.initRedisConfig(options.mode)



    def close(self):
        close_logger(self.logger)
        close_logger(self.gm_logger)


    def initRedisConfig(self,mode):
        with open(CONFIG_DIR+"%s.json"%(mode)) as data_file:
            value = json.load(data_file)
            if value==None:
                return None
            redis_host = value["redis"]['addr'].split(':')[0]
            redis_port = value["redis"]['addr'].split(':')[1]
            return redis.Redis(host=redis_host, port=redis_port, db=0)

