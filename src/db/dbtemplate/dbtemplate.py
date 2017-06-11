#  -*- coding:utf-8 -*-
from tornado import ioloop, gen
import tornado_mysql
import traceback
from tornado_mysql import pools,OperationalError

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
# class DBConfigList:
#     def __init__(self,dbConfigObjList):
#         self.dbConfigObjList=dbConfigObjList
#     # def getDatabaseTemplate(self):  # sharding
#     #     dtList=[]
#     #     for dbConfigObj in self.dbConfigObjList:
#     #         dtList.append(dbConfigObj.getDatabaseTemplate())
#     #     return DatabaseTemplateSharding(dtList)
#     def getDBConfigList(self):
#         return self.dbConfigObjList

class DBConfig:
    def __init__(self,user,passwd,host,database,port):
        self.user=user
        self.passwd=passwd
        self.host=host
        self.database=database
        self.port=port
    def __str__(self):
        return "user=%s,passwd=%s,host=%s,database=%s,port=%d"%(self.user,self.passwd,self.host,self.database,self.port)
    def getUser(self):
        return self.user
    def getPasswd(self):
        return self.passwd
    def getHost(self):
        return self.host
    def getDatabase(self):
        return self.database
    def getPort(self):
        return self.port
    def conn(self):
        return pools.Pool(
            dict(host=self.getHost(),
                 port=self.getPort(),
                 user=self.getUser(),
                 passwd=self.getPasswd(),
                 db=self.getDatabase(),
                 charset='utf8mb4',
            ),
            max_idle_connections=1,
            max_recycle_sec=3)
    # def getDatabaseTemplate(self) :
    #     pool=self.conn()
    #     return DatabaseTemplateSingle(pool)

class DatabaseTemplateSingle():
    def __init__(self,dbConfig ):
        self.dbConfig=dbConfig
        self._dbPool=self.dbConfig.conn()
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
    def	__exec(self,sql):
        try:
            data=self._dbPool.execute(sql)
            return data
        # except OperationalError as error:
        except Exception, error:
            print('mmmmmmerrormsg\t%s' % (str(error),))
            print('mmmmmmmmerrortrace\t%s' % (str(traceback.format_exc()),))
            return None
    @gen.coroutine
    def execDDL(self,sql):
        yield self.__exec(sql)
    @gen.coroutine
    def execSql(self,sql,sum=None):
        cur = yield self.__exec(sql)
        raise gen.Return(cur)
        # cursor.lastrowid 如果有auto_increment 列， 此值返回新生成的id
        # cursor.rowcount 返回 影响的行数
    @gen.coroutine
    def query(self,sql,mapRow=None,sum=None):
        cur=yield self.__exec(sql)
        result=cur.fetchall()
        yield cur.close()
        if mapRow!=None:
            raise gen.Return(map(mapRow,result))
        raise gen.Return(result)
    @gen.coroutine
    def queryObject(self,sql,mapRow=None,sum=None):
        cur=yield self.__exec(sql)
        result=cur.fetchone()
        yield cur.close()
        if mapRow!=None:
            if result==None:
                raise gen.Return(None)
            else:
                result=mapRow(result)
                raise gen.Return(result)
        raise gen.Return(result)



class DatabaseTemplateSharding():
    def __init__(self,dbConfigObjList):
        dtList=[]
        for dbConfigObj in dbConfigObjList:
            dtList.append(DatabaseTemplateSingle(dbConfigObj))
        # return DatabaseTemplateSharding(dtList)
        self._databaseTemplateList=dtList
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
            result=[]
            for dt in self._databaseTemplateList:
                result1= yield dt.query(sql,mapRow,sum)
                if result1!=None:
                    result.extend(result1)

            raise gen.Return(result)
        elif sum.sum_len()==1:  # 暂只支持根据sum 在某个特定的分库上执行查询
            result=yield self.getDatabaseTemplateShardingBySum(sum).query(sql,mapRow,sum)
            raise gen.Return(result)
        else:                   # 暂不支持 in(1,2,3) 之类的查询
            raise gen.Return(None)

    @gen.coroutine
    def queryObject(self,sql,mapRow=None,sum=None): #  (self,[], error)
        if sum == None :                        # 暂不支持在所有分库上支持查询，
            for dt in self._databaseTemplateList:
                result1= yield dt.queryObject(sql,mapRow,sum)
                if result1!=None:
                    raise gen.Return(result1)
            raise gen.Return(None)
        elif sum.sum_len()==1:  # 暂只支持根据sum 在某个特定的分库上执行查询
            result=yield self.getDatabaseTemplateShardingBySum(sum).queryObject(sql,mapRow,sum)
            raise gen.Return(result)
        else:                   # 暂不支持 in(1,2,3) 之类的查询
            raise gen.Return(None)
