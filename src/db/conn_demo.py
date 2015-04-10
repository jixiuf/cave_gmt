#! ../../virtual/bin/python
#  -*- coding:utf-8 -*-
from tornado_mysql import pools
from tornado import ioloop, gen
import conn
@gen.coroutine
def test_single():
    pool1=pools.Pool(
        dict(host='127.0.0.1', port=3306, user='th_dev', passwd='th_devpass', db='test'),
        max_idle_connections=1,
        max_recycle_sec=3)
    dt=conn.DatabaseTemplateSingle(pool1)
    yield dt.execDDL("create table if not exists test_python_conn(id int)")
    yield dt.execSql(None,"insert into test_python_conn value(2)")
    def mapRow(row):
        return row[0]
    result=yield dt.query(None,"select id from test_python_conn",mapRow)
    print "single_result",result

@gen.coroutine
def test_sharding():
    pool0=pools.Pool(
        dict(host='127.0.0.1', port=3306, user='th_dev', passwd='th_devpass', db='test'),
        max_idle_connections=1,
        max_recycle_sec=3)
    pool1=pools.Pool(
        dict(host='127.0.0.1', port=3306, user='th_dev', passwd='th_devpass', db='test_1'),
        max_idle_connections=1,
        max_recycle_sec=3)
    dt0=conn.DatabaseTemplateSingle(pool0)
    dt1=conn.DatabaseTemplateSingle(pool1)

    dt=conn.DatabaseTemplateSharding([dt0,dt1])
    yield dt.execDDL("create table if not exists test_python_conn_shard(id int)")
    yield dt.execDDL("truncate table test_python_conn_shard")
    yield dt.execSql(conn.Uint64Sum(1),"insert into test_python_conn_shard value(1)")
    yield dt.execSql(conn.Uint64Sum(2),"insert into test_python_conn_shard value(2)")
    def mapRow(row):
        return row[0]
    result=yield dt.query(conn.Uint64Sum(1),"select id from test_python_conn_shard where id=1",mapRow)
    print "shard_result,len(result) should=1",len(result)
    print "shard_result,should=1,actual=",result[0]
    result=yield dt.query(conn.Uint64Sum(2),"select id from test_python_conn_shard where id=2",mapRow)
    print "shard_result,len(result) should=1",len(result)
    print "shard_result,should=2,actual",result[0]



if __name__ == '__main__':
    test_single()
    test_sharding()
    ioloop.IOLoop.instance().start()
