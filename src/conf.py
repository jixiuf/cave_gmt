#  -*- coding:utf-8 -*-
__author__ = 'jixiufeng'

import json
import db.db_permissions
import db.dbmgr
from  db.dbtemplate import dbtemplate
from tornado.options import  options
import os.path
import etcd

AppName="cave"
CONFIG_DIR="/data/%s/config/"%(AppName)
etcdConfigJson=None
Etcd=etcd.Client(port=4001,host="127.0.0.1")
def getConfigJson(reload=False):
    global Etcd
    global AppName
    global etcdConfigJson
    if etcdConfigJson==None or reload:
        try:
            v =Etcd.get("/%s/config/%s_%s"%(AppName,str(options.mode),str(options.locale)))
            etcdConfigJson=json.loads(v.value)
            return etcdConfigJson
        except etcd.EtcdKeyNotFound:
            return None
    return etcdConfigJson

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
    value=getConfigJson()
    if value==None:
        return channels
    for k in value["channel"]:
        channels.append(int(k))
        channels.sort()
    return channels

def getChannelStrList():
    channels = []
    value=getConfigJson()
    if value==None:
        return channels
    for k in value["channel"]:
        channels.append(k)
        channels.sort()
    return channels


# key=渠道号，value =渠道名
def getChannelNameMap():
    value=getConfigJson()
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
    value=getConfigJson()
    if value==None:
        return addrs
    addrs.append(value["supervisor"][str(server)])
    return addrs

def getAllSupervisorAddrList(): # key=server ,value =["addr"]
    addrs=[]
    value=getConfigJson()
    if value==None:
        return addrs
    return value["supervisor"]

    # addrs={}                    # "ip":"ip","port":"port"
    # with open(getConfigFile()) as data_file:
    #     value = json.load(data_file)
    #     if value==None:
    #         return addrs
    #     if len(value["etcd"])==0:
    #         return addrs
    #     value["etcd"][0]=value["etcd"][0].replace("https://","")
    #     value["etcd"][0]=value["etcd"][0].replace("http://","")
    #     token=value["etcd"][0].split(":")
    #     addrs["ip"]=token[0]
    #     addrs["port"]=int(token[1])
    #     return addrs
def getRedisAddr():
    addrs={}                    # "ip":"ip","port":"port"
    value=getConfigJson()
    if value==None:
        return None
    addrs['host']= value["redis"]['addr'].split(':')[0]
    addrs['port'] = value["redis"]['addr'].split(':')[1]
    return addrs


def getProfileDBConfigMaster():
    value=getConfigJson()
    jsonData=value["profile_db_config"]
    user=jsonData["master"]['user']
    passwd=jsonData["master"]['passwd']
    host=jsonData["master"]['host']
    database=jsonData["master"]['database']
    port=jsonData["master"].get('port','')
    if port=="":
        port=3306
    if type(port)==str or type(port)==unicode :
        port=int(port)
    return dbtemplate.DBConfig(user,passwd,host,database,port)

def getEtcdAddr():
    addr=options.etcd.replace("https://","")
    addr=addr.replace("http://","")
    addr=addr.split(",")[0]
    addrs={}                    # "ip":"ip","port":"port"
    token=addr.split(":")
    addrs["ip"]=token[0]
    addrs["port"]=int(token[1])
    return addrs
def initEtcd():
    global Etcd
    etcdConfig=getEtcdAddr()
    Etcd=etcd.client.Client(port=etcdConfig["port"],host=etcdConfig["ip"], allow_reconnect=True)
    return Etcd

def getEtcd():
    global Etcd
    return Etcd




# [{u'processId': 1, u'startServerTime': 1465809520, u'ip': u'192.168.1.100', u'st': u'stopping', u'serverId': 1, u'port': u'2234', u'maxClientCount': 1000}
# , {u'processId': 2, u'startServerTime': 1465814775, u'ip': u'192.168.1.100', u'currentTcpCount': 250, u'st': u'running', u'serverId': 1, u'port': u'2235', u'maxClientCount': 1000}]
def getEtcdServerList(platform=1,server=1):
    list=[]
    global Etcd
    global AppName
    try:
        d =Etcd.read("/%s/logicmgr/%d/%d"%(AppName,int(platform),int(server)),recursive=True)
        for c in d.children:
            if c!=None and c.value!=None:
                list.append(json.loads(c.value))


        list.sort()
        return list
    except etcd.EtcdKeyNotFound:
        return list
def getEtcdServerProcess(platform=1,server=1,process=1):
    global Etcd
    global AppName
    try:
        v =Etcd.get("/%s/logicmgr/%d/%d/%d"%(AppName,int(platform),int(server),int(process)))
        return json.loads(v.value)
    except etcd.EtcdKeyNotFound:
        return None
def putEtcdServerProcess(platform=1,server=1,process=1,value={}):
    global Etcd
    global AppName
    Etcd.set("/%s/logicmgr/%d/%d/%d"%(AppName,int(platform),int(server),int(process)),json.dumps(value))


def isServerRunning(platform=1,server=1):
    servers=getEtcdServerList()
    running =False
    for server in servers:
        if server["st"]=="running":
            running=True
            break
    return running


