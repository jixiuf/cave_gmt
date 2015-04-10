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


class IDatabaseTemplate(object):
    """base class"""
    def	getDatabaseTemplateShardingBySum(self,sum ) :#(self,DatabaseTemplate, int, error):
        block
    def	getDatabaseTemplateShardingIdxBySum(self,sum ) :#(self,DatabaseTemplate, int, error):
        block
    def	getDatabaseTemplateByShardingIdx(self,idx ) :#(self,DatabaseTemplate, error):
        block
    def	isSharding(self) :
        block
    def	getWriteDatabaseTemplate(self) :
        block
    def	getReadDatabaseTemplate(self) :
        block
    @gen.coroutine
    def execDDL(self,sql):            # err
        block
    @gen.coroutine
    def execSql(self,sum ,sql):           # err
        block
    # def execSqlForResult(self,sum , sql,callback): #  (self,sql.Result, error)
    @gen.coroutine
    def query(self,sum , sql ): #  (self,[], error)
        block
    # def close(self): #  (self,obj, error)


class DatabaseTemplateSingle(IDatabaseTemplate):
    def __init__(self,dbPool ):
        self._dbPool=dbPool
    def	getDatabaseTemplateShardingBySum(self,sum ) :#(self,DatabaseTemplate, int, error):
        return self
    def getDatabaseTemplateShardingIdxBySum(self,sum):
        return -1
    def	getDatabaseTemplateByShardingIdx(self,idx ) :#(self,DatabaseTemplate, error):
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
    def execSql(self,sum ,sql):           # err
        cur = yield self._dbPool.execute(sql)
        # cursor.lastrowid 如果有auto_increment 列， 此值返回新生成的id
        # cursor.rowcount 返回 影响的行数
        raise gen.Return(cur)
    @gen.coroutine
    def query(self,sum , sql,mapRow): #  (self,[], error)
        cur=yield self._dbPool.execute(sql)
        if mapRow!=None:
            raise gen.Return(map(mapRow,cur))
        raise gen.Return(cur)



class DatabaseTemplateSharding(IDatabaseTemplate):
    def __init__(self,databaseTemplateList):
        self._databaseTemplateList=databaseTemplateList
    def	getDatabaseTemplateShardingBySum(self,sum) : # return sharding databasetemplate
        if len(self._databaseTemplateList)==0:
            return self
	idx = sum.to_sum() % len(self._databaseTemplateList)
        return self._databaseTemplateList[idx]
    def getDatabaseTemplateShardingIdxBySum(self,sum):
        if len(self._databaseTemplateList)==0:
            return -1
	return sum.to_sum() % len(self._databaseTemplateList)
    def	getDatabaseTemplateByShardingIdx(self,idx) :#(self,DatabaseTemplate, error):
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
    def execSql(self,sum ,sql):           # err
        if sum==None:
            for dt in self._databaseTemplateList:
                cur=yield dt.execSql(sum,sql)
            if len(self._databaseTemplateList)==0:
                raise gen.Return(None)
            raise gen.Return(cur) # useless ,
        elif sum.sum_len()==1:
            sumDt=self.getDatabaseTemplateShardingBySum(sum)
            cur=yield sumDt.execSql(None,sql)
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
                curosr=yield idxMap[subSumDtIdx].execSql(None,sql)
            if len(idMap)==0:
                raise gen.Return(None)
            raise gen.Return(cur) # useless ,


    @gen.coroutine
    def query(self,sum , sql,callback ): #  (self,[], error)
        if sum == None :
            block
        elif sum.sum_len()==1:
            result=yield self.getDatabaseTemplateShardingBySum(sum).query(sum,sql,callback)
            raise gen.Return(result)
