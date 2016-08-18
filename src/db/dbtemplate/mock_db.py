#  -*- coding:utf-8 -*-
from tornado_mysql import pools
import dbtemplate
def mockdbtemplate():
    pool= pools.Pool(
            dict(host="127.0.0.1", port=3306, user="zjh", passwd="zjh!!@@__))", db="test"),
            max_idle_connections=1,
            max_recycle_sec=3)
    return dbtemplate.DatabaseTemplateSingle(pool)

def mockdbtemplateSharding():
    pool0=pools.Pool(
        dict(host='127.0.0.1', port=3306, user='zjh', passwd='zjh!!@@__))', db='test'),
        max_idle_connections=1,
        max_recycle_sec=3)
    pool1=pools.Pool(
        dict(host='127.0.0.1', port=3306, user='zjh', passwd='zjh!!@@__))', db='test_1'),
        max_idle_connections=1,
        max_recycle_sec=3)
    dt0=dbtemplate.DatabaseTemplateSingle(pool0)
    dt1=dbtemplate.DatabaseTemplateSingle(pool1)
    return dbtemplate.DatabaseTemplateSharding([dt0,dt1])
