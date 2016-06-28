# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: mango
@contact: w4n9@sina.com
@create: 16/1/26
调用fdfs的相关接口,进行状态查询,文件上传,
16-02-14:修复无法上传文本文件,以及上传文件与源文件不一致的问题
"""

__author__ = "mango"
__version__ = "0.1"


# noinspection PyUnresolvedReferences
import FDFSPythonClient

import json
from settings import FDFS_CONFIG


# noinspection PyMethodMayBeStatic,PyBroadException
class FDFSUtils(object):
    def __init__(self):
        client_path = FDFS_CONFIG["client_path"]
        log_level = FDFS_CONFIG["log_level"]
        FDFSPythonClient.fdfs_init(client_path, log_level)

    def list_all_groups(self):
        """
        获取到的group信息:
            group_name : group名字 str
            total_mb : 总空间 MB int
            free_mb : 剩余空间 MB int
            server_count : storage数量 int
            active_count : 存活的storage数量 int
            storage_port : 开启的端口 int
        获取到的storage信息:
            id : id信息
            ip_addr: ip地址 str
            total_mb: 磁盘总量MB int
            store_path_count:
            version: fdfs版本号 str
            storage_port: 端口号 int
            status：状态  int
            free_mb：剩余空间  int
            up_time：上次开启时间 str
        storage状态码:
            1: INIT      :初始化，尚未得到同步已有数据的源服务器
            2: WAIT_SYNC :等待同步，已得到同步已有数据的源服务器
            3: SYNCING   :同步中
            4: DELETED   :已删除，该服务器从本组中摘除
            5: OFFLINE   :离线
            6: ONLINE    :在线，尚不能提供服务
            7: ACTIVE    :在线，可以提供服务
        :return:
        """
        try:
            group_detail = []
            all_info = dict()
            storage_count = 0    # storage 数量
            active_storage = 0    # 存活 storage 数量
            path_count = 0    # storage path  数量
            total_mb = 0
            free_mb = 0
            all_group = json.loads(FDFSPythonClient.list_all_groups()[1])
            for gc in range(1, len(all_group) + 1):
                group_name = "group%s" % gc
                storages_list = json.loads(FDFSPythonClient.list_storages(group_name, "")[1])  # list
                for storage in storages_list:
                    storage['group'] = group_name
                    group_detail.append(storage)
            # print group_detail
            all_info['group_count'] = len(all_group)
            for c in all_group:
                storage_count += c['server_count']
                active_storage += c['active_count']
                total_mb += c['total_mb']
                free_mb += c['free_mb']
            all_info['storage_count'] = storage_count
            all_info['active_storage'] = active_storage
            all_info['total_mb'] = total_mb
            all_info['free_mb'] = free_mb
            all_info['used_mb'] = total_mb - free_mb
        except Exception as error:
            return False, error
        return True, (all_info, all_group, group_detail)

    def upload_file(self, file_path):
        """
        上传文件
        :param file_path: 文件路径 str
        :return:成功返回fdfs路径,失败返回None
        """
        r_path = None
        try:
            with open(file_path, 'rb') as fp:
                file_content = fp.read()
                r_path = FDFSPythonClient.fdfs_upload(file_content, "")
                if r_path[0] != 0:
                    return False, r_path[1]
        except Exception as error:
            return False, error
        return True, r_path[1]

    def delete_file(self, group_name, local_path):
        """
        删除文件,由mysql查询后实现删除
        1.删除数据库数据
        2.删除fdfs文件
        :param group_name: 文件所属fdfs的group名 str
        :param local_path: 文件所属fdfs的路径 str
        :return: True 为成功, False 为失败以及错误信息
        """
        try:
            r = FDFSPythonClient.fdfs_delete(group_name, local_path)
            if r == 0:
                return True, None
            else:
                return False, "fdfs delete fail"
        except Exception as error:
            return False, str(error)

    def info_file(self, file_name):
        """
        获取文件相关信息,mysql查询
        :param file_name: 文件名
        :return: 通过mysql查询,考虑移除
        """
        pass

    def download_file(self, file_name):
        """
        获取下载文件url,mysql查询
        :param file_name: 文件名
        :return: 通过mysql查询,考虑移除
        """
        pass


if __name__ == '__main__':
    f = FDFSUtils()
    f.list_all_groups()
    f.upload_file('x.txt')

