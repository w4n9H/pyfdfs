# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: mango
@contact: w4n9@sina.com
@create: 16/1/26
"""

__author__ = "mango"
__version__ = "0.1"


import os
import zlib
import hashlib


# noinspection PyMethodMayBeStatic
class HashUtils(object):
    def __init__(self, file_path):
        self.file_path = file_path
        self.max_size = 1024 * 1024
        self.file_size = os.path.getsize(file_path)

    def file_md5(self):
        """
        计算文件MD5值
        :return:
        """
        m = hashlib.md5()
        with open(self.file_path, 'rb') as openfile:
            if self.file_size < self.max_size:
                data = openfile.read()
                m.update(data)
            else:
                while True:
                    data = openfile.read(self.max_size)
                    if not data:
                        break
                    m.update(data)
        return m.hexdigest().upper()

    def file_crc32(self):
        """
        计算文件crc32值
        :return:
        """
        crc = 0
        data = None
        with open(self.file_path, 'rb') as openfile:
            if self.file_size < self.max_size:
                data = openfile.read()
            else:
                while True:
                    data = openfile.read(self.max_size)
                    if not data:
                        break
                    crc = zlib.crc32(data, crc)
        crc = zlib.crc32(data, crc)
        return "%.08X" % (crc & 0xffffffff)

    def file_hash(self):
        """
        计算文件MD5和crc32
        """
        crc = 0
        data = None
        m = hashlib.md5()
        with open(self.file_path, 'rb') as openfile:
            if self.file_size < self.max_size:
                data = openfile.read()
                m.update(data)
            else:
                while True:
                    data = openfile.read(self.max_size)
                    if not data:
                        break
                    m.update(data)
                    crc = zlib.crc32(data, crc)
        crc = zlib.crc32(data, crc)
        return m.hexdigest().upper(), "%.08X" % (crc & 0xffffffff)


if __name__ == '__main__':
    print HashUtils('settings.py').file_md5()
    print HashUtils('settings.py').file_crc32()
    print HashUtils("stockfish_asm.png").file_hash()
