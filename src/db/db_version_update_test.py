#  -*- coding:utf-8 -*-
import tornado.testing
# import tornado.testing.gen_test
# python -m tornado.testing test_db_permissions
import dbtemplate.mock_db
from db_version_update import VersionUpdateDB
from db_version_update import VersionUpdate
class VersionUpdateDBTestCase(tornado.testing.AsyncTestCase):
    def setUp(self):
        super(VersionUpdateDBTestCase, self).setUp()
        self.dbtemplate=dbtemplate.mock_db.mockdbtemplate()
        self.versionUpdateDB=VersionUpdateDB(self.dbtemplate)
    @tornado.testing.gen_test
    def test_create(self):
        yield self.versionUpdateDB.create_table()
        yield self.versionUpdateDB.truncate_table()
        info=VersionUpdate()
        info.channel=1
        info.os=1
        info.comments="hello"
        info.url="http://baidu.com"
        cursor=yield self.versionUpdateDB.add(info)
        # self.assertNotEqual (cursor.lastrowid,0)

        data=yield self.versionUpdateDB.select_all()
        self.assertEqual (1,len(data))

        info.url="http://google.com"
        cursor=yield self.versionUpdateDB.update(info)
        self.assertEqual (1,cursor.rowcount)
        data=yield self.versionUpdateDB.select(1)
        self.assertEqual (info.url,data.url)

        data=yield self.versionUpdateDB.select_all()
        self.assertEqual (1,len(data))
        self.assertEqual (info.url,data[0].url)

