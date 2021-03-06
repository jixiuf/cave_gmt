#  -*- coding:utf-8 -*-
__author__ = 'jixiufeng'


from datetime import datetime, timedelta
import utils
import redis_notify
from handler.base import BaseHandler
from tornado.web import asynchronous
from tornado import  gen
import app
import json
import conf
import time
import subprocess
from tornado.process import Subprocess

class ServerMgr(BaseHandler):
    @asynchronous
    @gen.coroutine
    def self_get(self):
        def mapWhiteIPRow(row):
            whiteIP={}
            whiteIP['id']=row[0]
            whiteIP['ip']=row[1]
            return  whiteIP

        conf.getConfigJson(True) # reload config json
        serverIdList= app.DBMgr.get_all_server_id()

        cmds=[]
        redisAddrs=conf.getRedisAddr()
        cmds.append(r"echo 'keys *'|redis-cli -h %s -p %s"%(redisAddrs['host'],redisAddrs['port']))
        cmds.append(r"echo 'PUBLISH cave_notify_channel_1_1_1 %s '|redis-cli -h %s -p %s"%( "{\"type\":3}", redisAddrs['host'],redisAddrs['port']))

        cmds.append(r"echo 'get %s_cmd_output'|redis-cli -h %s -p %s"%(conf.AppName, redisAddrs['host'],redisAddrs['port']))

        profileDBConfig=conf.getProfileDBConfigMaster()
        cmds.append(r'echo "show tables"|mysql -h %s -u%s -p"%s" %s'%(profileDBConfig.host,profileDBConfig.user,profileDBConfig.passwd,profileDBConfig.database))
        cmds.append("ps -ef |grep ")
        cmds.append("ps -auxw --sort=rss|tac")
        cmds.append("ps -auxw --sort=%cpu|tac")
        cmds.append("tail  -n 100 data/server.log")
        cmds.append("tail  -n 100 data/gminfo.log")
        cmds.append("tail  -n 100 data/tornado.log")
        cmds.append("ll /tmp/tmp_cave_gmt/")
        cmds.append("md5sum /tmp/tmp_cave_gmt/cave_gmt.tgz ")
        cmds.append("md5sum /data/cave/bin/cave")
        cmds.append("cat  /data/cave/bin/get-last-cave-zh.sh")
        cmds.append("sh  /data/cave/bin/get-last-cave-zh.sh")
        cmds.append("llh /data/cave/config/logs/cave_logic")
        cmds.append("ll  ~/tmp/cave.zh.bin.tar.lzma ")
        cmds.append("/data/supervisor/reload.sh   /data/supervisor/supervisord.conf")
        cmds.append("python -m SimpleHTTPServer 3009")
        cmds.append("echo 'svg >a.svg'|go tool pprof ./cave heap.prof")
        cmds.append("echo 'svg >a.svg'|go tool pprof -alloc_space ./cave heap.prof")
        cmds.append("echo 'svg >a.svg'|go tool pprof -inuse_space ./cave heap.prof")
        cmds.append("echo 'svg >a.svg'|go tool pprof -inuse_objects ./cave heap.prof")
        cmds.append("echo 'svg >a.svg'|go tool pprof -alloc_objects ./cave heap.prof")



        now=datetime.now()
        cmds.append(now.strftime("llh /data/cave/config/logs/cave_logic |grep %m.%d"))
        cmds.append(now.strftime("llh /data/cave/config/logs/cave_auth |grep %m.%d"))
        cmds.append(now.strftime("supervisorctl -c /data/supervisor/supervisord.conf start cave:cave_zh_4 2>&1"))
        cmds.append("etcdctl ls / --recursive")
        cmds.append("etcdctl get")
        cmds.append("etcdctl member list")







        maintainList=yield app.DBMgr.maintainDB.select_all()
        whiteIPList=yield app.DBMgr.getProfileDB().query("select Id,Content from ban where Type=5 order by StartBanTime desc",mapWhiteIPRow ) # 5=whiteip list
        supervisorAddrJson=conf.getAllSupervisorAddrList()
        etcdServerListMap={}
        for serverId in serverIdList:
            etcdServerListMap[str(serverId)]=conf.getEtcdServerList(conf.PLATFORM,serverId)
        self.render("server_mgr.html",
                    Account=self.gmAccount,
                    myPublicIP=self.request.remote_ip,
                    cmds=json.dumps(cmds),
                    whiteIPList=whiteIPList,
                    title="服务器管理",serverIdList=serverIdList,supervisorAddrJson=supervisorAddrJson,etcdServerListMap=etcdServerListMap)

class ServerStopping(BaseHandler):
    @asynchronous
    @gen.coroutine
    def self_post(self):
        serverIdStr=self.get_argument('serverId')
        processIdStr=self.get_argument('processId')
        if processIdStr=='' or processIdStr=="0":
            app.Redis.publish(redis_notify.get_server_redis_notify_channel(conf.PLATFORM,serverIdStr), redis_notify.NOTIFY_TYPE_SERVER_STOPPING)
        else:
            app.Redis.publish(redis_notify.get_process_redis_notify_channel(conf.PLATFORM,serverIdStr,processIdStr), redis_notify.NOTIFY_TYPE_SERVER_STOPPING)
        time.sleep(0.1)
        self.write('success')
class ServerStop(BaseHandler):
    @asynchronous
    @gen.coroutine
    def self_post(self):
        serverIdStr=self.get_argument('serverId')
        processIdStr=self.get_argument('processId')
        if processIdStr=='' or processIdStr=="0":
            app.Redis.publish(redis_notify.get_server_redis_notify_channel(conf.PLATFORM,serverIdStr), redis_notify.NOTIFY_TYPE_SERVER_STOP)
        else:
            app.Redis.publish(redis_notify.get_process_redis_notify_channel(conf.PLATFORM,serverIdStr,processIdStr), redis_notify.NOTIFY_TYPE_SERVER_STOP)
        time.sleep(0.1)
        self.write('success')

class ServerExec(BaseHandler):
    @asynchronous
    @gen.coroutine
    def self_post(self):
        serverIdStr=self.get_argument('serverId')
        processIdStr=self.get_argument('processId')
        cmd=self.get_argument('cmd','')
        if cmd=="ll":
            cmd="ls -lthGvr"
        if cmd=="llh":
            cmd="ls -lthGvrh"
        if cmd.startswith("ll "):
            cmd=cmd.replace("ll ","ls -l ")
        if cmd.startswith("llh "):
            cmd=cmd.replace("llh ","ls -lh ")


        if processIdStr=='-1':  # on gmt
            app.Logger.info(cmd)
            self.write("<span style='color:green'>$ %s </span>"%(cmd))
            self.write("<br/>")

            process = Subprocess(cmd, stdout=Subprocess.STREAM, stderr=Subprocess.STREAM, shell=True)
            try:
                while True:
                    pout = yield process.stdout.read_until("\n")
                    # , process.stderr.read_until("\n")
                    app.Logger.info(pout)
                    pout=pout.replace(" ","&nbsp;")
                    pout=pout.replace("\t","&nbsp;&nbsp;&nbsp;&nbsp;")
                    self.write(pout)
                    # self.write(err)
                    self.write("<br/>")
                    self.flush()
            except Exception, error:
                self.flush()

            self.write("eof")
            self.flush()
            self.finish()
            return
        elif processIdStr=='' or processIdStr=="0":
            cmd=cmd.replace("\"","\\\"")
            app.Redis.publish(redis_notify.get_server_redis_notify_channel(conf.PLATFORM,serverIdStr), redis_notify.NOTIFY_TYPE_SERVER_EXEC%(cmd))
        else:
            cmd=cmd.replace("\"","\\\"")
            app.Redis.publish(redis_notify.get_process_redis_notify_channel(conf.PLATFORM,serverIdStr,processIdStr), redis_notify.NOTIFY_TYPE_SERVER_EXEC%(cmd))
        time.sleep(1)

        output=app.Redis.get(conf.AppName+"_cmd_output")
        output=output.replace("\n","<br/>")
        self.write(output)

class ServerSwitch(BaseHandler):
    @asynchronous
    @gen.coroutine
    def self_post(self):
        serverIdStr=self.get_argument('serverId')
        processIdStr=self.get_argument('processId')
        processIdStr=self.get_argument('processId')
        if processIdStr=='' or processIdStr=="0" or serverIdStr=='' or serverIdStr=='0':
            self.write('params wrong')
            return
        serverInfo=conf.getEtcdServerProcess(conf.PLATFORM,serverIdStr,processIdStr)
        if serverInfo==None:
            self.write('server not running')
            return
        if serverInfo['st']=='stopping':
            serverInfo['st']='running'
        else:
            serverInfo['st']='stopping'


        conf.putEtcdServerProcess(conf.PLATFORM,serverIdStr,processIdStr,serverInfo)
        time.sleep(0.1)
        self.write('success')



        # maintainList=yield app.DBMgr.maintainDB.select_all()
        # self.render("maintain.html",title="维护公告",maintainList=maintainList)
class KickUser(BaseHandler):
    @asynchronous
    @gen.coroutine
    def self_post(self):
        serverIdStr=self.get_argument('serverId','0')
        if serverIdStr=='':
            serverIdStr='0'
        processIdStr=self.get_argument('processId','0')
        if processIdStr=='':
            processIdStr="0"
        uin=self.get_argument('uin','0') # 0表示踢所有人
        if  serverIdStr=="0":
            redisChan=redis_notify.get_platform_redis_notify_channel(conf.PLATFORM)
        elif processIdStr=="0":
            redisChan=redis_notify.get_server_redis_notify_channel(conf.PLATFORM,serverIdStr)
        elif int(processIdStr)!=0:
            redisChan=redis_notify.get_process_redis_notify_channel(conf.PLATFORM,serverIdStr,processIdStr)
        else:
            redisChan=redis_notify.get_platform_redis_notify_channel(conf.PLATFORM)

        app.Redis.publish(redisChan, redis_notify.NOTIFY_TYPE_KICK_USER%uin)
        time.sleep(0.1)
        self.write('success')

class DelUser(BaseHandler):
    @asynchronous
    @gen.coroutine
    def self_post(self):
        uin= self.get_argument('uin','0')
        accountId= self.get_argument('accountId','')
        now=datetime.now()
        index=accountId.find("|||")
        if index>0:
            accountId=accountId[:index]+"|||"+now.strftime("%Y%m%d%H%M%S")
        else:
            accountId=accountId+"|||"+now.strftime("%Y%m%d%H%M%S")
        app.DBMgr.getUserDB().updateAccountId(uin,accountId)
        self.write('success')


class WhiteIPDelete(BaseHandler):
    @asynchronous
    @gen.coroutine
    def self_post(self):
        id= self.get_argument('id','')
        if id=='':
            return
        yield app.DBMgr.getProfileDB().execSql("delete from ban where Id=%s"%(id))
        time.sleep(0.13)
        app.Redis.publish(redis_notify.get_platform_redis_notify_channel(conf.PLATFORM), redis_notify.NOTIFY_TYPE_RELOAD_BAN)

        self.write('success')

class WhiteIPAdd(BaseHandler):
    @asynchronous
    @gen.coroutine
    def self_post(self):
        ip= self.get_argument('ip','')
        if ip=='':
            return
        now=datetime.now()
        year5FromNow=now+ timedelta(days=365*5)

        yield app.DBMgr.getProfileDB().execSql("insert into ban (Type,Content,EndBanTime) value (5,'%s','%s')"%(ip,year5FromNow))
        time.sleep(0.13)
        app.Redis.publish(redis_notify.get_platform_redis_notify_channel(conf.PLATFORM), redis_notify.NOTIFY_TYPE_RELOAD_BAN)

        self.write('success')

class ProfHandler(BaseHandler):
    @asynchronous
    @gen.coroutine
    def self_get(self):
        serverIdList= app.DBMgr.get_all_server_id()
        self.render("server_prof.html",
                Account=self.gmAccount,
                title="服务器Prof",serverIdList=serverIdList)


    @asynchronous
    @gen.coroutine
    def self_post(self):
        server= self.get_argument('serverId','')
        process= self.get_argument('process','')
        serverType= self.get_argument('server-type','')
        profType= self.get_argument('profType','')


        print(redis_notify.get_process_redis_notify_channel(conf.PLATFORM,server,process))
        print( '{"type":%s,"accept_type":"%s"}'%(profType,serverType))
        if process!='0':
            app.Redis.publish(redis_notify.get_process_redis_notify_channel(conf.PLATFORM,server,process), '{"type":%s,"accept_type":"%s"}'%(profType,serverType))
        else:
            app.Redis.publish(redis_notify.get_server_redis_notify_channel(conf.PLATFORM,server), '{"type":%s,"accept_type":"%s"}'%(profType,serverType))



        self.write('success')
