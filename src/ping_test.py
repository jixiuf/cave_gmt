# -*- coding:utf-8 -*-
from tornado.test.util import unittest
from base_test import BaseTest
from ping import PingHandler
from tornado_mysql import pools
# from db.conn import *
#TestHandler就是被测试的模块

class PingHandlerTest(BaseTest):
    def test_ping(self):
        # body = ''
        self.http_client.fetch(self.get_url('/ping'), self.stop)
        response = self.wait()
        self.assertEqual(response.code, 200)
        self.assertEqual(response.body, "pong")
        self.assertEqual(response.body, "pong")
