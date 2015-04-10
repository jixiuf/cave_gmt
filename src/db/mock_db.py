#  -*- coding:utf-8 -*-
from tornado_mysql import pools
import dbtemplate.dbtemplate
def mockdbtemplate():
    pool= pools.Pool(
            dict(host="127.0.0.1", port=3306, user="th_dev", passwd="th_devpass", db="test"),
            max_idle_connections=1,
            max_recycle_sec=3)
    return dbtemplate.dbtemplate.DatabaseTemplateSingle(pool)

