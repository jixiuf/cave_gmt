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
        data['ClientTime']         =row[ 3  ]
        data['Time']   =row[ 4  ]
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



class ItemChangeDB:
    def __init__(self,dbtemplate):
        self.dbtemplate=dbtemplate


    def mapRow(self,row):
        data               ={}
        data['Id']         =row[ 0 ]
        data['Uin']        =row[ 1 ]
        data['SUin']       =row[ 2 ]
        data['ClientTime']       =row[ 3 ]
        data['Time'] =row[ 4 ]
        data['Source']     =row[ 5 ]
        data['ItemID']     =row[ 6 ]
        data['PreCount']   =row[ 7 ]
        data['CurCount']   =row[ 8 ]
        data['Changed']    =row[ 9 ]
        return data


    @gen.coroutine
    def select_all(self,uin,startTime,endTime):
        query="select `Id`, `Uin`, `SUin`, `ClientTime`, `Time`, `Source`, `ItemID`, `PreCount`, `CurCount` ,`Changed` from ItemChange  where Uin=%s and Time>'%s' and Time<'%s' order by Time desc"%(uin,startTime,endTime)
        print(query)
        res=yield self.dbtemplate.query(query,self.mapRow)
        raise gen.Return(res)

class GearGotDB:
    def __init__(self,dbtemplate):
        self.dbtemplate=dbtemplate


    def mapRow(self,row):
        data               ={}
        data['Id']         =row[ 0 ]
        data['Uin']        =row[ 1 ]
        data['SUin']       =row[ 2 ]
        data['ClientTime']       =row[ 3 ]
        data['Time'] =row[ 4 ]
        data['Source']     =row[ 5 ]
        data['InstID']     =row[ 6 ]
        data['ModID']      =row[ 7 ]
        data['BaseID']     =row[ 8 ]
        data['Quality']    =row[ 9 ]
        return data


    @gen.coroutine
    def select_all(self,uin,startTime,endTime):
        query="select `Id`, `Uin`, `SUin`, `ClientTime`, `Time`, `Source`, `InstID`, `ModID`, `BaseID` ,`Quality` from GearGot  where Uin=%s and Time>'%s' and Time<'%s' order by Time desc"%(uin,startTime,endTime)
        print(query)
        res=yield self.dbtemplate.query(query,self.mapRow)
        raise gen.Return(res)



class GearFortifyDB:
    def __init__(self,dbtemplate):
        self.dbtemplate=dbtemplate
    def bool(self,d):
        if d==1:
            return "是"
        return "否"


    def mapRow(self,row):
        data               ={}
        data['Id']          =row[ 0 ]
        data['Uin']         =row[ 1 ]
        data['SUin']        =row[ 2 ]
        data['Time']        =row[ 3 ]
        data['ClientTime']  =row[ 4 ]
        data['Source']      =row[ 5 ]
        data['InstID']      =row[ 6 ]
        data['ModID']       =row[ 7 ]
        data['BaseID']      =row[ 8 ]
        data['CurFortify']  =row[ 9 ]
        data['PreFortify']  =row[10 ]
        data['IsDeleted']   =self.bool(row[11 ])
        data['IsBreak']     =self.bool(row[12 ])
        data['IsProtected'] =self.bool(row[13 ])
        data['IsSuccess']   =self.bool(row[14 ])
        data['Quality']     =row[15 ]

        return data


    @gen.coroutine
    def select_all(self,uin,startTime,endTime):
        query="select `Id`, `Uin`, `SUin`, `ClientTime`, `Time`, `Source`, `InstID`, `ModID`, `BaseID`,CurFortify,PreFortify,IsDeleted,IsBreak,IsProtected,IsSuccess ,`Quality` from GearFortify  where Uin=%s and Time>'%s' and Time<'%s' order by Time desc"%(uin,startTime,endTime)
        print(query)
        res=yield self.dbtemplate.query(query,self.mapRow)
        raise gen.Return(res)





class GearRefineDB:
    def __init__(self,dbtemplate):
        self.dbtemplate=dbtemplate
    def bool(self,d):
        if d==1:
            return "是"
        return "否"


    def mapRow(self,row):
        data               ={}
        data['Id']             =row[ 0 ]
        data['Uin']            =row[ 1 ]
        data['SUin']           =row[ 2 ]
        data['Time']           =row[ 3 ]
        data['ClientTime']     =row[ 4 ]
        data['Source']         =row[ 5 ]
        data['InstID']         =row[ 6 ]
        data['ModID']          =row[ 7 ]
        data['BaseID']         =row[ 8 ]
        data['Quality']        =row[ 9 ]
        data['CurRefineTimes'] =row[10 ]
        data['Operation']      =row[11 ]


        return data


    @gen.coroutine
    def select_all(self,uin,startTime,endTime):
        query="select `Id`, `Uin`, `SUin`, `ClientTime`, `Time`, `Source`, `InstID`, `ModID`, `BaseID`,`Quality`,CurRefineTimes,Operation from GearRefine  where Uin=%s and Time>'%s' and Time<'%s' order by Time desc"%(uin,startTime,endTime)
        print(query)
        res=yield self.dbtemplate.query(query,self.mapRow)
        raise gen.Return(res)

class LevelUpDB:
    def __init__(self,dbtemplate):
        self.dbtemplate=dbtemplate
    def bool(self,d):
        if d==1:
            return "是"
        return "否"


    def mapRow(self,row):
        data               ={}
        data['Id']         =row[ 0 ]
        data['Uin']        =row[ 1 ]
        data['SUin']       =row[ 2 ]
        data['Time']       =row[ 3 ]
        data['ClientTime'] =row[ 4 ]
        data['Source']     =row[ 5 ]
        data['CurLevel']   =row[ 6 ]
        data['PreLevel']   =row[ 7 ]
        data['PreExp']     =row[ 8 ]
        data['CurExp']     =row[ 9 ]
        data['Changed']    =row[10 ]


        return data


    @gen.coroutine
    def select_all(self,uin,startTime,endTime):
        query="select `Id`, `Uin`, `SUin`, `ClientTime`, `Time`, `Source`,CurLevel,PreLevel,PreExp,CurExp,Changed  from PlayerLevelUp  where Uin=%s and Time>'%s' and Time<'%s' order by Time desc"%(uin,startTime,endTime)
        print(query)
        res=yield self.dbtemplate.query(query,self.mapRow)
        raise gen.Return(res)




