#  -*- coding:utf-8 -*-
import unittest
import conn
class StringSumTestCase(unittest.TestCase):
    def runTest(self):
        strSum=conn.StringSum("ab")
        assert strSum.to_sum()==ord('a')+ord('b'), 'string conn assert false'
        assert strSum.sum_len()==1
if __name__ == "__main__":
    unittest.main()
