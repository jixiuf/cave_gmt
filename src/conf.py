#  -*- coding:utf-8 -*-
__author__ = 'jixiufeng'

PLATFORM=1
PLATFORM_NAME="默认平台"
SERVER=1
SERVER_NAME="1服"
CHANNEL_IPHONECAKE=7
CHANNEL_PLATFORM_MAP={CHANNEL_IPHONECAKE:PLATFORM}
PLATFORM_CHANNEL_MAP={PLATFORM:[CHANNEL_IPHONECAKE]}
PLATFORM_SERVER_LIST={PLATFORM:
                      {SERVER:{
                          'channel_name': unicode(PLATFORM_NAME, 'utf-8'),
                          'server_name': unicode(SERVER_NAME, 'utf-8'),
                          'server_type': "dev",
                          'server_status': 1
                      }}}
