#  -*- coding:utf-8 -*-
__author__ = 'jixiufeng'



from datetime import datetime, timedelta
from tornado import  gen
from handler.base import *
from tornado.web import asynchronous
import conf
import redis_notify
# import json
import app
import time
import copy

class BICurrencyChangeHandler(BaseHandler):
    @asynchronous
    @gen.coroutine
    def self_get(self):
        tStr = self.get_argument('time','')
        if tStr=='':
            self.write(json.dumps({"result":"请选择日期"}))
            return
        uin = self.get_argument('uin','')
        if uin=='':
            self.write(json.dumps({"result":"玩家Id不能为空"}))
            return

        t=time.strptime(tStr,"%Y-%m-%d")
        startTime=datetime(*t[:3])
        endTime=startTime+timedelta(days=1)

        currencyChangeList=yield app.DBMgr.getCurrencyChangeDB().select_all(uin,startTime,endTime)
        self.render("bi_currency_change_list.html", title="货币变化日志",
                    currencyChangeList=currencyChangeList,
                    Account=self.gmAccount,
                    channelMap=conf.getChannelNameMap())


class BIItemChangeHandler(BaseHandler):
    @asynchronous
    @gen.coroutine
    def self_get(self):
        uin = self.get_argument('uin','')
        tStr = self.get_argument('time','')
        if tStr=='':
            self.write(json.dumps({"result":"请选择日期"}))
            return
        if uin=='':
            self.write(json.dumps({"result":"玩家Id不能为空"}))
            return
        t=time.strptime(tStr,"%Y-%m-%d")
        startTime=datetime(*t[:3])
        endTime=startTime+timedelta(days=1)



        currencyChangeList=yield app.DBMgr.getItemChangeDB().select_all(uin,startTime,endTime)
        self.render("bi_item_change_list.html", title="道具变化日志",
                    currencyChangeList=currencyChangeList,
                    Account=self.gmAccount,
                    channelMap=conf.getChannelNameMap())

class BIGearGotHandler(BaseHandler):
    @asynchronous
    @gen.coroutine
    def self_get(self):
        uin = self.get_argument('uin','')
        tStr = self.get_argument('time','')
        if tStr=='':
            self.write(json.dumps({"result":"请选择日期"}))
            return
        if uin=='':
            self.write(json.dumps({"result":"玩家Id不能为空"}))
            return
        t=time.strptime(tStr,"%Y-%m-%d")
        startTime=datetime(*t[:3])
        endTime=startTime+timedelta(days=1)



        currencyChangeList=yield app.DBMgr.getGearGotDB().select_all(uin,startTime,endTime)
        self.render("bi_gear_got_list.html", title="装备获得日志",
                    currencyChangeList=currencyChangeList,
                    Account=self.gmAccount,
                    channelMap=conf.getChannelNameMap())

class BIGearFortifyHandler(BaseHandler):
    @asynchronous
    @gen.coroutine
    def self_get(self):
        uin = self.get_argument('uin','')
        tStr = self.get_argument('time','')
        if tStr=='':
            self.write(json.dumps({"result":"请选择日期"}))
            return
        if uin=='':
            self.write(json.dumps({"result":"玩家Id不能为空"}))
            return
        t=time.strptime(tStr,"%Y-%m-%d")
        startTime=datetime(*t[:3])
        endTime=startTime+timedelta(days=1)



        currencyChangeList=yield app.DBMgr.getGearFortifyDB().select_all(uin,startTime,endTime)
        self.render("bi_gear_fortify_list.html", title="装备强化日志",
                    currencyChangeList=currencyChangeList,
                    Account=self.gmAccount,
                    channelMap=conf.getChannelNameMap())

class BIGearRefineHandler(BaseHandler):
    @asynchronous
    @gen.coroutine
    def self_get(self):
        uin = self.get_argument('uin','')
        tStr = self.get_argument('time','')
        if tStr=='':
            self.write(json.dumps({"result":"请选择日期"}))
            return
        if uin=='':
            self.write(json.dumps({"result":"玩家Id不能为空"}))
            return
        t=time.strptime(tStr,"%Y-%m-%d")
        startTime=datetime(*t[:3])
        endTime=startTime+timedelta(days=1)



        currencyChangeList=yield app.DBMgr.getGearRefineDB().select_all(uin,startTime,endTime)
        self.render("bi_gear_refine_list.html", title="装备洗练日志",
                    currencyChangeList=currencyChangeList,
                    Account=self.gmAccount,
                    channelMap=conf.getChannelNameMap())

class BILevelUpHandler(BaseHandler):
    @asynchronous
    @gen.coroutine
    def self_get(self):
        uin = self.get_argument('uin','')
        tStr = self.get_argument('time','')
        if tStr=='':
            self.write(json.dumps({"result":"请选择日期"}))
            return
        if uin=='':
            self.write(json.dumps({"result":"玩家Id不能为空"}))
            return
        t=time.strptime(tStr,"%Y-%m-%d")
        startTime=datetime(*t[:3])
        endTime=startTime+timedelta(days=1)



        currencyChangeList=yield app.DBMgr.getLevelUpDB().select_all(uin,startTime,endTime)
        self.render("bi_levelup_list.html", title="玩家升级日志",
                    currencyChangeList=currencyChangeList,
                    Account=self.gmAccount,
                    channelMap=conf.getChannelNameMap())

class BIPartnerGotHandler(BaseHandler):
    @asynchronous
    @gen.coroutine
    def self_get(self):
        uin = self.get_argument('uin','')
        tStr = self.get_argument('time','')
        if tStr=='':
            self.write(json.dumps({"result":"请选择日期"}))
            return
        if uin=='':
            self.write(json.dumps({"result":"玩家Id不能为空"}))
            return
        t=time.strptime(tStr,"%Y-%m-%d")
        startTime=datetime(*t[:3])
        endTime=startTime+timedelta(days=1)



        currencyChangeList=yield app.DBMgr.getPartnerDB().select_all(uin,startTime,endTime)
        self.render("bi_partner_list.html", title="获得伙伴日志",
                    currencyChangeList=currencyChangeList,
                    Account=self.gmAccount,
                    channelMap=conf.getChannelNameMap())

class BIGuideHandle(BaseHandler):
    GuideActorDestroyOrder ={
"2200001":{"WordID":"2200001","order":  1     ,"name":"新手入场",    "desc":"这是什么地方？"},
"2200002":{"WordID":"2200002","order":  2     ,"name":"新手入场",    "desc":"这是史莱姆的洞穴，也是新手的必经之路"},
"2200003":{"WordID":"2200003","order":  3     ,"name":"新手入场",    "desc":"这个是出口吗？"},
"2200004":{"WordID":"2200004","order":  4     ,"name":"新手入场",    "desc":"没错，走到这里就可以了，不过……"},
"2200005":{"WordID":"2200005","order":  5     ,"name":"新手入场",    "desc":"不过什么啊？"},
"2200006":{"WordID":"2200006","order":  6     ,"name":"新手入场",    "desc":"没什么没什么^_^(呃，我先不吓唬年轻人了)"},
"2200007":{"WordID":"2200007","order":  7     ,"name":"学习技能",    "desc":"恭喜你升级了，每2级可以获得1技能点数"},
"2200008":{"WordID":"2200008","order":  8     ,"name":"学习技能",    "desc":"点击这里打开技能面板"},
"2200009":{"WordID":"2200009","order":  9     ,"name":"学习技能",    "desc":"点击你的第一个技能"},
"2200010":{"WordID":"2200010","order": 10     ,"name":"学习技能",    "desc":"使用1个技能点数来学习该技能"},
"2200011":{"WordID":"2200011","order": 11     ,"name":"学习技能",    "desc":"返回"},
"2200012":{"WordID":"2200012","order": 12     ,"name":"学习技能",    "desc":"移动到这里"},
"2200013":{"WordID":"2200013","order": 13     ,"name":"学习技能",    "desc":"点击下方图标释放技能"},
"2200014":{"WordID":"2200014","order": 14     ,"name":"学习技能",    "desc":"照这个姿势杀出一条血路吧！:D"},
"2200015":{"WordID":"2200015","order": 15     ,"name":"钥匙引导",    "desc":"怎么掉了个钥匙啊？"},
"2200016":{"WordID":"2200016","order": 16     ,"name":"钥匙引导",    "desc":"哦对对，出口要钥匙才能开的！"},
"2200017":{"WordID":"2200017","order": 17     ,"name":"钥匙引导",    "desc":"怎么不早说？"},
"2200018":{"WordID":"2200018","order": 18     ,"name":"钥匙引导",    "desc":"老了记性不好了^_^"},
"2200019":{"WordID":"2200019","order": 19     ,"name":"BOSS引导",    "desc":"这。。是啥东西啊？"},
"2200020":{"WordID":"2200020","order": 20     ,"name":"BOSS引导",    "desc":"每关都有一个BOSS，这关的BOSS是：巨型史莱姆"},
"2200021":{"WordID":"2200021","order": 21     ,"name":"BOSS引导",    "desc":"好，你帮我打"},
"2200022":{"WordID":"2200022","order": 22     ,"name":"BOSS引导",    "desc":"我这老胳膊老腿的不中用啦，我看好你哦！^_^"},
"2200023":{"WordID":"2200023","order": 23     ,"name":"BOSS引导",    "desc":"切！BOSS关也需要找钥匙吗？"},
"2200024":{"WordID":"2200024","order": 24     ,"name":"BOSS引导",    "desc":"打完BOSS你就知道了:D"},
"2210024":{"WordID":"2210024","order": 25     ,"name":"装备属性",    "desc":"恭喜你获得了一件蓝装，让我们来看看它的属性吧"},
"2210025":{"WordID":"2210025","order": 26     ,"name":"装备属性",    "desc":"打开人物界面"},
"2210026":{"WordID":"2210026","order": 27     ,"name":"装备属性",    "desc":"点击该装备"},
"2210027":{"WordID":"2210027","order": 28     ,"name":"装备属性",    "desc":"显示在这里的是主属性，会随装备的强化而大幅提升数值"},
"2210020":{"WordID":"2210020","order": 29     ,"name":"装备属性",    "desc":"显示在这里的是随机属性，装备品质越高，条目越多，洗练时可以重新洗出随机属性"},
"2210021":{"WordID":"2210021","order": 30     ,"name":"装备属性",    "desc":"每件装备在获得时都会有几率生成一些额外属性"},
"2210022":{"WordID":"2210022","order": 31     ,"name":"装备属性",    "desc":"属性的颜色表示装备属性浮动的高低，蓝色表示一般，紫色属于高级，橙色最高"},
"2210023":{"WordID":"2210023","order": 32     ,"name":"装备属性",    "desc":"好了，让我们把他穿上吧！希望你能再多获得一些好装备！^_^"},
"2210028":{"WordID":"2210028","order": 33     ,"name":"装备属性",    "desc":"关闭界面"},
"2210029":{"WordID":"2210029","order": 34     ,"name":"装备属性",    "desc":"返回战斗"},
"2200034":{"WordID":"2200034","order": 35     ,"name":"返回城镇",    "desc":"让我们去杂货店里看看有什么补给品吧"},
"2200036":{"WordID":"2200036","order": 36     ,"name":"返回城镇",    "desc":"点击选择HP药水"},
"2200037":{"WordID":"2200037","order": 37     ,"name":"返回城镇",    "desc":"买一瓶HP药水"},
"2200038":{"WordID":"2200038","order": 38     ,"name":"返回城镇",    "desc":"点击选择MP药水"},
"2200039":{"WordID":"2200039","order": 39     ,"name":"返回城镇",    "desc":"买一瓶MP药水"},
"2200040":{"WordID":"2200040","order": 40     ,"name":"返回城镇",    "desc":"点击关闭面板"},
"2200051":{"WordID":"2200051","order": 41     ,"name":"返回城镇",    "desc":"本来，咱们还可以干点别的，但现在都干不了了！"},
"2200041":{"WordID":"2200041","order": 42     ,"name":"返回城镇",    "desc":"铁匠被怪物抓走了"},
"2200042":{"WordID":"2200042","order": 43     ,"name":"返回城镇",    "desc":"契约商人也是"},
"2200043":{"WordID":"2200043","order": 44     ,"name":"返回城镇",    "desc":"让我们把他们都救出来吧！"},
"2200044":{"WordID":"2200044","order": 45     ,"name":"返回城镇",    "desc":"点击选择关卡"},
"2200045":{"WordID":"2200045","order": 46     ,"name":"返回城镇",    "desc":"每个关卡进入前都可以领任务"},
"2200046":{"WordID":"2200046","order": 47     ,"name":"返回城镇",    "desc":"任务会给予大量的金币"},
"2200047":{"WordID":"2200047","order": 48     ,"name":"返回城镇",    "desc":"对任务不满意还可以刷新"},
"2200048":{"WordID":"2200048","order": 49     ,"name":"返回城镇",    "desc":"好了，进入战斗，营救伙伴！"},
"2210005":{"WordID":"2210005","order": 50     ,"name":"第一关进入",  "desc":"可恶！就差一步！"},
"2210006":{"WordID":"2210006","order": 51     ,"name":"第一关进入",  "desc":"行啊小鬼，学会抓人了啊"},
"2210007":{"WordID":"2210007","order": 52     ,"name":"第一关进入",  "desc":"哪里哪里，大王过奖^_^"},
"2210008":{"WordID":"2210008","order": 53     ,"name":"第一关进入",  "desc":"把他搬到我这来，让我看着他呗"},
"2210009":{"WordID":"2210009","order": 54     ,"name":"第一关进入",  "desc":"嗯嗯好的！"},
"2210010":{"WordID":"2210010","order": 55     ,"name":"第一关进入",  "desc":"找到铁匠大叔了！不能让他们得逞！"},
"2210011":{"WordID":"2210011","order": 56     ,"name":"第一关进入",  "desc":"上！记得多用地图技能！"},
"2210012":{"WordID":"2210012","order": 57     ,"name":"第一关进入",  "desc":"好的，村长！！"},
"2210013":{"WordID":"2210013","order": 58     ,"name":"第一关BOSS",  "desc":"救命！"},
"2210014":{"WordID":"2210014","order": 59     ,"name":"第一关BOSS",  "desc":"坚持住！"},
"2210015":{"WordID":"2210015","order": 60     ,"name":"第一关BOSS",  "desc":"啊！终于得救了！"},
"2210016":{"WordID":"2210016","order": 61     ,"name":"第一关BOSS",  "desc":"呃……您是干啥的？"},
"2210017":{"WordID":"2210017","order": 62     ,"name":"第一关BOSS",  "desc":"别问这么多，先给我解绑再说！"},
"2200053":{"WordID":"2200053","order": 63     ,"name":"强化引导",    "desc":"谢谢你救了我，让我帮你强化装备吧"},
"2200054":{"WordID":"2200054","order": 64     ,"name":"强化引导",    "desc":"先选择一件装备"},
"2200055":{"WordID":"2200055","order": 65     ,"name":"强化引导",    "desc":"然后点击强化按钮"},
"2200056":{"WordID":"2200056","order": 66     ,"name":"强化引导",    "desc":"成功了！以后记得常来哦！（现在还可以继续强化其它装备）"},
"2210301":{"WordID":"2210301","order": 67     ,"name":"第二关进入",  "desc":"我晕！这位是谁没见过啊？"},
"2210302":{"WordID":"2210302","order": 68     ,"name":"第二关进入",  "desc":"这人身上有不少好装备，快把他给我送过来！"},
"2210303":{"WordID":"2210303","order": 69     ,"name":"第二关进入",  "desc":"不分我一点，就不给你送"},
"2210304":{"WordID":"2210304","order": 70     ,"name":"第二关进入",  "desc":"不送我就送你归西"},
"2210305":{"WordID":"2210305","order": 71     ,"name":"第二关进入",  "desc":"我送:("},
"2210306":{"WordID":"2210306","order": 72     ,"name":"第二关进入",  "desc":"刚才好像说……有好装备！？$_$"},
"2210307":{"WordID":"2210307","order": 73     ,"name":"第二关BOSS",  "desc":"…………"},
"2210308":{"WordID":"2210308","order": 74     ,"name":"第二关BOSS",  "desc":"你到底谁啊？"},
"2210309":{"WordID":"2210309","order": 75     ,"name":"第二关BOSS",  "desc":"我是卖装备的！都是好东西！"},
"2210310":{"WordID":"2210310","order": 76     ,"name":"第二关BOSS",  "desc":"不给打折我就不管你"},
"2210311":{"WordID":"2210311","order": 77     ,"name":"第二关BOSS",  "desc":"5折5折！！-_-!"},
"2200059":{"WordID":"2200059","order": 78     ,"name":"训练指引",    "desc":"让我们来看看刚才得到的红卷轴是干啥用的"},
"2200060":{"WordID":"2200060","order": 79     ,"name":"训练指引",    "desc":"点击训练"},
"2200061":{"WordID":"2200061","order": 80     ,"name":"训练指引",    "desc":"点击这里训练角色！"},
"2200062":{"WordID":"2200062","order": 81     ,"name":"训练指引",    "desc":"训练等级提升会送高品质武器！努力积攒卷轴吧！"},
"2210201":{"WordID":"2210201","order": 82     ,"name":"第三关进入",  "desc":"又差了一步？"},
"2210202":{"WordID":"2210202","order": 83     ,"name":"第三关进入",  "desc":"傻站着干嘛？没看人家都找上门来了吗？"},
"2210203":{"WordID":"2210203","order": 84     ,"name":"第三关进入",  "desc":"是啊！那怎么办啊，大王？"},
"2210204":{"WordID":"2210204","order": 85     ,"name":"第三关进入",  "desc":"赶紧把人质送我这来啊！笨蛋！"},
"2210205":{"WordID":"2210205","order": 86     ,"name":"第三关进入",  "desc":"哦对！"},
"2210206":{"WordID":"2210206","order": 87     ,"name":"第三关进入",  "desc":"这些怪物看来很没脑子，他们为什么会出现在这里？"},
"2210207":{"WordID":"2210207","order": 88     ,"name":"第四关进入",  "desc":"天啊，我不会死吧？"},
"2210208":{"WordID":"2210208","order": 89     ,"name":"第四关进入",  "desc":"不会！#_#$"},
"2210209":{"WordID":"2210209","order": 90     ,"name":"第四关进入",  "desc":"谢谢谢谢！！我还真以为我会死掉呢！"},
"2210210":{"WordID":"2210210","order": 91     ,"name":"第四关进入",  "desc":"哈哈，我再晚一步，指不定那怪物会对你做什么呢"},
"2210211":{"WordID":"2210211","order": 92     ,"name":"第四关进入",  "desc":"嗯！肯定都是一些，直击灵魂的事情！"},
"2200026":{"WordID":"2200026","order": 93     ,"name":"招募引导",    "desc":"谢谢你刚才救了我，来我这看看吧"},
"2200027":{"WordID":"2200027","order": 94     ,"name":"招募引导",    "desc":"如果你需要伙伴辅助你战斗，可以来我这看看"},
"2200028":{"WordID":"2200028","order": 95     ,"name":"招募引导",    "desc":"为了答谢你的救命之恩，前两位的伙伴价格我就给你免了"},
"2200029":{"WordID":"2200029","order": 96     ,"name":"招募引导",    "desc":"艾米是一位远程攻击角色，擅长大范围攻击，配合近战角色最佳"},
"2200030":{"WordID":"2200030","order": 97     ,"name":"招募引导",    "desc":"而隆则是一位肉搏角色，擅长攻击单体敌人，配合远程角色最佳"},
"2200031":{"WordID":"2200031","order": 98     ,"name":"招募引导",    "desc":"根据你的战术，选择一位最佳拍档吧:D"},
"2200049":{"WordID":"2200049","order": 99     ,"name":"切换角色",    "desc":"你现在可以随时点击这里切换角色"},
"2200050":{"WordID":"2200050","order":100     ,"name":"切换角色",    "desc":"伙伴的技能虽然比主角少，但是都特别独特，好好利用吧"},
"2200063":{"WordID":"2200063","order":101     ,"name":"深渊引导",    "desc":"恭喜您成功开启了深渊模式"},
"2200064":{"WordID":"2200064","order":102     ,"name":"深渊引导",    "desc":"点击副本入口"},
"2200065":{"WordID":"2200065","order":103     ,"name":"深渊引导",    "desc":"点击深渊模式按钮"},
"2200066":{"WordID":"2200066","order":104     ,"name":"深渊引导",    "desc":"深渊模式主要产出高品质装备和稀有材料"},
"2200067":{"WordID":"2200067","order":105     ,"name":"深渊引导",    "desc":"但是难度你懂的"}
}
    GuideStepFinish= {
"10003"  :{"X":1 ,"Y":3,"name":"陶罐  ","step":"新手1","order": 1 },
"60008"  :{"X":6 ,"Y":8,"name":"陶罐  ","step":"新手1","order": 2 },
"100008" :{"X":10,"Y":8,"name":"陶罐  ","step":"新手1","order": 3 },
"130003" :{"X":13,"Y":3,"name":"陶罐  ","step":"新手1","order": 4 },
"140008" :{"X":14,"Y":8,"name":"陶罐  ","step":"新手1","order": 5 },
"150008" :{"X":15,"Y":8,"name":"陶罐  ","step":"新手1","order": 6 },
"190003" :{"X":19,"Y":3,"name":"陶罐  ","step":"新手1","order": 7 },
"190007" :{"X":19,"Y":7,"name":"陶罐  ","step":"新手1","order": 8 },
"170006" :{"X":17,"Y":6,"name":"小红  ","step":"新手1","order": 9 },
"130004" :{"X":13,"Y":4,"name":"史莱姆","step":"新手1","order":10 },
"130007" :{"X":13,"Y":7,"name":"史莱姆","step":"新手1","order":11 },
"140003" :{"X":14,"Y":3,"name":"史莱姆","step":"新手1","order":12 },
"150005" :{"X":15,"Y":5,"name":"史莱姆","step":"新手1","order":13 },
"150007" :{"X":15,"Y":7,"name":"史莱姆","step":"新手1","order":14 },
"160006" :{"X":16,"Y":6,"name":"史莱姆","step":"新手1","order":15 },
"160008" :{"X":16,"Y":8,"name":"史莱姆","step":"新手1","order":16 },
"170004" :{"X":17,"Y":4,"name":"史莱姆","step":"新手1","order":17 },
"170005" :{"X":17,"Y":5,"name":"史莱姆","step":"新手1","order":18 },
"60002"  :{"X":6 ,"Y":2,"name":"陶罐  ","step":"新手2","order":19 },
"80001"  :{"X":8 ,"Y":1,"name":"陶罐  ","step":"新手2","order":20 },
"100002" :{"X":10,"Y":2,"name":"陶罐  ","step":"新手2","order":21 },
"110002" :{"X":11,"Y":2,"name":"陶罐  ","step":"新手2","order":22 },
"120003" :{"X":12,"Y":3,"name":"陶罐  ","step":"新手2","order":23 },
"120005" :{"X":12,"Y":5,"name":"陶罐  ","step":"新手2","order":24 },
"60006"  :{"X":6 ,"Y":6,"name":"陶罐  ","step":"新手2","order":25 },
"70006"  :{"X":7 ,"Y":6,"name":"陶罐  ","step":"新手2","order":26 },
"100006" :{"X":10,"Y":6,"name":"陶罐  ","step":"新手2","order":27 },
"70002"  :{"X":7 ,"Y":2,"name":"史莱姆","step":"新手2","order":28 },
"90002"  :{"X":9 ,"Y":2,"name":"史莱姆","step":"新手2","order":29 },
"70003"  :{"X":7 ,"Y":3,"name":"史莱姆","step":"新手2","order":30 },
"100003" :{"X":10,"Y":3,"name":"史莱姆","step":"新手2","order":31 },
"110003" :{"X":11,"Y":3,"name":"史莱姆","step":"新手2","order":32 },
"60005"  :{"X":6 ,"Y":5,"name":"史莱姆","step":"新手2","order":33 },
"70005"  :{"X":7 ,"Y":5,"name":"史莱姆","step":"新手2","order":34 },
"110005" :{"X":11,"Y":5,"name":"史莱姆","step":"新手2","order":35 },
"80006"  :{"X":8 ,"Y":6,"name":"史莱姆","step":"新手2","order":36 },
"110006" :{"X":11,"Y":6,"name":"史莱姆","step":"新手2","order":37 },
}

    @asynchronous
    @gen.coroutine
    def self_get(self):


        map1=yield app.DBMgr.getGuideDB().select_cnt_map()
        list1=[]
        for key in BIGuideHandle.GuideActorDestroyOrder:
            e=BIGuideHandle.GuideActorDestroyOrder.get(key)
            countInfo=map1.get(key)
            if  countInfo!=None :
                e['count']=countInfo['count']
            else:
                e['count']=0
            list1.append(e)

        list2=[]
        map2=yield app.DBMgr.getGuideDB().select_cnt_2_map()
        for key in BIGuideHandle.GuideStepFinish:
            e=BIGuideHandle.GuideStepFinish.get(key)
            countInfo=map2.get(key)
            if  countInfo!=None :
                e['count']=countInfo['count']
                e['X']=countInfo['X']
                e['Y']=countInfo['Y']
                e['Key']=countInfo['Key']
            else:
                e['count']=0
                e['Key']="Unknown"
            list2.append(e)



        # list2=yield app.DBMgr.getGuideDB().select_cnt_2()
        list1=sorted(list1,cmp=self.sortFunc,reverse=False)
        list2=sorted(list2,cmp=self.sortFunc,reverse=False)
        self.render("bi_guide_list.html", title="新手引导打点分析",
                    list1=list1,
                    list2=list2,
                    Account=self.gmAccount,
                    channelMap=conf.getChannelNameMap())

    def sortFunc(self,e1 ,e2 ):
            if e1.get("order",None)==None:
                return -1
            elif e2.get("order",None)==None:
                return 1

            diff=e1.get("order",0)-e2.get("order",0)
            return  diff



