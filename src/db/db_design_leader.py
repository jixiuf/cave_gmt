#  -*- coding:utf-8 -*-

from tornado import gen
class DesignBLeader:
    def __init__(self):
        self.id=0
        self.sameGroupId=0
        self.heroType=0
        self.name=""
class DesignBLeaderDB:
    def __init__(self,dbtemplate,locale):
        self.dbtemplate=dbtemplate
        self.locale=locale
    def mapRow(self,row):
        rec             = DesignBLeader()
        rec.id          = row[0]
        rec.sameGroupId = row[1]
        rec.heroType    = row[2]
        rec.name    = row[3]
        return rec

    @gen.coroutine
    def select_all(self):
        query="select l.Id,l.SameGroup,l.HeroType,ifnull(w.wordStr,'') wordStr from b_leader l left outer join b_wordid_%s w on l.NameId=w.wordID "%(self.locale)
        res=yield self.dbtemplate.query(query,self.mapRow)
        raise gen.Return(res)
