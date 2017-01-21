# -*- coding:utf-8 -*-
__author__ = 'jixiufeng'

import threading
import os.path
import sys
import signal
import traceback


import redis
import etcd
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

from tornado.ioloop import IOLoop

DBMgr=db.dbmgr.DBMgr()
Redis=redis.Redis()
Etcd=etcd.Client(port=4001,host="127.0.0.1")

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
            (r'/api/player_ban_uuid',PlayerBanUUIDHandler),
            (r'/api/reload_design_data' ,DesignReload),
            (r'/player/kick' ,KickUser),
            (r'/player/list' ,PlayerListHandler),
            (r'/player/del' ,DelUser),
            (r'/bi/player_bi_get' ,BIPlayerRender),
            (r'/bi/player_bi_post' ,BIPlayer),

            (r'/pay_order/list' ,PayOrderHandler),

            (r'/bugreport/get' ,BugReportHandler),


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




            (r'/server_mgr/server_mgr', ServerMgr),
            (r'/server_mgr/server_stopping', ServerStopping),
            (r'/server_mgr/server_switch', ServerSwitch),

            (r'/maintain/mgr', Maintain),
            (r'/maintain/mgr_post', Maintain),
            (r'/maintain/delete', MaintainDelete),
            (r'/broadcast/get', Broadcast),
            (r'/broadcast/post', Broadcast),

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
        global Etcd
        etcdConfig=conf.getEtcdAddr()
        Etcd=etcd.client.Client(port=etcdConfig["port"],host=etcdConfig["ip"], allow_reconnect=True)

        signal.signal(signal.SIGINT, self.handlerSignal)
        signal.signal(signal.SIGTERM, self.handlerSignal)
        self.keepRunning =True
        t=threading.Thread(target=self.keepReadFromRedis)
        t.start()
        # t.join()
        delay=utils.secondDiff("3:10:0") # 每天3:10执行
        self.biTimer=utils.RepeatTimer(delay,60*60*24,self.doMidNight)
        self.biTimer.start()



    def handlerSignal(self,signum, frame):
        self.keepRunning=False
        self.biTimer.cancel()
        sys.exit()
        os._exit()


    @gen.coroutine
    def doMidNight(self):
        self.logger.info("doMidNight")
        handler.zjh_player_bi.update_data()

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
            result=Redis.brpop("cave_redis_log",2) # timeout 2seconds
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
    with open(conf.getConfigFile()) as data_file:
        value = json.load(data_file)
        if value==None:
            return None
        redis_host = value["redis"]['addr'].split(':')[0]
        redis_port = value["redis"]['addr'].split(':')[1]
        return redis.Redis(host=redis_host, port=redis_port, db=0)

# [{u'processId': 1, u'startServerTime': 1465809520, u'ip': u'192.168.1.100', u'st': u'stopping', u'serverId': 1, u'port': u'2234', u'maxClientCount': 1000}
# , {u'processId': 2, u'startServerTime': 1465814775, u'ip': u'192.168.1.100', u'currentTcpCount': 250, u'st': u'running', u'serverId': 1, u'port': u'2235', u'maxClientCount': 1000}]
def getEtcdServerList(platform=1,server=1):
    list=[]
    global Etcd
    try:
        d =Etcd.read("/%s/logicmgr/%d/%d"%(conf.AppName,int(platform),int(server)),recursive=True)
        for c in d.children:
            if c!=None and c.value!=None:
                list.append(json.loads(c.value))


        list.sort()
        return list
    except etcd.EtcdKeyNotFound:
        return list
def getEtcdServerProcess(platform=1,server=1,process=1):
    global Etcd
    try:
        v =Etcd.get("/%s/logicmgr/%d/%d/%d"%(conf.AppName,int(platform),int(server),int(process)))
        return json.loads(v.value)
    except etcd.EtcdKeyNotFound:
        return None
def putEtcdServerProcess(platform=1,server=1,process=1,value={}):
    global Etcd
    Etcd.set("/%s/logicmgr/%d/%d/%d"%(conf.AppName,int(platform),int(server),int(process)),json.dumps(value))


def isServerRunning(platform=1,server=1):
    servers=getEtcdServerList()
    running =False
    for server in servers:
        if server["st"]=="running":
            running=True
            break
    return running


