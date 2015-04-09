# -*- coding:utf-8 -*-

from tornado.test.util import unittest
from base_test import BaseTest
from ping import PingHandler
#TestHandler就是被测试的模块

class PingHandlerTest(BaseTest):
    def test_ping(self):
        # body = ''
        self.http_client.fetch(self.get_url('/ping'), self.stop)
        response = self.wait()
        self.assertEqual(response.code, 200)
        self.assertEqual(response.body, "pong")
if __name__ == '__main__':
    unittest.main()
