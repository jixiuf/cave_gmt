#  -*- coding:utf-8 -*-
from tornado import  gen
import os,sys
# modulepath = os.getcwd()+'/..'
# sys.path.append(modulepath)


class BIUser:
    def toJsonObj(self):
        data={}
        data["day"]=self.day
        data["channel"]=self.channel
        data["newUserCnt"]=self.newUserCnt
        data["activeUserCnt"]=self.activeUserCnt
        data["payUserCnt"]=self.payUserCnt
        data["payNewUserCnt"]=self.payNewUserCnt
        data["money"]=self.money
        data["avgMoney"]="{0:.2f}".format(self.getAvgMoney())
        data["avgMoneyOfPayed"]="{0:.2f}".format(self.getAvgMoneyOfPayed())
        return data
    def getAvgMoney(self):
        if self.activeUserCnt==0:
            return 0
        else:
            return float(self.money)/float(self.activeUserCnt)
    def getAvgMoneyOfPayed(self):
        if self.payUserCnt==0:
            return 0
        else:
            return float(self.money)/float(self.payUserCnt)


    def __init__(self):
        self.day=""
        self.newUserCnt=0
        self.activeUserCnt=0
        self.channel=0
        self.payUserCnt = 0
        self.payNewUserCnt = 0
        self.money = 0
    def __str__(self):
        return "BIUser{day=%s,channel=%d,newUserCnt=%d,activeUserCnt=%d,payUserCnt=%d,payNewUserCnt=%d,money=%d,avgMoney=%d,avgMoneyOfPayed=%d}"%(
            self.day,self.channel,self.newUserCnt,
            self.activeUserCnt,self.payUserCnt,self.payNewUserCnt,self.money,
            self.getAvgMoney(),self.getAvgMoneyOfPayed())

class BIUserDB:
    def __init__(self,dbtemplate):
        self.dbtemplate=dbtemplate

    @gen.coroutine
    def create_table(self):
        query = "create table if not exists bi_user ("\
                "`day` date NOT NULL, " \
                "`channel` int NOT NULL default 0, " \
                "`newUserCnt` int NOT NULL DEFAULT 0 ," \
                "`activeUserCnt` int NOT NULL DEFAULT 0 ," \
                "`payUserCnt` int NOT NULL DEFAULT 0 ," \
                "`payNewUserCnt` int NOT NULL DEFAULT 0 ," \
                "`money` int NOT NULL DEFAULT 0, " \
                "primary key(day,channel)) "\
                "ENGINE = InnoDB CHARACTER SET = utf8"
        yield self.dbtemplate.execDDL(query)
    @gen.coroutine
    def truncate_table(self):
        query="truncate table bi_user "
        yield self.dbtemplate.execDDL(query)


    def mapRow(self,row):
        user=BIUser()
        user.newUserCnt=row[0]
        user.activeUserCnt=row[1]
        user.payUserCnt = row[2]
        user.payNewUserCnt = row[3]
        user.money = row[4]
        user.day = str(row[5])
        user.channel = row[6]

        return user

    @gen.coroutine
    def select_all(self,channel='0'):
        where= " where channel=%s "%(str(channel))

        query="select newUserCnt,activeUserCnt,payUserCnt,payNewUserCnt,money, day,channel from bi_user  %s order by day desc"%(where)
        res=yield self.dbtemplate.query(query,self.mapRow)
        raise gen.Return(res)

    @gen.coroutine
    def add(self,biUser):
        query="insert  into bi_user(day,newUserCnt,activeUserCnt,payUserCnt,payNewUserCnt,money,channel) values('%s',%d,%d,%d,%d,%d,%d) on  duplicate key update newUserCnt=values(newUserCnt),activeUserCnt=values(newUserCnt),payUserCnt=values(payUserCnt),payNewUserCnt=values(payNewUserCnt),money=values(money) "%(
            biUser.day,biUser.newUserCnt,biUser.activeUserCnt,biUser.payUserCnt,biUser.payNewUserCnt,biUser.money,biUser.channel)
        result=yield self.dbtemplate.execSql(query)
        raise gen.Return(result)

