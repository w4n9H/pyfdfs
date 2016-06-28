# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: mango
@contact: w4n9@sina.com
@create: 16/4/18
"""

__author__ = "mango"
__version__ = "0.1"


import peewee
from peewee import MySQLDatabase, CompositeKey
from playhouse.pool import PooledDatabase
from playhouse.shortcuts import RetryOperationalError

from settings import MYSQL_CONFIG
from settings import FDFS_DOMAIN


# noinspection PyAbstractClass
class MyMySQLDatabase(MySQLDatabase):
    commit_select = False


# noinspection PyAbstractClass
class MyRetryDB(RetryOperationalError, MyMySQLDatabase):
    pass


# pool_db = MyMySQLDatabase(host=MYSQL_CONFIG['host'],
#                          port=MYSQL_CONFIG['port'],
#                          user=MYSQL_CONFIG['user'],
#                          passwd=MYSQL_CONFIG['passwd'],
#                          database=MYSQL_CONFIG['db_name'],
#                          autocommit=MYSQL_CONFIG['autocommit'])


# noinspection PyAbstractClass
class MyPooledMySQLDatabase(PooledDatabase, MyMySQLDatabase):
    pass


pool_db = MyPooledMySQLDatabase(max_connections=MYSQL_CONFIG['max_connections'],
                                connect_timeout=MYSQL_CONFIG['connect_timeout'],
                                stale_timeout=MYSQL_CONFIG['stale_timeout'],
                                threadlocals=MYSQL_CONFIG['threadlocals'],
                                autocommit=MYSQL_CONFIG['autocommit'],
                                database=MYSQL_CONFIG['db_name'],
                                host=MYSQL_CONFIG['host'],
                                port=MYSQL_CONFIG['port'],
                                user=MYSQL_CONFIG['user'],
                                passwd=MYSQL_CONFIG['passwd'])


class BaseModel(peewee.Model):
    class Meta:
        database = pool_db


# noinspection PyPep8Naming
class fdfs_info(BaseModel):
    file_name = peewee.FixedCharField(max_length=255)
    file_size = peewee.IntegerField()
    file_md5 = peewee.CharField(default='', max_length=32)
    file_crc32 = peewee.CharField(default='', max_length=8)
    file_group = peewee.CharField(max_length=64)
    file_local_path = peewee.CharField(max_length=255)
    domain_id = peewee.IntegerField()

    class Meta:
        primary_key = CompositeKey('file_name', 'domain_id')
        indexes = ((('domain_id', 'file_name'), True), )    #


# noinspection PyPep8Naming
class domain_info(BaseModel):
    # domain_id = peewee.IntegerField()
    domain_name = peewee.CharField(max_length=255, unique=True)

    class Meta:
        pass


# noinspection PyMethodMayBeStatic,PyBroadException,PyProtectedMember
class MySQLUtils(object):
    def __init__(self):
        # self.create_connect()
        pass

    def create_connect(self):
        try:
            if pool_db.is_closed():
                pool_db.manual_close()
            else:
                pass
        except:
            return False
        return True

    def close_connetc(self):
        try:
            if not pool_db.is_closed():
                pool_db.close()
        except:
            return False
        return True

    def commit(self):
        pool_db.commit()

    def begin(self):
        pool_db.begin()

    def rollback(self):
        pool_db.rollback()

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
            pass

    def fdfs_update(self, up_dict, file_name, domain_name):
        """
        数据更新
        :param up_dict: 需要更新的数据  dict
        :param file_name: 文件名  str
        :param domain_name: 域空间ID  int
        :return:
        0 更新成功
        1 不存在这个domain空间
        2 更新错误
        """
        try:
            id_stat, id_info = self.domain_id_exist(domain_name)
            if id_stat == 0:
                uq = (fdfs_info
                      .update(**up_dict)
                      .where(fdfs_info.file_name == file_name, fdfs_info.domain_id == id_info.get('id')))
                uq.execute()
                return 0, None
            elif id_stat == 1:
                return 1, 'not this domain'
            else:
                return 2, id_info
        except Exception as error:
            return 2, str(error)
        finally:
            pass

    def fdfs_update_id(self, up_dict, file_name, domain_id):
        """
        数据更新
        :param up_dict: 需要更新的数据  dict
        :param file_name: 文件名  str
        :param domain_id: 域空间ID  int
        :return:
        0 更新成功
        1 不存在这个domain空间
        2 更新错误
        """
        try:
            uq = (fdfs_info
                  .update(**up_dict)
                  .where(fdfs_info.file_name == file_name, fdfs_info.domain_id == domain_id))
            uq.execute()
            return True, None
        except Exception as error:
            return False, str(error)
        finally:
            pass

    def fdfs_delete(self, file_name, domain_name):
        """
        数据删除
        :param file_name: 文件名  str
        :param domain_name: 域空间名  str
        :return:
        0 删除成功
        1 不存在这个domain空间
        2 删除错误
        """
        try:
            id_stat, id_info = self.domain_id_exist(domain_name)
            if id_stat == 0:
                d = (fdfs_info
                     .delete()
                     .where(fdfs_info.file_name == file_name, fdfs_info.domain_id == id_info.get('id')))
                d.execute()
                return 0, None
            elif id_stat == 1:
                return 1, 'not this domain'
            else:
                return 2, id_info
        except Exception as error:
            return False, str(error)
        finally:
            pass

    def fdfs_exist(self, file_name, domain_name):
        """
        判断文件是否存在
        :param file_name: 文件名  str
        :param domain_name: 域空间名  str
        :return:
        0 文件存在
        1 文件不存在
        2 查询错误
        """
        try:
            on_condition = (domain_info.id == fdfs_info.domain_id) & (domain_info.domain_name == domain_name)
            query_data = (fdfs_info
                          .select(fdfs_info.file_group, fdfs_info.file_local_path)
                          .join(domain_info, on=on_condition)
                          .where(fdfs_info.file_name == file_name))
            if query_data:
                return 0, query_data.dicts().get()
            else:
                return 1, None
        except Exception as error:
            return 2, str(error)
        finally:
            pass

    def fdfs_file_info(self, file_name, domain_name):
        """
        文件信息查询
        :param file_name: 文件名  str
        :param domain_name:  域空间名  str
        :return:
        0 查询成功
        1 未查询到数据
        2 查询错误
        """
        try:
            on_condition = (domain_info.id == fdfs_info.domain_id) & (domain_info.domain_name == domain_name)
            query_data = (fdfs_info
                          .select()
                          .join(domain_info, on=on_condition)
                          .where(fdfs_info.file_name == file_name))
            if query_data:
                return 0, query_data.dicts().get()
            else:
                return 1, None
        except Exception as error:
            return 2, str(error)
        finally:
            pass

    def fdfs_download(self, file_name, domain_name):
        """
        获取下载地址
        :param file_name: 文件名  str
        :param domain_name: 域空间名  str
        :return: 成功返回 true ,失败返回 false
        """
        try:
            on_condition = (domain_info.id == fdfs_info.domain_id) & (domain_info.domain_name == domain_name)
            query_data = (fdfs_info
                          .select(fdfs_info.file_group, fdfs_info.file_local_path)
                          .join(domain_info, on=on_condition)
                          .where(fdfs_info.file_name == file_name))
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
            pass

    def fdfs_empty(self, domain_name):
        """
        判断某个domain是否为空
        :param domain_name:
        :return:
        0 domain为空
        1 domain中有文件
        2 查询错误
        """
        try:
            on_condition = (domain_info.id == fdfs_info.domain_id) & (domain_info.domain_name == domain_name)
            result = (fdfs_info
                      .select()
                      .join(domain_info, on=on_condition)
                      .count())
            if result == 0:
                return 0, None
            else:
                return 1, None
        except Exception as error:
            return 2, str(error)
        finally:
            pass

    def list_file(self, domain_name, limit):
        """
        列出domain 文件列表
        :param domain_name:
        :param limit:
        :return:
        0 文件列表
        1 domain没有文件
        2 查询错误
        """
        try:
            result = []
            on_condition = (domain_info.id == fdfs_info.domain_id) & (domain_info.domain_name == domain_name)
            query_data = (fdfs_info
                          .select(fdfs_info.file_name)
                          .join(domain_info, on=on_condition)
                          .limit(limit))
            if query_data:
                for i in query_data.dicts():
                    result.append(i.get('file_name'))
                return 0, result
            else:
                return 1, []
        except Exception as error:
            return 2, str(error)
        finally:
            pass

    def domain_id_exist(self, domain_name):
        """
        判断 域空间 是否存在
        :param domain_name: 域空间名 str
        :return:
        0 数据存在
        1 数据不存在
        2 查询错误
        """
        try:
            query_data = (domain_info
                          .select(domain_info.id, domain_info.domain_name)
                          .where(domain_info.domain_name == domain_name))
            if query_data:
                return 0, query_data.dicts().get()
            else:
                return 1, None
        except Exception as error:
            return 2, str(error)
        finally:
            pass

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
            pass

    def domain_operation(self, domain_name):
        """
        域空间名操作
        :param domain_name: 域空间名 str
        :return:
        """
        try:
            id_exist_status, id_exist_info = self.domain_id_exist(domain_name)
            if id_exist_status == 0:
                return True, id_exist_info
            elif id_exist_status == 1:
                id_insert_status, id_insert_info = self.id_insert(domain_name)
                if id_insert_status:
                    id_query_status, id_query_info = self.domain_id_exist(domain_name)
                    if id_query_status == 0:
                        return True, id_query_info
                else:
                    return False, id_insert_info
            else:
                return False, id_exist_info
        except Exception as error:
            return False, str(error)
        finally:
            pass

    def domain_id_get_name(self, domain_id):
        """
        通过 domain_id 获取 domain_name
        :param domain_id:
        :return:
        0 获取成功
        1 没有获取到数据
        2 获取失败
        """
        try:
            query_data = (domain_info
                          .select(domain_info.domain_name)
                          .where(domain_info.id == domain_id))
            if query_data:
                return 0, query_data.dicts().get()
            else:
                return 1, None
        except Exception as error:
            return 2, str(error)
        finally:
            pass

    def get_all_domain(self):
        """
        获取所有 domain
        :return:
        0 获取成功
        1 没有domain
        2 获取失败
        """
        result = []
        try:
            query_data = (domain_info
                          .select(domain_info.domain_name))
            if query_data:
                for i in query_data.dicts():
                    result.append(i.get('domain_name'))
                return 0, result
            else:
                return 1, result
        except Exception as error:
            return 2, str(error)
        finally:
            pass

    def delete_domain(self, domain_name):
        """
        删除 domain
        :param domain_name:
        :return:
        0 删除成功
        1 domain 不为空
        2 删除失败
        """
        try:
            list_stat, list_info = self.list_file(domain_name, 1)
            if list_stat == 0:
                return 1, 'domain not empty'
            elif list_stat == 1:
                iq = (domain_info
                      .delete()
                      .where(domain_info.domain_name == domain_name))
                iq.execute()
                return 0, None
            else:
                return 2, list_info
        except Exception as error:
            return 2, str(error)
        finally:
            pass

    def get_pool(self):
        return len(pool_db._connections)

    def raw_sql_fdfs_exist(self, file_name, domain_name):
        try:
            raw_sql = """
            select t1.file_group,t1.file_local_path from fdfs_info t1 where t1.file_name = '%s'
            and t1.domain_id = (select t2.id from domain_info t2 where t2.domain_name='%s' );
            """ % (file_name, domain_name)
            result = pool_db.execute_sql(raw_sql).fetchone()
            if result:
                return 0, {'file_group': result[0], 'file_local_path': result[1]}
            else:
                return 1, None
        except Exception as error:
            return 2, str(error)
        finally:
            pass

    def raw_sql_fdfs_download(self, file_name, domain_name):
        try:
            raw_sql = """
            select t1.file_group,t1.file_local_path from fdfs_info t1 where t1.file_name = '%s'
            and t1.domain_id = (select t2.id from domain_info t2 where t2.domain_name='%s' );
            """ % (file_name, domain_name)
            result = pool_db.execute_sql(raw_sql).fetchone()
            if result:
                group_info, group_local_info = result[0], result[1]
                http_info = FDFS_DOMAIN.get(group_info, '')
                redirect_http = "%s/%s/%s?filename=%s" % (http_info, group_info, group_local_info, file_name)
                return True, redirect_http
            else:
                return False, None
        except Exception as error:
            return False, str(error)
        finally:
            pass

    def raw_sql_fdfs_file_info(self, file_name, domain_name):
        """
        文件信息查询
        :param file_name: 文件名  str
        :param domain_name:  域空间名  str
        :return:
        0 查询成功
        1 未查询到数据
        2 查询错误
        """
        try:
            raw_sql = """
            select t1.file_name,t1.file_size,t1.file_md5,t1.file_crc32,t1.file_group,t1.file_local_path,t1.domain_id
            from fdfs_info t1 where t1.file_name = '%s'
            and t1.domain_id = (select t2.id from domain_info t2 where t2.domain_name='%s' );
            """ % (file_name, domain_name)
            result = pool_db.execute_sql(raw_sql).fetchone()
            if result:
                result_dict = {
                    'file_name': result[0],
                    'file_size': result[1],
                    'file_md5': result[2],
                    'file_crc32': result[3],
                    'file_group': result[4],
                    'file_local_path': result[5],
                    'domain_id': result[6]
                }
                return 0, result_dict
            else:
                return 1, None
        except Exception as error:
            return 2, str(error)
        finally:
            pass

if __name__ == '__main__':
    m = MySQLUtils()
    #for i in xrange(100):
    #    print m.fdfs_exist('A9F85DC4B72841D532BF140273997D6E', 'sample')
    #print MySQLUtils().fdfs_download('1020B4E2642EC3C37FCD7DE14819BB4B', 'sample')
    print m.fdfs_download('1020B4E2642EC3C37FCD7DE14819BB4B', 'sample')
    print m.raw_sql_fdfs_download('1020B4E2642EC3C37FCD7DE14819BB4B', 'sample')
    MySQLUtils().close_connetc()

