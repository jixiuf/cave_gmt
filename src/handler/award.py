#  -*- coding:utf-8 -*-
__author__ = 'jixiufeng'


from handler.base import BaseHandler
from tornado import  gen
from tornado.web import asynchronous
import app
import json
class AwardIdList(BaseHandler):
    @asynchronous
    @gen.coroutine
    def self_post(self):
        awardList=yield app.DBMgr.getAwardDB().select_all()
        data={}
        for a in awardList:
            # 如果 has_id 为true ,则用于处理 装备 卡片等有id 的奖品，以例js 显示field供输入id
            # zjh 项目里所有的奖励乾了是key:value ,无key:id:value的，故此处一直为false
            data[str(a.id)]={"name":a.name,"has_id":"false"}
        info={}
        info['action'] = 'success'
        info['result'] = json.dumps(data)
        self.write(info)


class AwardSubIdList(BaseHandler):
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
    #     bLeaderList=yield app.DBMgr.getDesignLeaderDB().select_all()
    #     info = {}
    #     result = []
    #     for leader in bLeaderList:
    #         data={}
    #         data['label']=str(leader.id)+":"+leader.name
    #         data['value']=leader.id
    #         result.append(data)

    #     info['action'] = 'success'
    #     # info['award_type'] = 5
    #     info['result'] = json.dumps(result)
    #     self.write(info)


    # @asynchronous
    # @gen.coroutine
    # def id_list_hero(self):
    #     bLeaderList=yield app.DBMgr.getDesignHeroDB().select_all()
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


