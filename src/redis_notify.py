#  -*- coding:utf-8 -*-
__author__ = 'jixiufeng'

import conf

REDIS_NOTIFY_CHANNEL="%s_notify_channel"%(conf.AppName)

# 通知指定的服的指定进程
def get_process_redis_notify_channel(platform,server,process):
    return "%s_%d_%d_%d"%(REDIS_NOTIFY_CHANNEL,int(platform),int(server),int(process))

# 通知指定的服
def get_server_redis_notify_channel(platform,server):
    return "%s_%d_%d"%(REDIS_NOTIFY_CHANNEL,int(platform),int(server))
# 全平台通知
def get_platform_redis_notify_channel(platform):
    return "%s_%d"%(REDIS_NOTIFY_CHANNEL,int(platform))
# 通知类型
NOTIFY_TYPE_RELOAD_SERVER_VERSION='{"type":1,"accept_type":"center|auth|logic"}'
NOTIFY_TYPE_RELOAD_MAINTAIN='{"type":6,"accept_type":"center|auth"}'
NOTIFY_TYPE_RELOAD_BAN='{"type":8,"accept_type":"logic|auth|center"}'
NOTIFY_TYPE_RELOAD_MAIL='{"type":14,"accept_type":"logic","uin":"%s"}'
NOTIFY_TYPE_RELOAD_MONEY='{"type":1001,"accept_type":"logic","uin":"%s"}'
NOTIFY_TYPE_DESKINFO='{"type":1002,"accept_type":"logic","uin":"%s"}'
NOTIFY_TYPE_RELOAD_DESIGN_DATA='{"type":9,"accept_type":"logic"}'
NOTIFY_TYPE_SERVER_STOPPING='{"type":11,"accept_type":"logic"}'
NOTIFY_TYPE_SERVER_STOP='{"type":15,"accept_type":"logic"}'
NOTIFY_TYPE_SERVER_EXEC='{"type":16,"accept_type":"logic","content":"%s"}'
NOTIFY_TYPE_FREE_OS_MEM='{"type":19,"accept_type":"center|auth|logic"}'
NOTIFY_TYPE_RELOAD_NOTICE='{"type":12,"accept_type":"center|auth|logic"}'
NOTIFY_TYPE_BROADCAST='{"type":100,"accept_type":"logic","content":%s}'
NOTIFY_TYPE_MARQUEE='{"type":18,"accept_type":"logic"}'
NOTIFY_TYPE_GAMECONFIG_RELOAD='{"type":17,"accept_type":"logic"}'
NOTIFY_TYPE_KICK_USER='{"type":13,"accept_type":"logic","uin":"%s"}'
NOTIFY_TYPE_RELOAD_DAY7CONFIG='{"type":20,"accept_type":"logic"}'
NOTIFY_TYPE_CLEAR_RANK_USER='{"type":1003,"accept_type":"logic","uin":"%s"}'
