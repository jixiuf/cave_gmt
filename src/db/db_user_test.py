#  -*- coding:utf-8 -*-
import tornado.testing
# import tornado.testing.gen_test
# python -m tornado.testing db_user_test
import dbtemplate.mock_db
from db.db_user import UserDB
class UserDBTestCase(tornado.testing.AsyncTestCase):
    def setUp(self):
        super(UserDBTestCase, self).setUp()
        self.dbtemplate=dbtemplate.mock_db.mockdbtemplate()
        self.userDB=UserDB(self.dbtemplate)
    @tornado.testing.gen_test
    def test_create(self):
        yield self.userDB.create_table()
        yield self.userDB.truncate_table()
        cursor=yield self.userDB.add(3)
        # self.assertNotEqual (cursor.lastrowid,0)


        data=yield self.userDB.select_by_uin(3)
        self.assertEqual (3,data.uin)
        suin=data.suin

        uin=yield self.userDB.select_uin_by_suin(suin)
        self.assertEqual (3,uin)

        uin=yield self.userDB.select_uin_by_suin("3333")
        self.assertEqual (None,uin)

        data=yield self.userDB.select_uin_list_by_suins(str(suin))
        self.assertEqual (1,len(data))
        self.assertEqual (3,data[0])
