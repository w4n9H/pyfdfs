# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: mango
@contact: w4n9@sina.com
@create: 16/2/29
"""

__author__ = "mango"
__version__ = "0.1"

import peewee
from peewee import MySQLDatabase, CompositeKey
from settings import MYSQL_CONFIG


db = MySQLDatabase(host=MYSQL_CONFIG['host'],
                   port=MYSQL_CONFIG['port'],
                   user=MYSQL_CONFIG['user'],
                   passwd=MYSQL_CONFIG['passwd'],
                   database=MYSQL_CONFIG['db_name'],
                   charset="utf8")


def create_tables():    # 建表
    db.connect()
    db.create_tables([domain_info, fdfs_info])
    db.close()


# noinspection PyPep8Naming,PyMethodMayBeStatic
class fdfs_info(peewee.Model):    # 表名
    # id = peewee.IntegerField(primary_key=True)
    file_name = peewee.FixedCharField(max_length=255)
    file_size = peewee.IntegerField()
    file_md5 = peewee.CharField(default='', max_length=32)
    file_crc32 = peewee.CharField(default='', max_length=8)
    file_group = peewee.CharField(max_length=64)
    file_local_path = peewee.CharField(max_length=255)
    domain_id = peewee.IntegerField()
    #  primary_key  主键
    #  index        索引
    #  unique       约束
    #  default      默认值
    #  max_length   最大长度,CharField 适用

    class Meta:
        database = db    # 连接数据库
        primary_key = CompositeKey('file_name', 'domain_id')
        indexes = ((('domain_id', 'file_name'), True), )    #


# noinspection PyPep8Naming
class domain_info(peewee.Model):
    domain_name = peewee.CharField(max_length=255, unique=True)

    class Meta:
        database = db    # 连接数据库


if __name__ == '__main__':
    create_tables()

