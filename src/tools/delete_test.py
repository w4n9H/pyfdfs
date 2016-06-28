# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: mango
@contact: w4n9@sina.com
@create: 16/3/29
删除测试
"""

__author__ = "mango"
__version__ = "0.1"

from prettytable import PrettyTable
from multiprocessing import Manager, Pool
from multiprocessing.pool import ApplyResult
import pyfdfs_lib
import requests
import time


class DeleteTest(object):
    def __init__(self, delete_host, domain, limit):
        self.start_time = time.time()
        self.delete_host = delete_host
        self.domain = domain
        self.limit = limit
        self.delete_num = 0
        self.success = 0
        self.fail = 0

    def delete_file(self):
        delete_client = pyfdfs_lib.PyFdfsLib(self.delete_host)
        while 1:
            delete_list_stat, delete_list_info = delete_client.fdfs_list_file(self.domain, self.limit)
            if delete_list_stat:
                if isinstance(delete_list_info, list):
                    self.delete_num += len(delete_list_info)
                    for i in delete_list_info:
                        delete_stat, delete_info = delete_client.fdfs_delete_file(self.domain, i)
                        if delete_stat:
                            self.success += 1
                        else:
                            self.fail += 1
            else:
                break
        use_time = time.time() - self.start_time
        print "delete_count:%s, success:%s, fail:%s, use_time:%s" % (self.delete_num, self.success, self.fail, use_time)


if __name__ == '__main__':
    d = DeleteTest('', '', '')