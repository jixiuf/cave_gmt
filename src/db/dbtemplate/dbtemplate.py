#  -*- coding:utf-8 -*-
from tornado import ioloop, gen
import tornado_mysql

class Sum(object):
    def to_sum(self):
        return 0
    def sum_len(self):
        return 0
    def get_sum_by_idx(self,idx):
        return 0

class Uint64Sum(Sum):
    def __init__(self, value):
        self.value = value
    def to_sum(self):
        return int(self.value)
    def sum_len(self):
        return 1
    def get_sum_by_idx(self,idx):
        return self

class StringSum(Sum):
    def __init__(self, value):
        self.value = value
    def to_sum(self):
        sum=0
        for c in self.value:
            sum+=ord(c)
        return sum
    def sum_len(self):
        return 1
    def get_sum_by_idx(self,idx):
        return self

class DatabaseTemplateSingle():
    def __init__(self,dbPool ):
        self._dbPool=dbPool
    def	getDatabaseTemplateShardingBySum(self,sum ) :
        return self
    def getDatabaseTemplateShardingIdxBySum(self,sum):
        return -1
    def	getDatabaseTemplateByShardingIdx(self,idx ) :
        return self
    def	isSharding(self) :
        return False
    def	getWriteDatabaseTemplate(self) :
        return self
    def	getReadDatabaseTemplate(self) :
        return self
    @gen.coroutine
    def execDDL(self,sql):
        yield self._dbPool.execute(sql)
    @gen.coroutine
    def execSql(self,sql,sum=None):
        cur = yield self._dbPool.execute(sql)
        # cursor.lastrowid 如果有auto_increment 列， 此值返回新生成的id
        # cursor.rowcount 返回 影响的行数
        raise gen.Return(cur)
    @gen.coroutine
    def query(self,sql,mapRow=None,sum=None):
        cur=yield self._dbPool.execute(sql)
        result=cur.fetchall()
        if mapRow!=None:
            raise gen.Return(map(mapRow,result))
        raise gen.Return(result)
    @gen.coroutine
    def queryObject(self,sql,mapRow=None,sum=None):
        cur=yield self._dbPool.execute(sql)
        result=cur.fetchone()
        if mapRow!=None:
            if result==None:
                raise gen.Return(None)
            else:
                result=mapRow(result)
                raise gen.Return(result)
        raise gen.Return(result)



class DatabaseTemplateSharding():
    def __init__(self,databaseTemplateList):
        self._databaseTemplateList=databaseTemplateList
    def	getDatabaseTemplateShardingBySum(self,sum) :
        if len(self._databaseTemplateList)==0:
            return self
	idx = sum.to_sum() % len(self._databaseTemplateList)
        return self._databaseTemplateList[idx]
    def getDatabaseTemplateShardingIdxBySum(self,sum):
        if len(self._databaseTemplateList)==0:
            return -1
	return sum.to_sum() % len(self._databaseTemplateList)
    def	getDatabaseTemplateByShardingIdx(self,idx) :
        if idx>=len(self._databaseTemplateList):
            return self
        return self._databaseTemplateList[idx]
    def	isSharding(self) :
        return True
    def	getWriteDatabaseTemplate(self) :
        return self
    def	getReadDatabaseTemplate(self) :
        return self

    @gen.coroutine
    def execDDL(self,sql):
        for dt in self._databaseTemplateList:
            yield dt.execDDL(sql)
    @gen.coroutine
    def execSql(self,sql,sum=None): #
        if sum==None:
            for dt in self._databaseTemplateList:
                cur=yield dt.execSql(sql,sum)
            if len(self._databaseTemplateList)==0:
                raise gen.Return(None)
            raise gen.Return(cur) # useless ,
        elif sum.sum_len()==1:
            sumDt=self.getDatabaseTemplateShardingBySum(sum)
            cur=yield sumDt.execSql(sql,None)
            raise gen.Return(cur) # useless ,
        else:
            idxMap ={}
            for subSumIdx in range(sum.sum_len()):
                subSum=sum.get_sum_by_idx(subSumIdx)
                subSumDtIdx=self.getDatabaseTemplateShardingIdxBySum(subSum)
                subSumDt=self.getDatabaseTemplateShardingBySum(subSum)
                idxMap[subSumDtIdx]=subSumDt
            for subSumDtIdx in idxMap:
                # subSum=sum.get_sum_by_idx(subSumIdx)
                curosr=yield idxMap[subSumDtIdx].execSql(sql,None)
            if len(idMap)==0:
                raise gen.Return(None)
            raise gen.Return(cur) # useless ,


    @gen.coroutine
    def query(self, sql,mapRow=None,sum=None ): #
        if sum == None :                        # 暂不支持在所有分库上支持查询，
            raise gen.Return(None)
        elif sum.sum_len()==1:  # 暂只支持根据sum 在某个特定的分库上执行查询
            result=yield self.getDatabaseTemplateShardingBySum(sum).query(sql,mapRow,sum)
            raise gen.Return(result)
        else:                   # 暂不支持 in(1,2,3) 之类的查询
            raise gen.Return(None)

    @gen.coroutine
    def queryObject(self,sql,mapRow=None,sum=None): #  (self,[], error)
        if sum == None :                        # 暂不支持在所有分库上支持查询，
            raise gen.Return(None)
        elif sum.sum_len()==1:  # 暂只支持根据sum 在某个特定的分库上执行查询
            result=yield self.getDatabaseTemplateShardingBySum(sum).queryObject(sql,mapRow,sum)
            raise gen.Return(result)
        else:                   # 暂不支持 in(1,2,3) 之类的查询
            raise gen.Return(None)
