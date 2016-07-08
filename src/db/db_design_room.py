#  -*- coding:utf-8 -*-
__author__ = 'jixiufeng'

from tornado import  gen
from datetime import datetime, timedelta
import db.dbtemplate.dbtemplate


class BRoomDB:
    def __init__(self,dbtemplate):
        self.dbtemplate=dbtemplate



    def mapRow(self,row):
        kv          ={}
        kv['roomId']=row[0]
        kv['gametype']=row[1]
        kv['roomType']=row[2]
        kv['roomName']=row[3]
        return kv

    @gen.coroutine
    def select_all(self):
        query="select id,game_type,room_type,room_name from b_room "
        res=yield self.dbtemplate.query(query,self.mapRow)
        raise gen.Return(res)
