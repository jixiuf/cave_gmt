#! ../virtual/bin/python
#  -*- coding:utf-8 -*-
import unittest
from tornado.test.util import unittest

TEST_MODULES = [
    'db.test_db_permissions',
    'db.dbtemplate.test_sum',
    'test_ping',
]


def all():
    return unittest.defaultTestLoader.loadTestsFromNames(TEST_MODULES)

def main():
    import tornado.testing
    tornado.testing.main()

if __name__ == '__main__':
    main()


