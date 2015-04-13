#  -*- coding:utf-8 -*-
import tornado.testing
# import tornado.testing.gen_test
# python -m tornado.testing test_db_presentPacks
import dbtemplate.mock_db
from db_present_pack import PresentPackDB
class PresentPackTestCase(tornado.testing.AsyncTestCase):
    def setUp(self):
        super(PresentPackTestCase, self).setUp()
        self.dbtemplate=dbtemplate.mock_db.mockdbtemplate()
        self.presentPackDB=PresentPackDB(self.dbtemplate)
    @tornado.testing.gen_test
    def test_create(self):
        yield self.presentPackDB.create_table()
        yield self.presentPackDB.truncate_table()
        yield self.presentPackDB.add("name","content",1,"mail")
        data=yield self.presentPackDB.select_all()
        id=data[0].id
        self.assertEqual (1,len(data))
        self.assertEqual ("name",data[0].name )
        self.assertEqual ("content",data[0].content )


        data=yield self.presentPackDB.select_by_status(0)
        self.assertEqual (1,len(data))
        self.assertEqual ("name",data[0].name )
        self.assertEqual ("content",data[0].content )

        yield self.presentPackDB.update_hide(id,1)

        data=yield self.presentPackDB.select_by_id(id)
        self.assertEqual ("name",data.name )
        self.assertEqual ("content",data.content )
        self.assertEqual (1,data.hide )


        # Test contents of response
        # self.assertIn("FriendFeed", response.body)
