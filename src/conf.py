#  -*- coding:utf-8 -*-
__author__ = 'jixiufeng'

import json
import db.db_permissions
from tornado.options import  options

AppName="zjh"
CONFIG_DIR="/data/%s/config/"%(AppName)

initPermissionLevel=[db.db_permissions.NewGmToolAccountPermissionLevel(1,"管理员",''),
db.db_permissions.NewGmToolAccountPermissionLevel(0,"浏览权限",'/ping,/game/address,/game/update,/gmt/manage')]

DYNAMIC_USER='najaplus'
DYNAMIC_PASSWORD='qHcdGfE6TH'

QINIU_ACCESS_KEY = 'diDp_FZuFNaxi8eX2qKwIRvRewY0RfQced3WQcIt'
QINIU_SECRET_KEY = 'WA9qohA7cAaMQDwr4mT_AG2TzxqXXNzNCbvXokaJ'
QINIU_SECRET_BUCKET_NAME = 'najaplus'


PLATFORM=1
PLATFORM_NAME="默认平台"

def getChannelList():
    channels = []
    with open("%s/%s.json"%(CONFIG_DIR,options.mode)) as data_file:
        value = json.load(data_file)
        if value==None:
            return channels
        for k in value["channel"]:
            channels.append(int(k))
    channels.sort()
    return channels

# key=渠道号，value =渠道名
def getChannelNameMap():
    with open("%s/%s.json"%(CONFIG_DIR,options.mode)) as data_file:
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


