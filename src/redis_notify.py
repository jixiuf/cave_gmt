#  -*- coding:utf-8 -*-
__author__ = 'jixiufeng'

import conf

REDIS_NOTIFY_CHANNEL="%s_notify_channel"%(conf.AppName)

# 通知指定的服
def get_server_redis_notify_channel(platform,server):
    return "%s_%d_%d"%(REDIS_NOTIFY_CHANNEL,int(platform),int(server))
# 全平台通知
def get_platform_redis_notify_channel(platform):
    return "%s_%d"%(REDIS_NOTIFY_CHANNEL,int(platform))
# 通知类型
NOTIFY_TYPE_RELOAD_SERVER_VERSION='{"type":1,"accept_type":"center|auth|logic"}'
NOTIFY_TYPE_RELOAD_MAINTAIN='{"type":6,"accept_type":"center"}'
NOTIFY_TYPE_RELOAD_MAIL='{"type":1000,"accept_type":"logic","uin":"0"}'
