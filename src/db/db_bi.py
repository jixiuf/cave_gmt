#  -*- coding:utf-8 -*-
from tornado import  gen
from datetime import datetime, timedelta

class CurrencyChangeDB:
    def __init__(self,dbtemplate):
        self.dbtemplate=dbtemplate


    def mapRow(self,row):
        data={}
        data['Id']           =row[ 0  ]
        data['Uin']          =row[ 1  ]
        data['SUin']         =row[ 2  ]
        data['Time']         =row[ 3  ]
        data['ClientTime']   =row[ 4  ]
        data['Source']       =row[ 5  ]
        data['CurrencyType'] =row[ 6  ]
        data['CurAmount']    =row[ 7  ]
        data['Changed']      =row[ 8  ]
        return data

    @gen.coroutine
    def truncate_table(self):
        query="truncate table CurrencyChange "
        yield self.dbtemplate.execDDL(query)

    @gen.coroutine
    def select_all(self,uin,startTime,endTime):
        query="select `Id`, `Uin`, `SUin`, `ClientTime`, `Time`, `Source`, `CurrencyType`, `CurAmount`, `Changed` from CurrencyChange  where Uin=%s and Time>'%s' and Time<'%s' order by Time desc"%(uin,startTime,endTime)
        print(query)
        res=yield self.dbtemplate.query(query,self.mapRow)
        raise gen.Return(res)

