# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: mango
@contact: w4n9@sina.com
@create: 16/2/18
"""

__author__ = "mango"
__version__ = "0.1"


import peewee
from peewee import MySQLDatabase, CompositeKey
from playhouse.pool import PooledMySQLDatabase

from settings import MYSQL_CONFIG
from settings import FDFS_DOMAIN


db = MySQLDatabase(host=MYSQL_CONFIG['host'],
                   port=MYSQL_CONFIG['port'],
                   user=MYSQL_CONFIG['user'],
                   passwd=MYSQL_CONFIG['passwd'],
                   database=MYSQL_CONFIG['db_name'])


pool_db = PooledMySQLDatabase(MYSQL_CONFIG['db_name'],
                              max_connections=2000,
                              stale_timeout=10,
                              host=MYSQL_CONFIG['host'],
                              port=MYSQL_CONFIG['port'],
                              user=MYSQL_CONFIG['user'],
                              passwd=MYSQL_CONFIG['passwd'],)


# noinspection PyPep8Naming,PyMethodMayBeStatic
class fdfs_info(peewee.Model):
    file_name = peewee.FixedCharField(max_length=255)
    file_size = peewee.IntegerField()
    file_md5 = peewee.CharField(default='', max_length=32)
    file_crc32 = peewee.CharField(default='', max_length=8)
    file_group = peewee.CharField(max_length=64)
    file_local_path = peewee.CharField(max_length=255)
    domain_id = peewee.IntegerField()

    class Meta:
        database = db
        primary_key = CompositeKey('file_name', 'domain_id')
        indexes = ((('domain_id', 'file_name'), True), )    #

    def conn_finish(self):
        if not db.is_closed():
            db.close()

    def fdfs_insert(self, in_dict):
        """
        数据插入
        :param in_dict: 插入的数据  dict
        :return: 成功返回 true ,失败返回 false
        """
        try:
            iq = (fdfs_info
                  .insert(**in_dict))
            iq.execute()
            return True, None
        except Exception as error:
            return False, str(error)
        finally:
            self.conn_finish()

    def fdfs_update(self, up_dict, file_name, domain_id):
        """
        数据更新
        :param up_dict: 需要更新的数据  dict
        :param file_name: 文件名  str
        :param domain_id: 域空间ID  int
        :return: 成功返回 true ,失败返回 false
        """
        try:
            uq = (fdfs_info
                  .update(**up_dict)
                  .where(fdfs_info.domain_id == domain_id, fdfs_info.file_name == file_name))
            uq.execute()
            return True, None
        except Exception as error:
            return False, str(error)
        finally:
            self.conn_finish()

    def fdfs_delete(self, file_name, domain_id):
        """
        数据删除
        :param file_name: 文件名  str
        :param domain: 域空间名  str
        :return: 成功返回 true ,失败返回 false
        """
        try:
            d = (fdfs_info
                 .delete()
                 .where(fdfs_info.domain_id == domain_id, fdfs_info.file_name == file_name))
            d.execute()
            return True, None
        except Exception as error:
            return False, str(error)
        finally:
            self.conn_finish()

    def fdfs_exist(self, file_name, domain_id):
        """
        判断数据是否存在
        :param file_name: 文件名  str
        :param domain: 域空间名  str
        :return:
        0 数据存在
        1 数据不存在
        2 查询错误
        """
        try:
            query_data = fdfs_info.select(fdfs_info.file_group, fdfs_info.file_local_path).\
                where(fdfs_info.domain_id == domain_id, fdfs_info.file_name == file_name)
            if query_data:
                return 0, query_data.dicts().get()
            else:
                return 1, None
        except Exception as error:
            return 2, str(error)
        finally:
            self.conn_finish()

    def fdfs_file_info(self, file_name, domain_id):
        """
        数据查询
        :param file_name: 文件名  str
        :param domain:  域空间名  str
        :return:
        0 查询成功
        1 未查询到数据
        2 查询错误
        """
        try:
            query_data = fdfs_info.select().where(fdfs_info.domain_id == domain_id, fdfs_info.file_name == file_name)
            if query_data:
                return 0, query_data.dicts().get()
            else:
                return 1, None
        except Exception as error:
            return 2, str(error)
        finally:
            self.conn_finish()

    def fdfs_download(self, file_name, domain_id):
        """
        获取下载地址
        :param file_name: 文件名  str
        :param domain: 域空间名  str
        :return: 成功返回 true ,失败返回 false
        """
        try:
            query_data = fdfs_info.select(fdfs_info.file_group, fdfs_info.file_local_path).\
                where(fdfs_info.domain_id == domain_id, fdfs_info.file_name == file_name)
            if query_data:
                query_info = query_data.dicts().get()
                group_info = query_info.get('file_group', '')
                group_local_info = query_info.get('file_local_path', '')
                http_info = FDFS_DOMAIN.get(group_info, '')
                redirect_http = "%s/%s/%s?filename=%s" % (http_info, group_info, group_local_info, file_name)
                return True, redirect_http
            else:
                return False, None
        except Exception as error:
            return False, str(error)
        finally:
            self.conn_finish()

    def fdfs_empty(self, domain_id):
        """
        判断某个domain是否为空
        :param domain_id:
        :return:
        0 domain为空
        1 domain中有文件
        2 查询错误
        """
        try:
            result = fdfs_info.select().where(fdfs_info.domain_id == domain_id).count()
            if result == 0:
                return 0, None
            else:
                return 1, None
        except Exception as error:
            return 2, str(error)
        finally:
            self.conn_finish()

    def list_file(self, domain_id, limit):
        """
        列出domain 文件列表
        :param domain_id:
        :param limit:
        :return:
        0 文件列表
        1 domain没有文件
        2 查询错误
        """
        try:
            result = []
            query_data = fdfs_info.select(fdfs_info.file_name).where(fdfs_info.domain_id == domain_id).limit(limit)
            if query_data:
                for i in query_data.dicts():
                    result.append(i.get('file_name'))
                return 0, result
            else:
                return 1, []
        except Exception as error:
            return 2, str(error)
        finally:
            self.conn_finish()


# noinspection PyPep8Naming,PyMethodMayBeStatic
class domain_info(peewee.Model):
    # domain_id = peewee.IntegerField()
    domain_name = peewee.CharField(max_length=255, unique=True)

    class Meta:
        database = db    # 连接数据库

    def conn_finish(self):
        if not db.is_closed():
            db.close()

    def id_exist(self, domain_name):
        """
        判断 域空间 是否存在
        :param domain_name: 域空间名 str
        :return:
        0 数据存在
        1 数据不存在
        2 查询错误
        """
        try:
            query_data = domain_info.select(domain_info.id, domain_info.domain_name).\
                where(domain_info.domain_name == domain_name)
            if query_data:
                return 0, query_data.dicts().get()
            else:
                return 1, None
        except Exception as error:
            return 2, str(error)
        finally:
            self.conn_finish()

    def id_insert(self, domain_name):
        """
        插入新的 域空间
        :param domain_name: 域空间名 str
        :return: 成功返回 true ,失败返回 false
        """
        try:
            in_dict = {'domain_name': domain_name}
            iq = (domain_info
                  .insert(**in_dict))
            iq.execute()
            return True, None
        except Exception as error:
            return False, str(error)
        finally:
            self.conn_finish()

    def domain_operation(self, domain_name):
        """
        域空间名操作
        :param domain_name: 域空间名 str
        :return:
        """
        try:
            id_exist_status, id_exist_info = self.id_exist(domain_name)
            if id_exist_status == 0:
                return True, id_exist_info
            elif id_exist_status == 1:
                id_insert_status, id_insert_info = self.id_insert(domain_name)
                if id_insert_status:
                    id_query_status, id_query_info = self.id_exist(domain_name)
                    if id_query_status == 0:
                        return True, id_query_info
                else:
                    return False, id_insert_info
            else:
                return False, id_exist_info
        except Exception as error:
            return False, str(error)
        finally:
            self.conn_finish()

    def get_domain_name(self, domain_id):
        """
        通过 domain_id 获取 domain_name
        :param domain_id:
        :return:
        """
        try:
            query_data = domain_info.select(domain_info.domain_name).where(domain_info.id == domain_id)
            if query_data:
                return 0, query_data.dicts().get()
            else:
                return 1, None
        except Exception as error:
            return 2, str(error)
        finally:
            self.conn_finish()

    def get_all_domain(self):
        """
        获取所有 domain
        :return:
        """
        result = []
        try:
            query_data = domain_info.select(domain_info.domain_name)
            if query_data:
                for i in query_data.dicts():
                    result.append(i.get('domain_name'))
                return 0, result
            else:
                return 1, result
        except Exception as error:
            return 2, str(error)
        finally:
            self.conn_finish()

    def delete_domain(self, domain):
        """
        删除 domain
        :param domain:
        :return:
        """
        try:
            iq = (domain_info
                  .delete()
                  .where(domain_info.domain_name == domain))
            iq.execute()
            return True, None
        except Exception as error:
            return False, str(error)
        finally:
            self.conn_finish()


if __name__ == '__main__':
    ms = domain_info()
    # ms.query_data()
    # print ms.fdfs_exist('281cb5c0-d07e-', 'test')
    print ms.get_all_domain()
    # print ms.fdfs_download('281cb5c0-d07e-', 'test')
    # print ms.fdfs_update({'file_crc32': 'F'}, '281cb5c0-d07e-4', 'test')
