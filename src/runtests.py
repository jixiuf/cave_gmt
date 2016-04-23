#  -*- coding:utf-8 -*-
__author__ = 'jixiufeng'

import unittest
from tornado.test.util import unittest

TEST_MODULES = [
    'db.dbtemplate.dbtemplate_test',
    'db.dbtemplate.sum_test',
    'db.db_permissions_test',
    'db.db_present_pack_test',
    'db.db_maintain_test',
    'db.db_server_version_test',
    "db.db_version_update_test",
    "db.db_dynamic_version_update_test",
    "db.db_user_test",
    'handler.ping_test',
]


def all():
    return unittest.defaultTestLoader.loadTestsFromNames(TEST_MODULES)

def main():
    import tornado.testing
    tornado.testing.main()

if __name__ == '__main__':
    main()


