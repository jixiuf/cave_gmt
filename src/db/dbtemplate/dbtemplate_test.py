#  -*- coding:utf-8 -*-
from tornado_mysql import pools
from tornado import ioloop, gen
import tornado.testing
import dbtemplate
import mock_db
class DBTemplateSingleTestCase(tornado.testing.AsyncTestCase):
    def setUp(self):
        super(DBTemplateSingleTestCase, self).setUp()
        self.dbtemplate=mock_db.mockdbtemplate()

    @tornado.testing.gen_test
    def test_single(self):
        yield self.dbtemplate.execDDL("create table if not exists test_python_conn(id int)")
        yield self.dbtemplate.execDDL("truncate table test_python_conn")
        yield self.dbtemplate.execSql("insert into test_python_conn value(2)")
        yield self.dbtemplate.execSql("insert into test_python_conn value(3)")

        # query  no mapRow
        result=yield self.dbtemplate.query("select id from test_python_conn order by id asc")
        self.assertEqual(2,len(result))
        self.assertEqual(2,result[0][0])
        self.assertEqual(3,result[1][0])

        def mapRow(row):
            return row[0]
        # query with mapRow
        result=yield self.dbtemplate.query("select id from test_python_conn order by id asc",mapRow)
        self.assertEqual(2,len(result))
        self.assertEqual(2,result[0])
        self.assertEqual(3,result[1])


        # queryObject with mapRow
        result=yield self.dbtemplate.queryObject("select id from test_python_conn where id=2",mapRow)
        self.assertEqual(2,result)

        # queryObject with mapRow and  no result return (return None)
        result=yield self.dbtemplate.queryObject("select id from test_python_conn where id=40000",mapRow) # not exists
        self.assertEqual(None,result)

        # queryObject with mapRow and
        result=yield self.dbtemplate.queryObject("select 1",mapRow) #
        self.assertEqual(1,result)
        result=yield self.dbtemplate.queryObject("select 1") #
        self.assertEqual(1,result[0])


class DBTemplateShardingTestCase(tornado.testing.AsyncTestCase):
    def setUp(self):
        super(DBTemplateShardingTestCase, self).setUp()
        self.dbtemplate=mock_db.mockdbtemplateSharding()

    @tornado.testing.gen_test
    def test_sharding(self):
        yield self.dbtemplate.execDDL("create table if not exists test_python_conn_shard(id int)")
        yield self.dbtemplate.execDDL("truncate table test_python_conn_shard")
        # insert with sharding ,两条数据会插入到不同的库里
        yield self.dbtemplate.execSql("insert into test_python_conn_shard value(1)",dbtemplate.Uint64Sum(1))
        yield self.dbtemplate.execSql("insert into test_python_conn_shard value(2)",dbtemplate.Uint64Sum(2))
        def mapRow(row):
            return row[0]
        result=yield self.dbtemplate.query("select id from test_python_conn_shard where id=1",mapRow,dbtemplate.Uint64Sum(1))
        self.assertEqual(1,len(result))
        self.assertEqual(1,result[0])
        result=yield self.dbtemplate.query("select id from test_python_conn_shard where id=2",mapRow,dbtemplate.Uint64Sum(2))
        self.assertEqual(1,len(result))
        self.assertEqual(2,result[0])

        result=yield self.dbtemplate.query("select id from test_python_conn_shard ",mapRow)
        self.assertEqual(2,len(result))
        self.assertEqual(2,result[0])
        self.assertEqual(1,result[1])


        result=yield self.dbtemplate.queryObject("select id from test_python_conn_shard where id=1",mapRow,dbtemplate.Uint64Sum(1))
        self.assertEqual(1,result)
        result=yield self.dbtemplate.queryObject("select id from test_python_conn_shard where id=2",mapRow,dbtemplate.Uint64Sum(2))
        self.assertEqual(2,result)

        result=yield self.dbtemplate.queryObject("select id from test_python_conn_shard where id=1",mapRow)
        self.assertEqual(1,result)
        result=yield self.dbtemplate.queryObject("select id from test_python_conn_shard where id=2",mapRow)
        self.assertEqual(2,result)
