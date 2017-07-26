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
        res=yield self.dbtemplate.query(query,self.mapRow)
        raise gen.Return(res)
    @gen.coroutine
    def select_stat_obtain(self,startTime=None ,endTime=None,channel=None):
        def mapRow(row):
            data={}
            data['CurrencyType']=row[0]
            data['Source']=row[1]
            data['usercnt']=row[2]
            data['totalSum']=row[3]
            return data
        where =" "
        if startTime!=None and startTime!='':
            where += "and time >'%s' "%(startTime)
        if endTime!=None and endTime!='':
            where += "and time <'%s' "%(endTime)
        if channel!='0' and channel!=0 and channel!=None:
            where += "and Channel=%d"%(int(channel))


        query=" select  `CurrencyType`,`Source`,count(DISTINCT uin) usercnt, sum(CHANGED) totalSum from `CurrencyChange` where CHANGED>0 %s group by `CurrencyType`,`Source` order by `CurrencyType`,Source"%(where)
        print(query)

        res=yield self.dbtemplate.query(query,mapRow)
        raise gen.Return(res)

    @gen.coroutine
    def select_stat_consume(self,startTime=None ,endTime=None,channel=None):
        def mapRow(row):
            data={}
            data['CurrencyType']=row[0]
            data['Source']=row[1]
            data['usercnt']=row[2]
            data['totalSum']=row[3]
            return data
        where =" "
        if startTime!=None and startTime!='':
            where += "and time >'%s' "%(startTime)
        if endTime!=None and endTime!='':
            where += "and time <'%s' "%(endTime)
        if channel!='0' and channel!=0 and channel!=None:
            where += "and Channel=%d"%(int(channel))
        query=" select  `CurrencyType`,`Source`,count(DISTINCT uin) usercnt, -sum(CHANGED) totalSum from `CurrencyChange` where CHANGED<0 %s group by `CurrencyType`,`Source` order by `CurrencyType`,Source"%(where)
        print(query)
        res=yield self.dbtemplate.query(query,mapRow)
        raise gen.Return(res)
#


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
        res=yield self.dbtemplate.query(query,self.mapRow)
        raise gen.Return(res)
    @gen.coroutine
    def select_level_group(self,):
        def mapRow(row):
            data       ={}
            data['CurLevel'] =row[ 0 ]
            data['countLevel'] =row[ 1 ]
            return data
        query="select CurLevel,count(distinct `Uin`)  as countLevel from PlayerLevelUp  group by CurLevel order by CurLevel asc"
        res=yield self.dbtemplate.query(query,mapRow)
        raise gen.Return(res)




class PartnerDB:
    def __init__(self,dbtemplate):
        self.dbtemplate=dbtemplate
    def bool(self,d):
        if d==1:
            return "是"
        return "否"


    def mapRow(self,row):
        data               ={}
        data['Id']            =row[ 0 ]
        data['Uin']           =row[ 1 ]
        data['SUin']          =row[ 2 ]
        data['ClientTime']    =row[ 3 ]
        data['Time']          =row[ 4 ]
        data['PartnerID']     =row[ 5 ]
        data['FromPartnerID'] =row[ 6 ]
        data['Operation']     =row[ 7 ]


        return data


    @gen.coroutine
    def select_all(self,uin,startTime,endTime):
        query="select `Id`, `Uin`, `SUin`, `ClientTime`, `Time`, PartnerID,FromPartnerID,Operation  from Partner  where Uin=%s and Time>'%s' and Time<'%s' order by Time desc"%(uin,startTime,endTime)
        res=yield self.dbtemplate.query(query,self.mapRow)
        raise gen.Return(res)

class GuideDB:
    def __init__(self,dbtemplate):
        self.dbtemplate=dbtemplate

    def mapRow(self,row):
        data           ={}
        data['WordID'] =row[ 0 ]
        data['count']  =row[ 1 ]
        return data

    def mapRow2(self,row):
        data           ={}
        data['X'] =row[ 0 ]
        data['Y'] =row[ 1]
        data['count']  =row[ 2]
        data['Key']  =str(data['X']*10000+data['Y'])

        return data


    @gen.coroutine
    def select_cnt_map(self,):
        query="select WordID,count(distinct `Uin`) as count  from GuideStepFinish group by WordID"
        res=yield self.dbtemplate.query(query,self.mapRow)
        data={}
        for e in res:
            data[str(e['WordID'])]=e
        raise gen.Return(data)

    @gen.coroutine
    def select_cnt_2_map(self):
        query="select X,Y,count(`Id`) as count  from GuideActorDestroy group by x,y"
        res=yield self.dbtemplate.query(query,self.mapRow2)
        data={}
        for e in res:
            data[e['Key']]=e
            print(e['Key'])
        raise gen.Return(data)


class StageDB:
    def __init__(self,dbtemplate):
        self.dbtemplate=dbtemplate

    @gen.coroutine
    def select_enter_cnt_as_map(self):
        query="select `StageID`,`StageName`,count(distinct Uin) as userEnterCnt,count(Id) as enterCount from `StageComplete` where `Source`='EnterStage' group by `StageID`,StageName"
        def mapRow(row):
            data              ={}
            data['StageID']    =row[ 0 ]
            data['StageName']  =row[ 1 ]
            data['userCount']  =row[ 2 ]
            data['enterCount'] =row[ 3 ]
            return data
        res=yield self.dbtemplate.query(query,mapRow)
        data={}
        for e in res:
            data[str(e['StageID'])]=e

        raise gen.Return(data)
    @gen.coroutine
    def select_complete_cnt_as_map(self):
        query="select `StageID`,count(Id) as completeCnt from `StageComplete` where `Source`='Complete' group by `StageID`"
        def mapRow(row):
            data              ={}
            data['StageID']    =row[ 0 ]
            data['completeCnt']=row[ 1 ]
            return data

        res=yield self.dbtemplate.query(query,mapRow)
        data={}
        for e in res:
            data[str(e['StageID'])]=e
        raise gen.Return(data)

class CharacterDeadDB:
    def __init__(self,dbtemplate):
        self.dbtemplate=dbtemplate

    @gen.coroutine
    def select_cnt(self):
        query="select MapInfoID,count(Id) as cnt from `CharacterDead` group by `MapInfoID` order by cnt desc"
        def mapRow(row):
            data              ={}
            data['MapInfoID'] =row[ 0 ]
            data['cnt']       =row[ 1 ]
            return data
        res=yield self.dbtemplate.query(query,mapRow)
        raise gen.Return(res)

class SkillDB:
    def __init__(self,dbtemplate):
        self.dbtemplate=dbtemplate

    @gen.coroutine
    def select_cnt(self):
        query="select SkillID,count(Id) as cnt from `CastSkill` group by `SkillID` order by cnt desc"
        def mapRow(row):
            data              ={}
            data['SkillID'] =row[ 0 ]
            data['cnt']       =row[ 1 ]
            return data
        res=yield self.dbtemplate.query(query,mapRow)
        raise gen.Return(res)
