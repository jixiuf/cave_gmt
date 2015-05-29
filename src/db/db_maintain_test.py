#  -*- coding:utf-8 -*-
import tornado.testing
# import tornado.testing.gen_test
# python -m tornado.testing test_db_presentPacks
import dbtemplate.mock_db
from datetime import datetime, timedelta
from db_maintain import MaintainDB
class MaintainTestCase(tornado.testing.AsyncTestCase):
    def setUp(self):
        super(MaintainTestCase, self).setUp()
        self.dbtemplate=dbtemplate.mock_db.mockdbtemplate()
        self.maintainDB=MaintainDB(self.dbtemplate)
    @tornado.testing.gen_test
    def test_create(self):
        yield self.maintainDB.create_table()
        yield self.maintainDB.truncate_table()
        now=datetime.now()
        day7FromNow=now+ timedelta(days=7)
        yield self.maintainDB.add("1","content",now,day7FromNow)
        data=yield self.maintainDB.select_all()
        serverId=data[0].serverId
        self.assertEqual (1,len(data))
        self.assertEqual ("content",data[0].content )

        yield self.maintainDB.delete("1")
        data=yield self.maintainDB.select_all()
        self.assertEqual (0,len(data))




        # Test contents of response
        # self.assertIn("FriendFeed", response.body)
