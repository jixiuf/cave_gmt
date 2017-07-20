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
        wordIdMap=yield app.DBMgr.getWordIdMap(1)
        for index, item in enumerate(currencyChangeList):
            source=item.get("Source",0)
            sourceStr=wordIdMap.get(int(source),source)
            item['Source']=sourceStr
            currencyChangeList[index]=item

        self.render("bi_currency_change_list.html", title="货币变化日志",
                    currencyChangeList=currencyChangeList,
                    wordIdMap=wordIdMap,
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
        wordIdMap=yield app.DBMgr.getWordIdMap(1)
        for index, item in enumerate(currencyChangeList):
            source=item.get("Source",0)
            sourceStr=wordIdMap.get(int(source),source)
            item['Source']=sourceStr
            currencyChangeList[index]=item


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
        wordIdMap=yield app.DBMgr.getWordIdMap(1)
        for index, item in enumerate(currencyChangeList):
            source=item.get("Source",0)
            sourceStr=wordIdMap.get(int(source),source)
            item['Source']=sourceStr
            currencyChangeList[index]=item


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
        # wordIdMap=yield app.DBMgr.getWordIdMap(1)
        # for index, item in enumerate(currencyChangeList):
        #     source=item.get("Source",0)
        #     sourceStr=wordIdMap.get(int(source),source)
        #     item['Source']=sourceStr
        #     currencyChangeList[index]=item

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
        # wordIdMap=yield app.DBMgr.getWordIdMap(1)
        # for index, item in enumerate(currencyChangeList):
        #     source=item.get("Source",0)
        #     sourceStr=wordIdMap.get(int(source),source)
        #     item['Source']=sourceStr
        #     currencyChangeList[index]=item

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
'2200001':{'WordID':'2200001','order':1,'name':'新手进入','desc':'一般开始都会有一个奇怪的老头来做新手引导吧？'},
'2200002':{'WordID':'2200002','order':2,'name':'新手进入','desc':'没错！就是村长我！咳...我将指引你离开这里。'},
'2200003':{'WordID':'2200003','order':3,'name':'新手进入','desc':'传送门？可是我是跳下来的啊！'},
'2200004':{'WordID':'2200004','order':4,'name':'新手进入','desc':'不不不，我们得往下一层走才能出去。 '},
'2200005':{'WordID':'2200005','order':5,'name':'新手进入','desc':'现在看来我只能一路射爆这些怪物到达那里。'},
'2200006':{'WordID':'2200006','order':6,'name':'怪物信息查看引导','desc':'作为一名长者，我要给你一点关于操作的经验。'},
'2200007':{'WordID':'2200007','order':7,'name':'怪物信息查看引导','desc':'用你的食指长按怪物，请不要竖中指谢谢'},
'2200008':{'WordID':'2200008','order':8,'name':'怪物信息查看引导','desc':'战斗前看看它的信息，让战斗如鱼得水。'},
'2200009':{'WordID':'2200009','order':9,'name':'怪物信息查看引导','desc':'看完之后点击任意位置关闭怪物信息页面。'},
'2200010':{'WordID':'2200010','order':10,'name':'战斗与技能引导','desc':'接下来！点击怪物，正面上啊！'},
'2200011':{'WordID':'2200011','order':11,'name':'战斗与技能引导','desc':'升级了？跟着指示点击吧！'},
'2200012':{'WordID':'2200012','order':12,'name':'战斗与技能引导','desc':'点击你的第一个技能'},
'2200013':{'WordID':'2200013','order':13,'name':'战斗与技能引导','desc':'然后点击学习按钮'},
'2200014':{'WordID':'2200014','order':14,'name':'战斗与技能引导','desc':'这样！你就成功地学会了第一个技能！点击返回回到地图页面！'},
'2200015':{'WordID':'2200015','order':15,'name':'战斗与技能引导','desc':'点击地图！你就能到达那里！'},
'2200016':{'WordID':'2200016','order':16,'name':'战斗与技能引导','desc':'没见过的怪物！要怎么办来着？长按怪物查看。'},
'2200017':{'WordID':'2200017','order':17,'name':'战斗与技能引导','desc':'无法显示等级信息？ 我们还是先绕过他吧！'},
'2200018':{'WordID':'2200018','order':18,'name':'战斗与技能引导','desc':'点击移动到这里绕过怪物'},
'2200019':{'WordID':'2200019','order':19,'name':'战斗与技能引导','desc':'我们来释放一次主动技能吧！点击下方技能图标进行释放。'},
'2200020':{'WordID':'2200020','order':20,'name':'战斗与技能引导','desc':'这是火护盾的怪物？你需要一把冰属性的武器！'},
'2200021':{'WordID':'2200021','order':21,'name':'战斗与技能引导','desc':'村长，你老年痴呆犯了？哪来的其它武器？'},
'2200022':{'WordID':'2200022','order':22,'name':'战斗与技能引导','desc':'别担心，说不定你干掉面前的怪物就会掉一个呢？'},
'2200051':{'WordID':'2200051','order':23,'name':'战斗与技能引导','desc':'什么东西都没掉...'},
'2200052':{'WordID':'2200052','order':24,'name':'战斗与技能引导','desc':'咳咳...当然选择原谅它啊！'},
'2200023':{'WordID':'2200023','order':25,'name':'战斗与技能引导','desc':'看看这些陶罐，击碎它们！'},
'2200024':{'WordID':'2200024','order':26,'name':'战斗与技能引导','desc':'释放技能同时击碎多个陶罐'},
'2200025':{'WordID':'2200025','order':27,'name':'属性介绍与换装引导','desc':'这难道是史诗级别的装备么！'},
'2200026':{'WordID':'2200026','order':28,'name':'属性介绍与换装引导','desc':'没错！这把武器附带了冰属性攻击！ '},
'2200053':{'WordID':'2200053','order':29,'name':'属性介绍与换装引导','desc':'开局就送史诗装备么？为啥会装在陶罐里！'},
'2200054':{'WordID':'2200054','order':30,'name':'属性介绍与换装引导','desc':'别吐槽了！ 快换上它！'},
'2200027':{'WordID':'2200027','order':31,'name':'属性介绍与换装引导','desc':'点击左上角人物头像信息框'},
'2200028':{'WordID':'2200028','order':32,'name':'属性介绍与换装引导','desc':'点击这件装备'},
'2200029':{'WordID':'2200029','order':33,'name':'属性介绍与换装引导','desc':'显示在这里的是主属性，会随装备的强化而大幅提升数值'},
'2200030':{'WordID':'2200030','order':34,'name':'属性介绍与换装引导','desc':'显示在这里的是随机属性，装备品质越高，条目越多'},
'2200031':{'WordID':'2200031','order':35,'name':'属性介绍与换装引导','desc':'每件装备在获得时都会有几率生成一些额外属性'},
'2200032':{'WordID':'2200032','order':36,'name':'属性介绍与换装引导','desc':'属性的颜色表示装备属性浮动的高低，蓝色一般，橙色最高'},
'2200033':{'WordID':'2200033','order':37,'name':'属性介绍与换装引导','desc':'好了！快换上它！'},
'2200034':{'WordID':'2200034','order':38,'name':'属性介绍与换装引导','desc':'点击关闭界面'},
'2200035':{'WordID':'2200035','order':39,'name':'属性介绍与换装引导','desc':'让前面的火盾怪感觉一下来自主角的恶意吧！'},
'2200036':{'WordID':'2200036','order':40,'name':'属性介绍与换装引导','desc':'接下来去下一层看看吧！'},
'2200037':{'WordID':'2200037','order':41,'name':'属性介绍与换装引导','desc':'点击下一层入口'},
'2200038':{'WordID':'2200038','order':42,'name':'新手BOSS引导','desc':'不要告诉我这个头顶绿帽的家伙就是魔王！'},
'2200039':{'WordID':'2200039','order':43,'name':'新手BOSS引导','desc':'没错！它就是这里绿帽魔王！'},
'2200040':{'WordID':'2200040','order':44,'name':'新手BOSS引导','desc':'想给我戴绿帽？从来就没有我原谅过别人！'},
'2200041':{'WordID':'2200041','order':45,'name':'新手BOSS引导','desc':'绿帽王离你有点远，你这样喊他是听不到的。'},
'2200042':{'WordID':'2200042','order':46,'name':'陷阱与使用道具引导','desc':'点击移动到这里。'},
'2200043':{'WordID':'2200043','order':47,'name':'陷阱与使用道具引导','desc':'这不是捕兽陷阱么，还让我就这样踩上去！'},
'2200044':{'WordID':'2200044','order':48,'name':'陷阱与使用道具引导','desc':'让你踩是为你好！现在村长教你如何治疗。'},
'2200045':{'WordID':'2200045','order':49,'name':'陷阱与使用道具引导','desc':'点击下方血瓶使用'},
'2200046':{'WordID':'2200046','order':50,'name':'陷阱与使用道具引导','desc':'血量满了！是时候来一波骚操作了！'},
'2200047':{'WordID':'2200047','order':51,'name':'陷阱与使用道具引导','desc':'这些陷阱是可以被技能破坏的哦！'},
'2200055':{'WordID':'2200055','order':52,'name':'陷阱与使用道具引导','desc':'村长我现在想打死你！为什么不早说啊！'},
'2200056':{'WordID':'2200056','order':53,'name':'陷阱与使用道具引导','desc':'不要在意这些细节！快去消灭绿帽王！'},
'2200048':{'WordID':'2200048','order':54,'name':'返回城镇引导','desc':'绿帽王已被消灭！世间再无原谅！'},
'2200049':{'WordID':'2200049','order':55,'name':'返回城镇引导','desc':'等等！村子的铁匠和契约商人被抓走了！'},
'2200050':{'WordID':'2200050','order':56,'name':'返回城镇引导','desc':'点击这里离开地下城。'},
'2210001':{'WordID':'2210001','order':57,'name':'返回城镇引导','desc':'铁匠、契约商人对你的冒险有非常大的作用！'},
'2210002':{'WordID':'2210002','order':58,'name':'返回城镇引导','desc':'少废话！快救人！'},
'2210003':{'WordID':'2210003','order':59,'name':'商店购买引导','desc':'在那之前先去杂货店补给一下吧。'},
'2210004':{'WordID':'2210004','order':60,'name':'商店购买引导','desc':'点击选择HP药水'},
'2210005':{'WordID':'2210005','order':61,'name':'商店购买引导','desc':'买一瓶HP药水'},
'2210006':{'WordID':'2210006','order':62,'name':'商店购买引导','desc':'点击选择MP药水'},
'2210007':{'WordID':'2210007','order':63,'name':'商店购买引导','desc':'买一瓶MP药水'},
'2210008':{'WordID':'2210008','order':64,'name':'商店购买引导','desc':'点击关闭面板'},
'2210009':{'WordID':'2210009','order':65,'name':'第一关进入引导','desc':'接下来开始你的表演吧！'},
'2210010':{'WordID':'2210010','order':66,'name':'第一关进入引导','desc':'点击选择第一关'},
'2210011':{'WordID':'2210011','order':67,'name':'第一关进入引导','desc':'她的存在导致整个村的人都无法放假，击败她！拯救我们的伙伴！'},
'2210012':{'WordID':'2210012','order':68,'name':'第一关进入引导','desc':'满地图的鸡儿！ 你们都不放假么？'},
'2210013':{'WordID':'2210013','order':69,'name':'第一关进入引导','desc':'小鸡儿，快把那个人带过来，我给你放假。'},
'2210014':{'WordID':'2210014','order':70,'name':'第一关进入引导','desc':'好的鸡爷！我这就送过去！'},
'2210015':{'WordID':'2210015','order':71,'name':'第一关进入引导','desc':'其他的鸡儿看好那个冒险家！'},
'2210016':{'WordID':'2210016','order':72,'name':'第一关进入引导','desc':'是的！鸡爷！'},
'2210017':{'WordID':'2210017','order':73,'name':'第一关进入引导','desc':'找到铁匠大叔了！不能让他们得逞！'},
'2210018':{'WordID':'2210018','order':74,'name':'第一关进入引导','desc':'去吧！记得注意护盾怪物和多用技能啊。'},
'2210019':{'WordID':'2210019','order':75,'name':'第一关进入引导','desc':'好的，村长！！'},
'2210020':{'WordID':'2210020','order':76,'name':'第一关进入引导','desc':'救命！我要放假！我不要加班！'},
'2210021':{'WordID':'2210021','order':77,'name':'第一关BOSS引导','desc':'坚持住！'},
'2210022':{'WordID':'2210022','order':78,'name':'第一关BOSS引导','desc':'呼，这波窒息的操作差点让我在这交代了。'},
'2210023':{'WordID':'2210023','order':79,'name':'第一关BOSS引导','desc':'别担心，我的操作绝对稳，先回去吧！'},
'2210024':{'WordID':'2210024','order':80,'name':'第一关BOSS引导','desc':'一定要小心！'},
'2210025':{'WordID':'2210025','order':81,'name':'第一关BOSS引导','desc':'老铁快过来！既然救了我，我就帮你来一发感天动地的强化吧！'},
'2210026':{'WordID':'2210026','order':82,'name':'强化装备引导','desc':'先选择一件装备'},
'2210027':{'WordID':'2210027','order':83,'name':'强化装备引导','desc':'点击强化按钮'},
'2210028':{'WordID':'2210028','order':84,'name':'强化装备引导','desc':'再强化一次'},
'2210029':{'WordID':'2210029','order':85,'name':'强化装备引导','desc':'最后一次，武器会更强力'},
'2210030':{'WordID':'2210030','order':86,'name':'强化装备引导','desc':'武器更加锋利了，快去拯救契约商人吧！'},
'2210031':{'WordID':'2210031','order':87,'name':'强化装备引导','desc':'点击返回退出强化界面'},
'2210032':{'WordID':'2210032','order':88,'name':'第二关进入引导','desc':'点击选择第二关'},
'2210033':{'WordID':'2210033','order':89,'name':'第二关进入引导','desc':'来不及解释了！快点开始！'},
'2210034':{'WordID':'2210034','order':90,'name':'第二关进入引导','desc':'咦？被抓住的不是契约商人！'},
'2210035':{'WordID':'2210035','order':91,'name':'第二关进入引导','desc':'哈哈！抓了一个欧洲人！他身上有史诗装备！ '},
'2210036':{'WordID':'2210036','order':92,'name':'第二关进入引导','desc':'打死偷渡海豹！'},
'2210037':{'WordID':'2210037','order':93,'name':'第二关进入引导','desc':'夺它兵器！吸它欧气！非酋部落万岁！'},
'2210038':{'WordID':'2210038','order':94,'name':'第二关进入引导','desc':'夺回属于我们的欧气！'},
'2210039':{'WordID':'2210039','order':95,'name':'第二关进入引导','desc':'非酋要发动围攻了么？出货是欧皇的特权！'},
'2210040':{'WordID':'2210040','order':96,'name':'第二关BOSS引导','desc':'…………'},
'2210041':{'WordID':'2210041','order':97,'name':'第二关BOSS引导','desc':'非洲大酋长！齐鸽丸！'},
'2210042':{'WordID':'2210042','order':98,'name':'第二关BOSS引导','desc':'你到底是谁？'},
'2210043':{'WordID':'2210043','order':99,'name':'第二关BOSS引导','desc':'我是个商人，找到了不少好东西，要看看吗？'},
'2210044':{'WordID':'2210044','order':100,'name':'第二关BOSS引导','desc':'你这根本就是盗墓的黑心商人啊！'},
'2210045':{'WordID':'2210045','order':101,'name':'第二关BOSS引导','desc':'咳咳…快帮我解绑吧'},
'2210046':{'WordID':'2210046','order':102,'name':'第二关BOSS引导','desc':'我也会出售男孩穿的女装，想要么？'},
'2210047':{'WordID':'2210047','order':103,'name':'第二关BOSS引导','desc':'背包里有一些刚拿到的卷轴，该不会是激动人心的同人本？'},
'2210048':{'WordID':'2210048','order':104,'name':'训练系统引导','desc':'这些卷轴包含着古老的力量！他可以用来提升你的能力～'},
'2210049':{'WordID':'2210049','order':105,'name':'训练系统引导','desc':'老夫来教教你如何使用，点击训练'},
'2210050':{'WordID':'2210050','order':106,'name':'训练系统引导','desc':'点击这里训练角色！'},
'2210051':{'WordID':'2210051','order':107,'name':'训练系统引导','desc':'提升训练等级会有固定的武器奖励，还会解锁更酷炫的职业头衔。'},
'2210052':{'WordID':'2210052','order':108,'name':'训练系统引导','desc':'不过现在还是先去把契约商人救出来吧！'},
'2210053':{'WordID':'2210053','order':109,'name':'训练系统引导','desc':'点击确定'},
'2210054':{'WordID':'2210054','order':110,'name':'训练系统引导','desc':'点击返回退出训练界面'},
'2210055':{'WordID':'2210055','order':111,'name':'训练系统引导','desc':'点击返回退出队伍界面'},
'2210056':{'WordID':'2210056','order':112,'name':'训练系统引导','desc':'点击选择第三关'},
'2210057':{'WordID':'2210057','order':113,'name':'第三关进入引导','desc':'让我们赶快去营救契约商人！'},
'2210058':{'WordID':'2210058','order':114,'name':'第三关进入引导','desc':'这次应该不会错了！肯定是契约商人！'},
'2210059':{'WordID':'2210059','order':115,'name':'第三关进入引导','desc':'把他抓到我的办公室！我要让它爱上学习！'},
'2210060':{'WordID':'2210060','order':116,'name':'第三关进入引导','desc':'班主任！我们要如何让孩子爱上学习！'},
'2210061':{'WordID':'2210061','order':117,'name':'第三关进入引导','desc':'当然是让他们爱上GJ！'},
'2210062':{'WordID':'2210062','order':118,'name':'第三关进入引导','desc':'考试强制开始啦！'},
'2210063':{'WordID':'2210063','order':119,'name':'第三关进入引导','desc':'书本居然也受到了影响？'},
'2210064':{'WordID':'2210064','order':120,'name':'第三关BOSS引导','desc':'快来救我！'},
'2210065':{'WordID':'2210065','order':121,'name':'第三关BOSS引导','desc':'我来了！！'},
'2210066':{'WordID':'2210066','order':122,'name':'第三关BOSS引导','desc':'谢谢！我还以为学一辈子习了！'},
'2210067':{'WordID':'2210067','order':123,'name':'第三关BOSS引导','desc':'是不是我再晚来一步，你就会爱上学习？'},
'2210068':{'WordID':'2210068','order':124,'name':'第三关BOSS引导','desc':'不不不！爱上学习是不可能的！'},
'2210069':{'WordID':'2210069','order':125,'name':'雇佣伙伴引导','desc':'快来，现在正好有合适你的小伙伴。'},
'2210070':{'WordID':'2210070','order':126,'name':'雇佣伙伴引导','desc':'这两位的伙伴非常适合你，我就免费介绍啦！'},
'2210071':{'WordID':'2210071','order':127,'name':'雇佣伙伴引导','desc':'艾米是一位远程攻击角色，擅长大范围攻击，配合近战角色最佳'},
'2210072':{'WordID':'2210072','order':128,'name':'雇佣伙伴引导','desc':'而隆则是一位肉搏角色，擅长攻击单体敌人，配合远程角色最佳'},
'2210073':{'WordID':'2210073','order':129,'name':'雇佣伙伴引导','desc':'根据你的战术，选择一位最佳拍档吧 :D'},
'2210074':{'WordID':'2210074','order':130,'name':'雇佣伙伴引导','desc':'喔，有了强力的小伙伴，这样就能拯救更多的人了，快去吧！'},
'2210075':{'WordID':'2210075','order':131,'name':'切换伙伴战斗引导','desc':'你现在可以随时点击这里切换角色'},
'2210076':{'WordID':'2210076','order':132,'name':'切换伙伴战斗引导','desc':'伙伴的技能虽然比主角少，但是都很独特，好好利用吧'},
'2210077':{'WordID':'2210077','order':133,'name':'深渊关卡开启引导','desc':'恭喜您成功开启了深渊模式'},
'2210078':{'WordID':'2210078','order':134,'name':'深渊关卡开启引导','desc':'点击副本入口'},
'2210079':{'WordID':'2210079','order':135,'name':'深渊关卡开启引导','desc':'点击深渊模式按钮'},
'2210080':{'WordID':'2210080','order':136,'name':'深渊关卡开启引导','desc':'深渊模式主要产出高品质装备和稀有材料'},
'2210081':{'WordID':'2210081','order':137,'name':'深渊关卡开启引导','desc':'但是难度你懂的'},
}
    GuideStepFinish= {
'20004':{'X':2,'Y':4,'name':'普通怪物','step':'新手地图1','order':1},
'20006':{'X':2,'Y':6,'name':'高级怪物','step':'新手地图1','order':2},
'10008':{'X':1,'Y':8,'name':'普通怪物','step':'新手地图1','order':3},
'20008':{'X':2,'Y':8,'name':'火盾怪物','step':'新手地图1','order':4},
'30008':{'X':3,'Y':8,'name':'普通怪物','step':'新手地图1','order':5},
'10010':{'X':1,'Y':10,'name':'陶罐','step':'新手地图1','order':6},
'30010':{'X':3,'Y':10,'name':'陶罐','step':'新手地图1','order':7},
'10011':{'X':1,'Y':11,'name':'陶罐','step':'新手地图1','order':8},
'30011':{'X':3,'Y':11,'name':'陶罐','step':'新手地图1','order':9},
'20013':{'X':2,'Y':13,'name':'火盾怪物','step':'新手地图1','order':10},
'20015':{'X':2,'Y':15,'name':'新手2层入口','step':'新手地图1','order':11},
'20002':{'X':2,'Y':2,'name':'陷阱','step':'新手地图2','order':12},
'20005':{'X':2,'Y':5,'name':'火盾怪物','step':'新手地图2','order':13},
'30005':{'X':3,'Y':5,'name':'普通怪物','step':'新手地图2','order':14},
'10006':{'X':1,'Y':6,'name':'普通怪物','step':'新手地图2','order':15},
'30007':{'X':3,'Y':7,'name':'陶罐','step':'新手地图2','order':16},
'10008':{'X':1,'Y':8,'name':'陶罐','step':'新手地图2','order':17},
'30008':{'X':3,'Y':8,'name':'普通怪物','step':'新手地图2','order':18},
'10009':{'X':1,'Y':9,'name':'普通怪物','step':'新手地图2','order':19},
'20009':{'X':2,'Y':9,'name':'火盾怪物','step':'新手地图2','order':20},
'10011':{'X':1,'Y':11,'name':'陶罐','step':'新手地图2','order':21},
'20011':{'X':2,'Y':11,'name':'陷阱','step':'新手地图2','order':22},
'30011':{'X':3,'Y':11,'name':'普通怪物','step':'新手地图2','order':23},
'10013':{'X':1,'Y':13,'name':'普通怪物','step':'新手地图2','order':24},
'30013':{'X':3,'Y':13,'name':'普通怪物','step':'新手地图2','order':25},
'20014':{'X':2,'Y':14,'name':'BOSS','step':'新手地图2','order':26},
'20015':{'X':2,'Y':15,'name':'回城出口','step':'新手地图2','order':27},
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



class BIStageHandler(BaseHandler):
    def sortFunc(self,e1 ,e2 ):
            if e1.get("StageID",None)==None:
                return -1
            elif e2.get("StageID",None)==None:
                return 1

            diff=e1.get("StageID",0)-e2.get("StageID",0)
            return  diff
    @asynchronous
    @gen.coroutine
    def self_get(self):

        stageMap=yield app.DBMgr.getStageDB().select_enter_cnt_as_map()
        stageCompleteMap=yield app.DBMgr.getStageDB().select_complete_cnt_as_map()
        list=[]
        for key in stageMap:
            stage=stageMap.get(key)
            stageComplete=stageCompleteMap.get(key)
            if stageComplete!=None:
                stage['completeCnt']=stageComplete.get('completeCnt')
            else:
                stage['completeCnt']=0
            stage['completeRatio']="%.2f"%(100*float(stage['completeCnt'])/float(stage['enterCount']))
            list.append(stage)


        list=sorted(list,cmp=self.sortFunc,reverse=False)

        self.render("bi_stage_list.html", title="通关日志分析",
                    list=list,
                    Account=self.gmAccount,
                    channelMap=conf.getChannelNameMap())
class BILevelHandler(BaseHandler):
    @asynchronous
    @gen.coroutine
    def self_get(self):

        levelList=yield app.DBMgr.getLevelUpDB().select_level_group()
        list=[]
        i=0
        for info in levelList:
            if i!=len(levelList)-1:
                info['countLevel']=info['countLevel']-levelList[i+1].get("countLevel")
                if info['countLevel']<0:
                    info['countLevel']=0
            i=i+1

            list.append(info)



        self.render("bi_level.html", title="玩家等级分析",
                    list=list,
                    Account=self.gmAccount,
                    channelMap=conf.getChannelNameMap())
class BIDeadHandler(BaseHandler):
    @asynchronous
    @gen.coroutine
    def self_get(self):
        list=yield app.DBMgr.getCharacterDeadDB().select_cnt()
        self.render("bi_dead.html", title="玩家死亡地图分析",
                    list=list,
                    Account=self.gmAccount,
                    channelMap=conf.getChannelNameMap())
class BISkillHandler(BaseHandler):
    @asynchronous
    @gen.coroutine
    def self_get(self):
        list=yield app.DBMgr.getSkillDB().select_cnt()
        self.render("bi_skill.html", title="技能使用分析",
                    list=list,
                    Account=self.gmAccount,
                    channelMap=conf.getChannelNameMap())

class BICurrencyHandler(BaseHandler):
    @asynchronous
    @gen.coroutine
    def self_get(self):
        timeStart = self.get_argument('op-time-start','')
        timeEnd= self.get_argument('op-time-end','')
        channel= self.get_argument('channel','0')
        if self.gmAccount.channel!='0':
            if not channel in self.gmAccount.getChannelList():
                channel= self.gmAccount.channel


        obtainList=yield app.DBMgr.getCurrencyChangeDB().select_stat_obtain(timeStart,timeEnd,channel)
        consumeList=yield app.DBMgr.getCurrencyChangeDB().select_stat_consume(timeStart,timeEnd,channel)
        usercnt=yield app.DBMgr.getUserDB().select_cnt()
        currencyObtainMap={}
        currencyConsumeMap={}
        wordIdMap=yield app.DBMgr.getWordIdMap(1)
        for index, item in enumerate(obtainList):
            source=item.get("Source",0)
            sourceStr=wordIdMap.get(int(source),source)
            item['Source']=sourceStr
            obtainList[index]=item
        for index, item in enumerate(consumeList):
            source=item.get("Source",0)
            sourceStr=wordIdMap.get(int(source),source)
            item['Source']=sourceStr
            consumeList[index]=item


        for e in obtainList:
            currencyType=e.get('CurrencyType')
            currencyInfo=currencyObtainMap.get(currencyType,{})
            currencyInfo['usercnt']=usercnt
            currencyInfo['totalSum']=currencyInfo.get('totalSum',0)+e.get('totalSum')
            currencyObtainMap[currencyType]=currencyInfo
        for index, e in enumerate(obtainList):
            currencyType=e.get('CurrencyType')
            currencyInfo=currencyObtainMap.get(currencyType,{})
            e['usercntTotal']=usercnt
            e['totalSumAll']=currencyInfo.get('totalSum',0)
            e['usercntPercent']="%.2f"%(100*float(e.get('usercnt',0))/float(usercnt)) +"%"
            e['sumPercent']="%.2f"%(100*float(e.get('totalSum',0))/float(currencyInfo.get('totalSum',0))) +"%"
            obtainList[index]=e

        for e in consumeList:
            currencyType=e.get('CurrencyType')
            currencyInfo=currencyConsumeMap.get(currencyType,{})
            currencyInfo['usercnt']=usercnt
            currencyInfo['totalSum']=currencyInfo.get('totalSum',0)+e.get('totalSum')
            currencyConsumeMap[currencyType]=currencyInfo
        for index, e in enumerate(consumeList):
            currencyType=e.get('CurrencyType')
            currencyInfo=currencyConsumeMap.get(currencyType,{})
            e['usercntTotal']=usercnt
            e['totalSumAll']=currencyInfo.get('totalSum',0)
            e['usercntPercent']="%.2f"%(100*float(e.get('usercnt',0))/float(usercnt)) +"%"
            e['sumPercent']="%.2f"%(100*float(e.get('totalSum',0))/float(currencyInfo.get('totalSum',0))) +"%"
            consumeList[index]=e



        currencyConsumeMap={}
        self.render("bi_currency.html", title="货币消耗与产出分析",
                    obtainList=obtainList,
                    consumeList=consumeList,
                    timeStart =timeStart,
                    timeEnd=timeEnd,
                    defaultChannel=channel,
                    Account=self.gmAccount,
                    channelMap=conf.getChannelNameMap())
