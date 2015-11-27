#  -*- coding:utf-8 -*-
import tornado.testing
# import tornado.testing.gen_test
# python -m tornado.testing test_db_permissions
import dbtemplate.mock_db
from db_server_version import ServerVersionDB
from db_server_version import ServerVersion
class ServerVersionDBTestCase(tornado.testing.AsyncTestCase):
    def setUp(self):
        super(ServerVersionDBTestCase, self).setUp()
        self.dbtemplate=dbtemplate.mock_db.mockdbtemplate()
        self.serverVersionDB=ServerVersionDB(self.dbtemplate)
    @tornado.testing.gen_test
    def test_create(self):
        yield self.serverVersionDB.create_table()
        yield self.serverVersionDB.truncate_table()
        sv=ServerVersion()
        sv.platform=1
        sv.comments="hello"
        sv.maxVesion=1
        sv.midVersion=2
        sv.minVersion=3
        sv.showVersion="v1.2.3"
        cursor=yield self.serverVersionDB.add(sv)
        # self.assertNotEqual (cursor.lastrowid,0)

        data=yield self.serverVersionDB.select_all()
        self.assertEqual (1,len(data))

        sv.minVersion=4
        sv.showVersion="v1.2.4"
        cursor=yield self.serverVersionDB.update(sv)
        self.assertEqual (1,cursor.rowcount)
        data=yield self.serverVersionDB.select(1)
        self.assertEqual (sv.minVersion,data.minVersion)

        data=yield self.serverVersionDB.select_all()
        self.assertEqual (1,len(data))
        self.assertEqual (sv.minVersion,data[0].minVersion)

