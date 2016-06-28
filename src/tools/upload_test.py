# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: mango
@contact: w4n9@sina.com
@create: 16/3/28
"""

__author__ = "mango"
__version__ = "0.1"

from prettytable import PrettyTable
from multiprocessing import Process, Queue, Manager
import pyfdfs_lib
import subprocess
import time
import os


# noinspection PyBroadException,PyMethodMayBeStatic
class UploadTest(object):
    def __init__(self, upload_host, domain, list_path, local_root_dir, process):
        self.start_time = time.time()
        self.upload_host = upload_host
        self.local_root_dir = local_root_dir
        self.list_path = list_path
        self.domain = domain
        self.tmp_list = []
        self.work_count = process
        self.download_fail = 0
        self.upload_num = 0
        self.success = 0
        self.fail = 0

    def chunks(self, ls, n):
        """
        分割一个列表为n份
        :param ls: 列表 (list)
        :param n: 份数 (int)
        :return: list
        """
        if not isinstance(ls, list) or not isinstance(n, int):
            return []
        ls_len = len(ls)
        if n <= 0 or 0 == ls_len:
            return []
        if n > ls_len:
            return [ls]
        elif n == ls_len:
            return [[i] for i in ls]
        else:
            j = ls_len / n
            k = ls_len % n
            ls_return = []
            for i in xrange(0, (n - 1) * j, j):
                ls_return.append(ls[i:i + j])
            ls_return.append(ls[(n - 1) * j:])
            return ls_return

    def download_file(self, download_url, local_path):
        try:
            download_cmd = """wget -q "%s" -O %s""" % (download_url, local_path)
            return_code = subprocess.call(download_cmd, shell=True)
            if return_code == 0:
                return True
            else:
                return False
        except:
            return False

    def upload_file(self, q, md5_crc32_list):
        for md5_crc32 in md5_crc32_list:
            upload_client = pyfdfs_lib.PyFdfsLib(self.upload_host)
            download_path = os.path.join(self.local_root_dir, md5_crc32)
            download_url_mog = 'http://xxx.xxx.xxx/download/%s' % md5_crc32
            if self.download_file(download_url_mog, download_path):
                upload_stat, upload_info = upload_client.fdfs_upload(domain=self.domain, local_path=download_path,
                                                                     hash=True, remove=True)
                if upload_stat:
                    q.put(0)
                else:
                    q.put(1)
            else:
                os.remove(download_path)
                q.put(2)

    def upload_begin(self):
        plist = []
        q = Manager().Queue()
        with open(self.list_path, 'r') as fp:
            for i in fp:
                if not i:
                    break
                md5_crc32 = i.strip()[:41]
                if md5_crc32 not in self.tmp_list and len(md5_crc32) == 41:
                    self.tmp_list.append(md5_crc32)
                    self.upload_num += 1
        print self.upload_num
        for md5_crc32_list in self.chunks(self.tmp_list, self.work_count):
            proc = Process(target=self.upload_file, args=(q, md5_crc32_list,))
            plist.append(proc)
        for proc in plist:
            proc.start()
        for proc in plist:
            proc.join()
        while True:
            if q.empty():
                break
            else:
                r = q.get()
                if r == 0:
                    self.success += 1
                elif r == 1:
                    self.fail += 1
                elif r == 2:
                    self.download_fail += 1
                else:
                    pass
        use_time = time.time() - self.start_time
        table = PrettyTable(["key", "value"])
        table.add_row(["Upload Count", len(set(self.tmp_list))])
        table.add_row(["Success count", self.success])
        table.add_row(["Fail count", self.fail])
        table.add_row(["Download Fail", self.download_fail])
        table.add_row(["Use time (s)", "%.2f" % use_time])
        print table


if __name__ == '__main__':
    p = UploadTest('xxx.xxx', 'test', 'xxx.txt', '/dev/shm', 15)
    p.upload_begin()



