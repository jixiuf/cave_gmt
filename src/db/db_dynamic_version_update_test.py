#  -*- coding:utf-8 -*-
import tornado.testing
# import tornado.testing.gen_test
# python -m tornado.testing test_db_permissions
import dbtemplate.mock_db
from db_dynamic_version_update import DynamicVersionUpdateDB
from db_dynamic_version_update import DynamicVersionUpdate
class DynamicVersionUpdateDBTestCase(tornado.testing.AsyncTestCase):
    def setUp(self):
        super(DynamicVersionUpdateDBTestCase, self).setUp()
        self.dbtemplate=dbtemplate.mock_db.mockdbtemplate()
        self.dynamicVersionUpdateDB=DynamicVersionUpdateDB(self.dbtemplate)
    @tornado.testing.gen_test
    def test_create(self):
        yield self.dynamicVersionUpdateDB.create_table()
        yield self.dynamicVersionUpdateDB.truncate_table()
        info=DynamicVersionUpdate()
        info.channel=1
        info.version=10001
        info.comment="hello"
        info.url="http://baidu.com"
        cursor=yield self.dynamicVersionUpdateDB.add(info)
        # self.assertNotEqual (cursor.lastrowid,0)

        data=yield self.dynamicVersionUpdateDB.select_all()
        self.assertEqual (1,len(data))
        self.assertEqual (info.url,data[0].url)

        info.url="http://google.com"
        cursor=yield self.dynamicVersionUpdateDB.update(info)
        self.assertEqual (1,cursor.rowcount)
        data=yield self.dynamicVersionUpdateDB.select(1,10001)
        self.assertEqual (info.url,data.url)


