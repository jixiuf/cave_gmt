#  -*- coding:utf-8 -*-
import unittest
import dbtemplate
class StringSumTestCase(unittest.TestCase):
    def runTest(self):
        strSum=dbtemplate.StringSum("ab")
        assert strSum.to_sum()==ord('a')+ord('b'), 'string dbtemplate assert false'
        assert strSum.sum_len()==1
# if __name__ == "__main__":
#     unittest.main()
