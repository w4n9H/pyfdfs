# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: mango
@contact: w4n9@sina.com
@create: 16/2/15
上传测试脚本
"""

__author__ = "mango"
__version__ = "0.1"


import os
import sys
import uuid
import time
from multiprocessing import Process, Manager

import requests
from prettytable import PrettyTable


class FDFSUploadTest(object):
    def __init__(self, upload_url, upload_file_size, upload_number, upload_user, upload_time):
        """
        FDFS 上传测试类
        :param upload_url: 上传url str
        :param upload_file_size: 上传文件大小(兆) int
        :param upload_number: 上传文件数量 int
        :param upload_user: 上传进程,模拟多用户 int
        :param upload_time: 上传间隔时间
        :return:
        """
        self.upload_url = upload_url
        self.upload_file_size = upload_file_size
        self.upload_number = upload_number
        self.upload_user = upload_user
        self.upload_time = upload_time
        self.upload_success = 0
        self.upload_fail = 0

    def create_file(self):
        """
        生成指定大小的临时文件
        :return:
        """
        try:
            parent, bindir = os.path.split(os.path.dirname(os.path.abspath(sys.argv[0])))
            file_dir = os.path.join(parent, bindir)
            file_path = os.path.join(file_dir, str(uuid.uuid4())[:15])
            with open(file_path, 'w') as fp:
                fp.seek(1024 * 1024 * self.upload_file_size)    # 以兆为单位
                fp.write('\x00')
        except Exception as error:
            return False, str(error)
        return True, file_path

    def upload_tmp_file(self):
        """
        上传临时生成文件
        :return:
        """
        file_status, file_path = self.create_file()
        if file_status:
            files = {'file': open(file_path, 'rb')}
            r = requests.post(self.upload_url, files=files)
            os.remove(file_path)
            if r.status_code == 200:
                return True
            else:
                return False
        else:
            return False

    def upload_one_user(self, q):
        for i in range(self.upload_number):
            if self.upload_tmp_file():
                q.put(0)
                time.sleep(self.upload_time)
            else:
                q.put(1)

    def upload_test(self):
        start_time = time.time()
        q = Manager().Queue()
        plist = []
        for i in range(self.upload_user):
            proc = Process(target=self.upload_one_user, args=(q,))
            plist.append(proc)
        for proc in plist:
            proc.start()
        for proc in plist:
            proc.join()
        while True:
            if q.empty():
                break
            else:
                if q.get() == 0:
                    self.upload_success += 1
                else:
                    self.upload_fail += 1
        use_time = time.time() - start_time
        table = PrettyTable(["key", "value"])
        table.add_row(["One File Size (M)", self.upload_file_size])
        table.add_row(["All File Size (M)", self.upload_file_size * self.upload_number * self.upload_user])
        table.add_row(["Process Count(user)", self.upload_user])
        table.add_row(["Upload Count", self.upload_number * self.upload_user])
        table.add_row(["Interval Time(s)", self.upload_time])
        table.add_row(["Success count", self.upload_success])
        table.add_row(["Fail count", self.upload_fail])
        table.add_row(["Success ratio (%)",
                       (round(self.upload_success / float(self.upload_number * self.upload_user), 4) * 100)])
        table.add_row(["Use time (s)", "%.2f" % use_time])
        print table


if __name__ == '__main__':
    fdfs = FDFSUploadTest('http://192.168.11.77:8080/v1/upload?domain=test', 10, 200, 2, 1)
    fdfs.upload_test()



