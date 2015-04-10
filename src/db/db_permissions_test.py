#  -*- coding:utf-8 -*-
import tornado.testing
# import tornado.testing.gen_test
# python -m tornado.testing test_db_permissions
import mock_db
from db_permissions import PermissionDB
from db_permissions import PermissionLevelDB
class PermissionsTestCase(tornado.testing.AsyncTestCase):
    def setUp(self):
        super(PermissionsTestCase, self).setUp()
        self.dbtemplate=mock_db.mockdbtemplate()
        self.permissionDB=PermissionDB(self.dbtemplate)
        self.permissionLevelDB=PermissionLevelDB(self.dbtemplate)
    @tornado.testing.gen_test
    def test_create(self):
        yield self.permissionDB.create_table()
        yield self.permissionDB.truncate_table()
        yield self.permissionLevelDB.create_table()
        yield self.permissionLevelDB.truncate_table()
        cursor=yield self.permissionDB.add("hello","world")
        self.assertNotEqual (cursor.lastrowid,0)
        cursor=yield self.permissionDB.update_level("hello",1)
        self.assertEqual (1,cursor.rowcount)
        cursor=yield self.permissionLevelDB.add(1,"world","urls,urls2")
        accountList=yield self.permissionDB.select("hello")
        self.assertEqual (1,len(accountList))
        self.assertEqual ("hello",accountList[0].account )
        self.assertEqual ("world",accountList[0].passwd )
        print
        # Test contents of response
        # self.assertIn("FriendFeed", response.body)
