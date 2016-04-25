# -*- coding:utf-8 -*-
__author__ = 'jixiufeng'

import os.path


import redis
import tornado.web
import conf
from tornado.options import  options
from logger import *
import db.dbmgr

import handler
from handler.ping import PingHandler
from handler.login import *
from handler.account import *
from handler.present_pack import *
from handler.maintain import *
from handler.version import *
from handler.award import *
from handler.mail import *
from handler.player import *

from tornado.ioloop import IOLoop

DBMgr=db.dbmgr.DBMgr()
Redis=redis.Redis()

class Application(tornado.web.Application):
    """
    Application
    """

    def __init__(self):

        handlers = [
            (r'/player/search' ,PlayerSearchRenderHandler),
            (r'/api/player_search' ,PlayerSearchHandler),
            (r'/api/player_info_update',PlayerInfoUpdateHandler),
            (r'/api/player_ban',PlayerBanHandler),


            (r'/ping', PingHandler),
            (r'/', LoginHandler),
            (r'/account/register', AccountRegistrationRenderHandler),
            (r'/account/manage', AccountManageRenderHandler),
            (r'/api/account/create', AccountCreateHandler),
            (r'/api/account/delete', AccountCreateHandler),
            (r'/api/account/update_level', AccountLevelHandler),

            (r'/present_pack/list', PresentPackList),
            (r'/present_pack/show_or_hide', PresentPackHideShow),
            (r'/present_pack/add', PresentPackAdd),

            (r'/award/sub_id_list', AwardSubIdList),
            (r'/award/id_list', AwardIdList),

            (r'/mail/edit', MailEdit),
            (r'/mail/draft_list', MailDraftList),
            (r'/mail/draft_send', MailDraftSend),
            (r'/mail/draft_delete', MailDraftDelete),





            (r'/maintain/mgr', Maintain),
            (r'/maintain/mgr_post', Maintain),
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
        global DBMgr
        DBMgr.init(options.mode,options.locale)
        DBMgr.load()
        global Redis
        Redis =initRedisConfig(options.mode)





    def close(self):
        close_logger(self.logger)
        close_logger(self.gm_logger)


def initRedisConfig(mode):
    with open(conf.CONFIG_DIR+"%s.json"%(mode)) as data_file:
        value = json.load(data_file)
        if value==None:
            return None
        redis_host = value["redis"]['addr'].split(':')[0]
        redis_port = value["redis"]['addr'].split(':')[1]
        return redis.Redis(host=redis_host, port=redis_port, db=0)

