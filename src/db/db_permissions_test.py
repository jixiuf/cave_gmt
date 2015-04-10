#  -*- coding:utf-8 -*-
import tornado.testing
# import tornado.testing.gen_test
# python -m tornado.testing test_db_permissions
import mock_db
from db_permissions import PermissionsDB
class PermissionsTestCase(tornado.testing.AsyncTestCase):
    def setUp(self):
        super(PermissionsTestCase, self).setUp()
        self.dbtemplate=mock_db.mockdbtemplate()
        self.permissionDB=PermissionsDB(self.dbtemplate)
    @tornado.testing.gen_test
    def test_create(self):
        yield self.permissionDB.create_table()
        yield self.permissionDB.truncate_table()
        cursor=yield self.permissionDB.add("hello","world")
        self.assertNotEqual (cursor.lastrowid,0)
        cursor=yield self.permissionDB.update_level("hello",3)
        self.assertEqual (1,cursor.rowcount)
        # Test contents of response
        # self.assertIn("FriendFeed", response.body)
