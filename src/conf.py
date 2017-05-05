#  -*- coding:utf-8 -*-
__author__ = 'jixiufeng'

import json
import db.db_permissions
from tornado.options import  options
import os.path

AppName="cave"
CONFIG_DIR="/data/%s/config/"%(AppName)
def getConfigFile():
    filename="%s%s_%s.json"%(CONFIG_DIR,options.mode,options.locale)
    if not os.path.exists(filename)   :
        filename="%s%s.json"%(CONFIG_DIR,options.mode)
    return filename

REDIS_MAX_SCORE = 9007199254740992
ClientSVNResourcesURL='svn://svn.najaplus.com/game2/dev/client/cocos2d-x-2.2.6/projects/client/Resources'

initPermissionLevel=[db.db_permissions.NewGmToolAccountPermissionLevel(1,"管理员",''),
db.db_permissions.NewGmToolAccountPermissionLevel(0,"浏览权限",
                                                  ','.join(['/ping',
                                                            '/logout',
                                                            '/game/address',
                                                            '/account/manage',
                                                            '/player/search',
                                                            '/api/player_search',
                                                            '/pay_order/list',
                                                            '/assets_log/list',
                                                            '/player/deskinfo',
                                                            'game/server_version_update',
                                                            '/bi/player_bi_get' ,
                                                            '/bi/player_bi_post',
                                                            '/maintain/mgr',
                                                            '/award/sub_id_list',
                                                            '/award/id_list',])
)]

DYNAMIC_USER='najaplus'
DYNAMIC_PASSWORD='qHcdGfE6TH'

QINIU_ACCESS_KEY = 'AYwnALpeN5pT5c--NG2sjbnUNP1ey9px4SZAFD-3'
QINIU_SECRET_KEY = 'jLLvul-joXk6ALMCNkJVnxexsi7yMa7U--dJjwnU'
QINIU_SECRET_BUCKET_NAME = 'najaplus'


PLATFORM=1
PLATFORM_NAME="默认平台"

def getChannelList():
    channels = []
    with open(getConfigFile()) as data_file:
        value = json.load(data_file)
        if value==None:
            return channels
        for k in value["channel"]:
            channels.append(int(k))
            channels.sort()
    return channels

def getChannelStrList():
    channels = []
    with open(getConfigFile()) as data_file:
        value = json.load(data_file)
        if value==None:
            return channels
        for k in value["channel"]:
            channels.append(k)
            channels.sort()
    return channels


# key=渠道号，value =渠道名
def getChannelNameMap():
    with open(getConfigFile()) as data_file:
        value = json.load(data_file)
        if value==None:
            return {}
        return value["channel"]

#key=channelid value=platformid
def getChannelPlatformMap():
    ret ={}
    m=getChannelNameMap()
    for k in m:
        ret[str(k)]=PLATFORM
    return ret


def getSupervisorAddrList(server="1"):
    addrs=[]
    with open(getConfigFile()) as data_file:
        value = json.load(data_file)
        if value==None:
            return addrs
        addrs.append(value["supervisor"][str(server)])
    return addrs

def getAllSupervisorAddrList(): # key=server ,value =["addr"]
    addrs=[]
    with open(getConfigFile()) as data_file:
        value = json.load(data_file)
        if value==None:
            return addrs
        return value["supervisor"]
def getEtcdAddr():
    addrs={}                    # "ip":"ip","port":"port"
    with open(getConfigFile()) as data_file:
        value = json.load(data_file)
        if value==None:
            return addrs
        if len(value["etcd"])==0:
            return addrs
        value["etcd"][0]=value["etcd"][0].replace("https://","")
        value["etcd"][0]=value["etcd"][0].replace("http://","")
        token=value["etcd"][0].split(":")
        addrs["ip"]=token[0]
        addrs["port"]=int(token[1])
        return addrs

