#  -*- coding:utf-8 -*-
__author__ = 'jixiufeng'

import json
from tornado.options import  options

AppName="zjh"
CONFIG_DIR="/data/%s/config/"%(AppName)


DYNAMIC_USER='dynamicUser'
DYNAMIC_PASSWORD='dynamicPassword'

QINIU_ACCESS_KEY = '4V9Hf9mJb-4oXbM5H_kqXEuV_5aI4v6S1_LaVLKY'
QINIU_SECRET_KEY = 'BX6p6vGQWa-6VuWf6eikNKYN4P3RG_L4H5Sig_vh'
QINIU_SECRET_BUCKET_NAME = 'thgmtools'


PLATFORM=1
PLATFORM_NAME="默认平台"
SERVER=1
SERVER_NAME="1服"
CHANNEL_IPHONECAKE=7
CHANNEL_PLATFORM_MAP={str(CHANNEL_IPHONECAKE):PLATFORM}
# PLATFORM_CHANNEL_MAP={CHANNEL_IPHONECAKE:PLATFORM}
PLATFORM_SERVER_LIST={PLATFORM:
                      {SERVER:{
                          'platform_name': unicode(PLATFORM_NAME, 'utf-8'),
                          'server_name': unicode(SERVER_NAME, 'utf-8'),
                          'server_type': "dev",
                          'server_status': 1
                      }}}
DEFAULT_CHANNEL_NAME = {
    '6': 'app store',
    '7': 'iphonecake',
}

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


