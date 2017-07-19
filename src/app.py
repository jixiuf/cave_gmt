# -*- coding:utf-8 -*-
__author__ = 'jixiufeng'

import threading
import os.path
import sys
import signal
import traceback


import redis
import tornado.web
import conf
from tornado.options import  options
from logger import *
import db.dbmgr

import handler
from handler.pay_order import *
from handler.broadcast import *
from handler.notice import *
from handler.ping import PingHandler
from handler.login import *
from handler.account import *
from handler.present_pack import *
from handler.maintain import *
from handler.server_mgr import *
from handler.version import *
from handler.award import *
from handler.mail import *
from handler.player import *
from handler.design  import *
from handler.player_bi import *
from handler.bugreport import *
from handler.gameconfig import *
from handler.rank import *
from handler.code import *
from handler.bi import *
from handler.day7config import *
from handler.weekmonth import *
from handler.award_time import *
from handler.award_festival import *

from tornado.ioloop import IOLoop

DBMgr=db.dbmgr.DBMgr()
Redis=redis.Redis()
Logger=None

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
            (r'/api/player_unban',PlayerUnBanHandler),
            (r'/api/player_ban_chat',PlayerBanChatHandler),
            (r'/api/player_unban_chat',PlayerUnBanChatHandler),
            (r'/api/player_ban_uuid',PlayerBanUUIDHandler),
            (r'/api/reload_design_data' ,DesignReload),
            (r'/player/kick' ,KickUser),
            (r'/player/list' ,PlayerListHandler),
            (r'/player/del' ,DelUser),
            (r'/bi/player_bi_get' ,BIPlayerRender),
            (r'/bi/player_bi_post' ,BIPlayer),
            (r'/bi/active_player' ,BIActivePlayer),
            (r'/bi/active_player_post' ,BIActivePlayer),

            (r'/bi/rank' ,Rank),
            (r'/bi/rank_post' ,Rank),
            (r'/currency_change/list' ,BICurrencyChangeHandler),
            (r'/item_change/list' ,BIItemChangeHandler),
            (r'/gear_got/list' ,BIGearGotHandler),
            (r'/gear_fortify/list' ,BIGearFortifyHandler),
            (r'/gear_refine/list' ,BIGearRefineHandler),
            (r'/levelup/list' ,BILevelUpHandler),
            (r'/partner_got/list' ,BIPartnerGotHandler),
            (r'/bi/GuideActorDestroy' ,BIGuideHandle),
            (r'/bi/stage' ,BIStageHandler),
            (r'/bi/level' ,BILevelHandler),
            (r'/bi/dead' ,BIDeadHandler),
            (r'/bi/skill' ,BISkillHandler),





            (r'/pay_order/list' ,PayOrderHandler),
            (r'/pay_order/stat' ,PayOrderBIHandler),


            (r'/bugreport/get' ,BugReportHandler),

            (r'/gameconfig/put' ,GameConfigHandler),
            (r'/gameconfig/get' ,GameConfigHandler),


            (r'/ping', PingHandler),
            (r'/', LoginHandler),
            (r'/logout', LogoutHandler),

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

            (r'/code/get', CodeMgr),
            (r'/code/put', CodeMgr),
            (r'/code/list', CodeList),
            (r'/code/del', CodeDel),
            (r'/day7config/list', Day7Config),
            (r'/day7config/put', Day7Config),
            (r'/weekmonth/list', WeekMonth),
            (r'/weekmonth/put', WeekMonth),
            (r'/award_time/list', AwardTime),
            (r'/award_time/put', AwardTime),

            (r'/award_festival/list',FestivalConfig),
            (r'/award_festival/put', FestivalConfig),



            (r'/server_mgr/server_mgr', ServerMgr),
            (r'/server_mgr/server_stopping', ServerStopping),
            (r'/server_mgr/server_stop', ServerStop),
            (r'/server_mgr/server_switch', ServerSwitch),
            (r'/server_mgr/server_exec', ServerExec),
            (r'/server_mgr/whiteip_delete', WhiteIPDelete),
            (r'/server_mgr/whiteip_add', WhiteIPAdd),
            (r'/server_mgr/prof', ProfHandler),


            (r'/maintain/mgr', Maintain),
            (r'/maintain/mgr_post', Maintain),
            (r'/maintain/delete', MaintainDelete),
            (r'/broadcast/get', Broadcast),
            (r'/broadcast/post', Broadcast),
            (r'/marquee/delete', MarqueeDelete),


            (r'/notice/get', NoticeManageRenderHandler),
            (r'/notice/add', NoticeAddRenderHandler),
            (r'/notice/edit', NoticeEditRenderHandler),
            (r'/api/notice/info', NoticeInfoHandler),
            (r'/api/notice/add/info', NoticeAddInfoHandler),
            (r'/api/notice/add', NoticeAddHandler),
            (r'/api/notice/update', NoticeUpdateHandler),


            (r'/game/update', GameUpdateRenderHandler),
            # (r'/game/dynamic', GameDynamicRenderHandler),
            (r'/game/address', GameAddressRenderHandler),

            (r'/api/game/dynamic', DynamicHandler),
            (r'/api/version/update', VersionUpdateHandler),
            (r'/api/game/address', GameAddressHandler),
            (r'/api/game/dynamic_package_generator', DynamicPackageGeneratorHandler),

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
        global Logger
        Logger=self.logger

        # self.channel_logger = get_logger('channel',os.path.join(options.data_dir,'channel.log'))
        self.gm_logger = get_logger('gminfo',os.path.join(options.data_dir,'gminfo.log'))
        conf.initEtcd()
        global DBMgr
        DBMgr.init(options.mode,options.locale)
        DBMgr.load()
        global Redis
        Redis =initRedisConfig(options.mode)
        # global Etcd
        # etcdConfig=conf.getEtcdAddr()
        # Etcd=etcd.client.Client(port=etcdConfig["port"],host=etcdConfig["ip"], allow_reconnect=True)

        signal.signal(signal.SIGINT, self.handlerSignal)
        signal.signal(signal.SIGTERM, self.handlerSignal)
        self.keepRunning =True

        # t=threading.Thread(target=self.keepReadFromRedis)
        # t.start()

        # t.join()
        delay=utils.secondDiff("3:10:0") # 每天3:10执行
        self.biTimer=utils.RepeatTimer(delay,60*60*24,self.doMidNight)
        self.biTimer.start()


    def stop(self):
        self.keepRunning=False
        self.biTimer.cancel()
        sys.exit()
        os._exit()


    def handlerSignal(self,signum, frame):
        self.keepRunning=False
        self.biTimer.cancel()
        sys.exit()
        os._exit()


    @gen.coroutine
    def doMidNight(self):
        global Redis
        self.logger.info("doMidNight")
        conf.getConfigJson(True)
        handler.player_bi.update_data()
        Redis.publish(redis_notify.get_platform_redis_notify_channel(conf.PLATFORM), redis_notify.NOTIFY_TYPE_FREE_OS_MEM)

        last2Month=datetime.now()+ timedelta(days=-62)

        sql="delete from LoginLog where  Time<'%s' "%(last2Month.strftime("%Y-%m-%d %H:%M:%S"))
        yield app.DBMgr.getGMToolDB().execSql(sql)
        self.logger.info(sql)

        # sql="delete from ZJHDeskEnterLog where  Time<'%s' "%(last2Month.strftime("%Y-%m-%d %H:%M:%S"))
        # yield app.DBMgr.getGMToolDB().execSql(sql)
        # self.logger.info(sql)

        # sql="delete from AssetsLog where  Time<'%s' "%(last2Month.strftime("%Y-%m-%d %H:%M:%S"))
        # yield app.DBMgr.getGMToolDB().execSql(sql)
        # self.logger.info(sql)




    def keepReadFromRedis(self):

        global Redis
        global DBMgr
        while self.keepRunning:
            result=Redis.brpop(conf.AppName+"_redis_log",2) # timeout 2seconds
            if result!=None:
                # result[0]=="key"
                # result[1]=="value"
                self.logger.info(result[1])

                try:
                    # e=yield DBMgr.getGMToolDB().execSql(result[1])
                    DBMgr.getGMToolDB().execSql(result[1])
                except Exception, error:
                    self.logger.warning('errormsg\t%s' % (str(error),))
                    self.logger.warning('errortrace\t%s' % (str(traceback.format_exc()),))


        print("keepReadFromRedis_exit")



    def close(self):
        close_logger(self.logger)
        close_logger(self.gm_logger)


def initRedisConfig(mode):
    addr=conf.getRedisAddr()
    return redis.Redis(host=addr['host'], port=addr['port'], db=0)
