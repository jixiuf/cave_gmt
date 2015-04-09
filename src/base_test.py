#  -*- coding:utf-8-unix -*-
# from tornado.options import options
from tornado.testing import AsyncHTTPTestCase
from init import get_test_app

class BaseTest(AsyncHTTPTestCase):
    def setUp(self):
        pass
        super(BaseTest, self).setUp()
    def get_app(self):
        return get_test_app()


