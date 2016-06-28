# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: mango
@contact: w4n9@sina.com
@create: 16/3/25
"""

__author__ = "mango"
__version__ = "0.1"


import os
import json
import requests


# noinspection PyMethodMayBeStatic
class PyFdfsLib(object):
    def __init__(self, host, port=80):
        self.host = host
        self.port = port
        self.url_prefix = "http://%s:%s" % (self.host, self.port)

    def fdfs_upload(self, domain, local_path, hash=False, file_name=None, remove=False):
        """
        上传文件
        :param domain: 域空间名 str
        :param local_path: 文件本地路径 str
        :param hash: 是否计算hash bool
        :param file_name: 是否指定文件名 str
        :return:
        """
        upload_url = "%s/v1/upload?domain=%s" % (self.url_prefix, domain)
        if hash:
            upload_url += "&hash=true"
        if file_name:
            upload_url += "&filename=%s" % file_name
        try:
            files = {'file': open(local_path, 'rb')}
            r = requests.post(upload_url, files=files)
            result = json.loads(r.text)
            if result['status'] == 0:
                return True, result['result']
            else:
                return False, result['result']
        except Exception as error:
            return False, str(error)
        finally:
            if remove:
                os.remove(local_path)

    def fdfs_delete_file(self, domain, file_name):
        """
        删除fdfs文件
        :param domain: 域空间 str
        :param file_name: 文件名 str
        :return:
        """
        delete_url = "%s/v1/delete/%s/%s" % (self.url_prefix, domain, file_name)
        try:
            r = requests.get(delete_url)
            result = json.loads(r.text)
            if result['status'] == 0:
                return True, result['result']
            else:
                return False, result['result']
        except Exception as error:
            return False, str(error)
        finally:
            pass

    def fdfs_info_file(self, domain, file_name):
        """
        获取文件信息
        :param domain: 域空间 str
        :param file_name: 文件名 str
        :return:
        """
        info_url = "%s/v1/info/%s/%s" % (self.url_prefix, domain, file_name)
        try:
            r = requests.get(info_url)
            result = json.loads(r.text)
            if result['status'] == 0:
                return True, result['result']
            else:
                return False, result['result']
        except Exception as error:
            return False, str(error)
        finally:
            pass

    def fdfs_list_domain(self):
        """
        列出所有的domain
        :return:
        """
        domain_url = "%s/v1/list_domain" % self.url_prefix
        try:
            r = requests.get(domain_url)
            result = json.loads(r.text)
            if result['status'] == 0:
                return True, result['result']
            else:
                return False, result['result']
        except Exception as error:
            return False, str(error)
        finally:
            pass

    def fdfs_list_file(self, domain, limit):
        """
        列出domain下的文件名
        :param domain: 域空间 str
        :param limit: 列出数量 int
        :return:
        """
        file_url = "%s/v1/list_file?domain=%s&limit=%s" % (self.url_prefix, domain, limit)
        try:
            r = requests.get(file_url)
            result = json.loads(r.text)
            if result['status'] == 0:
                return True, result['result']
            else:
                return False, result['result']
        except Exception as error:
            return False, str(error)
        finally:
            pass

    def fdfs_create_domain(self, domain):
        """
        新建domain
        :param domain: 域空间
        :return:
        """
        create_domain_url = "%s/v1/create_domain/%s" % (self.url_prefix, domain)
        try:
            r = requests.get(create_domain_url)
            result = json.loads(r.text)
            if result['status'] == 0:
                return True, result['result']
            else:
                return False, result['result']
        except Exception as error:
            return False, str(error)
        finally:
            pass

    def fdfs_delete_domain(self, domain):
        """
        删除空域空间 (有文件的无法删除)
        :param domain: 域空间
        :return:
        """
        delete_domain_url = "%s/v1/delete_domain/%s" % (self.url_prefix, domain)
        try:
            r = requests.get(delete_domain_url)
            result = json.loads(r.text)
            if result['status'] == 0:
                return True, result['result']
            else:
                return False, result['result']
        except Exception as error:
            return False, str(error)
        finally:
            pass


if __name__ == '__main__':
    p = PyFdfsLib('afdfs.com')
    print p.fdfs_list_file('test', '100')

