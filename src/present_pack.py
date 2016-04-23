#  -*- coding:utf-8 -*-
__author__ = 'jixiufeng'


import utils
from base_handler import BaseHandler
from tornado.web import asynchronous
from tornado import  gen


class PresentPackList(BaseHandler):
    @asynchronous
    @gen.coroutine
    def self_get(self):
        # playerInfo=yield self.application.dbmgr.getUserDB().select_by_uin(144150423530676224)
        # playerInfo=yield self.application.dbmgr.getUserAttrDB(1).select_by_uin(144150423530676224)
        # print playerInfo
        packs=yield self.application.dbmgr.presentPackDB.select_all()
        self.render("present_pack_list.html",title="礼包列表",packs=packs)
class PresentPackHideShow(BaseHandler):
    @asynchronous
    @gen.coroutine
    def self_post(self):
        id=self.get_argument('id')
        hide=self.get_argument('hide')
        self.application.dbmgr.presentPackDB.update_hide(id,hide)
        self.write('success')

class PresentPackAdd(BaseHandler):
    @asynchronous
    @gen.coroutine
    def self_get(self):
        awardList=yield self.application.dbmgr.getAwardDB().select_all()
        data={}
        for a in awardList:
            # 如果 has_id 为true ,则用于处理 装备 卡片等有id 的奖品，以例js 显示field供输入id
            # zjh 项目里所有的奖励乾了是key:value ,无key:id:value的，故此处一直为false
            data[str(a.id)]={"name":a.name,"has_id":"false"}
        print(data)
        self.render("present_pack_add.html",title="礼包打包",awardList=data)
    @asynchronous
    @gen.coroutine
    def self_post(self):
        awardList= self.get_argument('pack_awards')
        packName=self.get_argument('pack_name','')
        packVersion=self.get_argument('version','1')
        # packIcon=self.get_argument('pack_icon')
        status=self.get_argument('status','')
        yield self.application.dbmgr.presentPackDB.add(packName,awardList,packVersion,status)
        # self.render("present_pack_add.html",title="礼包打包")

class PresentPackIdList(BaseHandler):
    def self_get(self):
        self.self_post()

        # 对装备 卡片的奖励类型， 其有对应的装备id 卡片id ,此处用于返回所有的装备id 或卡片id , 以便客户端进行选择
    def self_post(self):
        awardType=self.get_argument('id')
        info = {}
        # 这里只是示范相应的格式
        if awardType==5:
            result = [{"label":"1:装备1","value":"1"},{"label":"2:装备2","value":"2"}]
        else:
            result = [{"label":"1:卡片1","value":"1"},{"label":"2:卡片2","value":"2"}]


        info['action'] = 'success'
        info['award_type'] = awardType
        info['result'] = json.dumps(result)
        self.write(info)


        return
    #     awardType=self.get_argument('id')
    #     if awardType=='5':        # leader
    #         self.id_list_leader()
    #     elif awardType=='6':
    #         self.id_list_hero()


    # @asynchronous
    # @gen.coroutine
    # def id_list_leader(self):
    #     bLeaderList=yield self.application.dbmgr.getDesignLeaderDB().select_all()
    #     info = {}
    #     result = []
    #     for leader in bLeaderList:
    #         data={}
    #         data['label']=str(leader.id)+":"+leader.name
    #         data['value']=leader.id
    #         result.append(data)

    #     print result
    #     info['action'] = 'success'
    #     # info['award_type'] = 5
    #     info['result'] = json.dumps(result)
    #     self.write(info)


    # @asynchronous
    # @gen.coroutine
    # def id_list_hero(self):
    #     bLeaderList=yield self.application.dbmgr.getDesignHeroDB().select_all()
    #     info = {}
    #     result = []
    #     for hero in bLeaderList:
    #         data={}
    #         data['label']=str(hero.id)+":"+hero.name
    #         data['value']=hero.id
    #         result.append(data)

    #     info['action'] = 'success'
    #     info['result'] = json.dumps(result)
    #     self.write(info)


