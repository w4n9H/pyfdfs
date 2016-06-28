# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: mango
@contact: w4n9@sina.com
@create: 16/1/27


"""

__author__ = "mango"
__version__ = "0.1"


FDFS_CONFIG = {
    "client_path": "/etc/fdfs/client.conf",
    "log_level": 3,
    "tmp_path": "/dev/shm"
}

MYSQL_CONFIG = {
    "host": "192.168.11.129",
    "port": 3306,
    "user": "root",
    "passwd": "test",
    "db_name": "fdfs",
    "table_name": "fdfs_info",
    "max_connections": 5000,
    "connect_timeout": 60,
    "stale_timeout": 55,
    "threadlocals": True,
    "autocommit": True
}


FDFS_DOMAIN = {
    "group1": "http://192.168.11.152",
    "group2": "http://192.168.11.154",
    "group3": "http://192.168.11.159"
}

