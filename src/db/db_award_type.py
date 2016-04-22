#  -*- coding:utf-8 -*-
from tornado import  gen
class Award:
    def __init__(self):
        self.id=0
        self.name=''
    def toJsonObj(self):
      data={}
      data["id"]=self.id
      data["name"]=self.name
      return data

class AwardDB:
    def __init__(self,dbtemplate,locale):
        self.dbtemplate=dbtemplate

    def mapRow(self,row):
        a =Award()
        a.id=row[0]
        a.name=row[1]
        return a
    @gen.coroutine
    def select_all(self):
        query="select a.shopid id,w.wordStr name from b_assets a ,b_wordid w where a.nameid=w.wordID"
        res=yield self.dbtemplate.query(query,self.mapRow)
        raise gen.Return(res)
