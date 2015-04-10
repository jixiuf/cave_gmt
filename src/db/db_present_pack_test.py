#  -*- coding:utf-8 -*-
import tornado.testing
# import tornado.testing.gen_test
# python -m tornado.testing test_db_presentPacks
import mock_db
from db_present_pack import PresentPackDB
class PresentPackTestCase(tornado.testing.AsyncTestCase):
    def setUp(self):
        super(PresentPackTestCase, self).setUp()
        self.dbtemplate=mock_db.mockdbtemplate()
        self.presentPackDB=PresentPackDB(self.dbtemplate)
    @tornado.testing.gen_test
    def test_create(self):
        yield self.presentPackDB.create_table()
        yield self.presentPackDB.truncate_table()
        cursor=yield self.presentPackDB.add("name","content",1,0)
        data=yield self.presentPackDB.select_all()
        self.assertEqual (1,cursor.rowcount)
        self.assertEqual (1,len(accountList))
        self.assertEqual ("hello",accountList[0].account )
        self.assertEqual ("world",accountList[0].passwd )
        print
        # Test contents of response
        # self.assertIn("FriendFeed", response.body)
