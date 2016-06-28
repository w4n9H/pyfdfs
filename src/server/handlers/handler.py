# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: mango
@contact: w4n9@sina.com
@create: 16/1/26

# 16-01-27 : tornado文件上传模块,支持大文件
# 16-02-01 : 文件上传功能完成
# 16-02-02 : 下载功能完成,集群状态以及单个文件信息传接口完成
# 16-02-03 : 功能测试
# 16-02-19 : mysql 全部替换为使用 orm
# 16-04-18 : 优化mysql调用，减少了50%的连接数
"""

__author__ = "mango"
__version__ = "0.1"


import os
import json
import logging
import tornado.web
import tornado.gen
from tornado.web import HTTPError

from post_streamer import PostDataStreamer
from hash_utils import HashUtils
from fdfs_utils import FDFSUtils
from mysql_utils import MySQLUtils
from settings import FDFS_CONFIG


class HandlerExcept(Exception):
    def __init__(self, error):
        Exception.__init__(self, error)
        self.msg = error


class FdfsExcept(Exception):
    def __init__(self, error):
        Exception.__init__(self, error)
        self.msg = error


class MysqlExcept(Exception):
    def __init__(self, error):
        Exception.__init__(self, error)
        self.msg = error


# noinspection PyAbstractClass
class TestHandlerV1(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.write('fuck')


# noinspection PyBroadException,PyAttributeOutsideInit,PyExceptClausesOrder
@tornado.web.stream_request_body
class UploadHandlerV1(tornado.web.RequestHandler):
    """
    Tornado文件上传类,使用了 stream_request_body 支持大文件上传
    """
    def initialize(self):
        """
        第一步执行,初始化操作
        :return:
        """
        self.set_header('Content-type', 'application/json')
        self.upload_dir = FDFS_CONFIG.get('tmp_path')
        if not os.path.exists(self.upload_dir):
            os.mkdir(self.upload_dir)
        self.fdfs_client = FDFSUtils()
        self.mysql_client = MySQLUtils()
        self.file_tmp_path = None
        self.res_status = dict()
        self.file_info = dict()

    @tornado.gen.coroutine
    def prepare(self):
        """
        第二步执行,读取请求头
        :return:
        """
        try:
            total = int(self.request.headers.get("Content-Length", "0"))
        except:
            total = 0
        self.ps = PostDataStreamer(total, self.upload_dir)

    @tornado.gen.coroutine
    def data_received(self, chunk):
        """
        第三步执行,写文件
        :param chunk: 文件内容
        :return:
        """
        self.ps.receive(chunk)

    def fdfs_index(self, file_name, domain_name, replace=False):
        """
        上传文件到fdfs,插入索引信息到mysql
        :return:
        返回 0 , 正常上传并写入索引信息
        返回 1 , mysql相关错误
        返回 2 , fdfs相关错误
        返回 3 , 其他错误
        """
        try:
            exist_status, exist_info = self.mysql_client.raw_sql_fdfs_exist(file_name, domain_name)
            if exist_status == 0:    # 已经存在,决定是否覆盖
                if replace:   # 覆盖
                    fdfs_up_status, fdfs_up_info = self.fdfs_client.upload_file(self.file_tmp_path)
                    if fdfs_up_status:
                        file_group, file_local_path = fdfs_up_info.split('/', 1)
                        self.file_info['file_group'] = file_group
                        self.file_info['file_local_path'] = file_local_path
                        mysql_up_status, mysql_up_info = self.mysql_client.fdfs_update(self.file_info, file_name,
                                                                                       domain_name)
                        if mysql_up_status == 0:
                            if exist_info.get('file_group', '') == '' or exist_info.get('file_local_path', '') == '':
                                pass
                            else:
                                delete_status, delete_result = self.fdfs_client.delete_file(
                                    exist_info.get('file_group', ''), exist_info.get('file_local_path', ''))
                                if delete_status:
                                    pass
                                else:
                                    raise FdfsExcept("{res}:{group}/{path}".format(res=delete_result,
                                                                                   group=self.file_info['file_group'],
                                                                                   path=self.file_info['file_local_path']))
                        else:
                            raise MysqlExcept(mysql_up_info)
                    else:    # 上传失败
                        raise FdfsExcept(fdfs_up_info)
                else:
                    pass
            elif exist_status == 1:    # 不存在，上传新文件
                # insert 半条数据
                self.file_info['file_group'] = ''
                self.file_info['file_local_path'] = ''
                mysql_insert_status, mysql_insert_info = self.mysql_client.fdfs_insert(self.file_info)
                if mysql_insert_status:
                    fdfs_up_status, fdfs_up_info = self.fdfs_client.upload_file(self.file_tmp_path)
                    if fdfs_up_status:
                        file_group, file_local_path = fdfs_up_info.split('/', 1)
                        self.file_info['file_group'] = file_group
                        self.file_info['file_local_path'] = file_local_path
                        # mysql_status, mysql_info = self.mysql_client.fdfs_insert(self.file_info)
                        mysql_up_status, mysql_up_info = self.mysql_client.fdfs_update_id(self.file_info, file_name,
                                                                                          self.file_info['domain_id'])
                        if mysql_up_status:
                            pass
                        else:
                            raise MysqlExcept("update-%s" % mysql_up_info)
                    else:
                        raise FdfsExcept(str(fdfs_up_info))
                else:
                    raise MysqlExcept("insert-%s" % mysql_insert_info)
            else:
                raise MysqlExcept("exist-%s" % exist_info)
            """
            elif exist_status == 1:    # 不存在，上传新文件
                fdfs_up_status, fdfs_up_info = self.fdfs_client.upload_file(self.file_tmp_path)
                if fdfs_up_status:
                    file_group, file_local_path = fdfs_up_info.split('/', 1)
                    self.file_info['file_group'] = file_group
                    self.file_info['file_local_path'] = file_local_path
                    mysql_insert_status, mysql_insert_info = self.mysql_client.fdfs_insert(self.file_info)
                    if mysql_status:
                        pass
                    else:
                        raise MysqlExcept("insert-%s" % mysql_insert_info)
                else:
                    raise FdfsExcept(str(fdfs_up_info))
            else:
                raise MysqlExcept("exist-%s" % exist_info)
            """
        except MysqlExcept as error:
            return 1, str(error.msg)
        except FdfsExcept as error:
            return 2, str(error.msg)
        except Exception as error:
            return 3, str(error)
        return 0, None

    @tornado.gen.coroutine
    @tornado.web.asynchronous
    def post(self, *args, **kwargs):
        """
        第四步执行,获取文件信息,上传写数据库,销毁文件
        :param args:
        :param kwargs:
        :return:
        """
        domain = self.get_argument('domain', default='test', strip=True)
        file_name = self.get_argument('filename', default=None, strip=True)
        hash_flag = self.get_argument('hash', default='false', strip=True)
        replace = self.get_argument('replace', default='false', strip=True)
        replace_flag = False
        # redis = self.get_argument('redis', default='false', strip=True)
        try:
            self.ps.finish_receive()
            # 获取文件信息
            for idx, part in enumerate(self.ps.parts):
                self.file_info['file_size'] = part.get('size', 0)
                self.file_tmp_path = part.get("tmpfile").name
                if hash_flag == 'true':
                    md5, crc32 = HashUtils(self.file_tmp_path).file_hash()
                    self.file_info['file_md5'] = md5
                    self.file_info['file_crc32'] = crc32
                else:
                    self.file_info['file_md5'] = ""
                    self.file_info['file_crc32'] = ""
                for header in part["headers"]:
                    params = header.get("params", None)
                    if params:
                        if file_name:
                            self.file_info['file_name'] = file_name
                        else:
                            self.file_info['file_name'] = params.get("filename", "")
            domain_exist_stat, domain_exist_info = self.mysql_client.domain_id_exist(domain)
            if domain_exist_stat == 0:
                domain_id = domain_exist_info.get('id')
                self.file_info['domain_id'] = domain_id
                # 上传文件,写入索引
                if replace == 'true':
                    replace_flag = True
                fdfs_index_status, fdfs_index_info = self.fdfs_index(self.file_info['file_name'], domain,
                                                                     replace=replace_flag)
                if fdfs_index_status == 0:
                    logging.info("file: %s, domain: %s ,fdfs upload, index insert success" %
                                 (self.file_info['file_name'], domain))
                    self.res_status['status'], self.res_status['result'] = 0, self.file_info['file_name']
                else:
                    logging.error("file: %s, domain: %s , error: %s-%s" % (self.file_info['file_name'],
                                                                           domain, str(fdfs_index_status),
                                                                           fdfs_index_info))
                    self.res_status['status'], self.res_status['result'] = fdfs_index_status, fdfs_index_info
            elif domain_exist_stat == 1:
                self.res_status['status'], self.res_status['result'] = 6, "Domain not exist"
            else:
                logging.error("file: %s, domain: %s , error: %s" % (self.file_info['file_name'],
                                                                    domain, domain_exist_info))
                self.res_status['status'], self.res_status['result'] = 5, domain_exist_info
        except Exception as error:
            logging.error(str(error))
            self.res_status['status'], self.res_status['result'] = 4, str(error)
        finally:
            self.mysql_client.close_connetc()
            self.file_info.clear()
            self.ps.release_parts()    # 删除处理
            self.write(json.dumps(self.res_status))
            self.finish()


# noinspection PyAbstractClass,PyAttributeOutsideInit,PyBroadException
class DownloadHandlerV1(tornado.web.RequestHandler):
    def initialize(self):
        self.mysql_client = MySQLUtils()

    @tornado.gen.coroutine
    @tornado.web.asynchronous
    def get(self, domain, file_name):
        try:
            if file_name:
                query_status, query_result = self.mysql_client.raw_sql_fdfs_download(file_name.strip(), domain.strip())
                if query_status:
                    self.redirect(url=query_result, permanent=False, status=None)
                else:
                    # logging.error("file: %s, domain: %s , error: %s" % (file_name, domain, query_result))
                    raise HTTPError(404)
            else:
                raise HTTPError(404)
        except:
            raise HTTPError(404)
        finally:
            self.mysql_client.close_connetc()
            # pass

    @tornado.gen.coroutine
    @tornado.web.asynchronous
    def head(self, *args, **kwargs):
        return self.get(*args, **kwargs)


# noinspection PyAbstractClass,PyAttributeOutsideInit
class DeleteHandlerV1(tornado.web.RequestHandler):
    def initialize(self):
        self.mysql_client = MySQLUtils()
        self.fdfs_client = FDFSUtils()
        self.res_status = dict()

    @tornado.gen.coroutine
    @tornado.web.asynchronous
    def get(self, domain, file_name):
        try:
            if file_name:
                exist_status, exist_info = self.mysql_client.fdfs_exist(file_name, domain)
                if exist_status == 0:    # exist
                    delete_status, delete_result = self.fdfs_client.delete_file(exist_info.get('file_group', ''),
                                                                                exist_info.get('file_local_path', ''))
                    if delete_status:
                        mysql_status, mysql_info = self.mysql_client.fdfs_delete(file_name, domain)
                        if mysql_status == 0:
                            logging.info("file: %s ,domain: %s ,delete mysql success" % (file_name, domain))
                            self.res_status['status'], self.res_status['result'] = 0, None
                        else:
                            raise MysqlExcept(mysql_info)
                    else:
                        raise FdfsExcept(delete_result)
                elif exist_status == 1:
                    raise MysqlExcept('mysql query no data')
                else:
                    raise MysqlExcept(exist_info)
            else:
                raise HandlerExcept("no file name")
        except MysqlExcept as error:
            logging.error("file: %s,domain: %s,error: %s" % (file_name, domain, error.msg))
            self.res_status['status'], self.res_status['result'] = 1, error.msg
        except FdfsExcept as error:
            logging.error("file: %s,domain: %s,error: %s" % (file_name, domain, error.msg))
            self.res_status['status'], self.res_status['result'] = 2, error.msg
        except Exception as error:
            logging.error(str(error))
            self.res_status['status'], self.res_status['result'] = 3, str(error)
        finally:
            self.mysql_client.close_connetc()
            self.write(json.dumps(self.res_status))
            self.finish()


# noinspection PyAbstractClass,PyAttributeOutsideInit
class InfoHandlerV1(tornado.web.RequestHandler):
    def initialize(self):
        self.set_header('Content-type', 'application/json')
        self.mysql_client = MySQLUtils()
        self.res_status = dict()

    @tornado.gen.coroutine
    @tornado.web.asynchronous
    def get(self, domain, file_name):
        try:
            if file_name:
                query_status, query_result = self.mysql_client.raw_sql_fdfs_file_info(file_name.strip(), domain)
                if query_status == 0:
                    self.res_status['status'], self.res_status['result'] = 0, query_result
                elif query_status == 1:
                    raise HandlerExcept('mysql query no data')
                else:
                    raise MysqlExcept("mysql query fail , error:%s" % str(query_result))
            else:
                raise HandlerExcept("no file name")
        except MysqlExcept as error:
            logging.error("file: %s,domain: %s,error: %s" % (file_name, domain, error.msg))
            self.res_status['status'], self.res_status['result'] = 1, error.msg
        except HandlerExcept as error:
            logging.info("file: %s,domain: %s,error: %s" % (file_name, domain, error.msg))
            self.res_status['status'], self.res_status['result'] = 2, error.msg
        except Exception as error:
            logging.error(str(error))
            self.res_status['status'], self.res_status['result'] = 3, str(error)
        finally:
            self.mysql_client.close_connetc()
            self.write(json.dumps(self.res_status))
            self.finish()


# noinspection PyAbstractClass,PyAttributeOutsideInit
class StorageHandlerV1(tornado.web.RequestHandler):
    def initialize(self):
        self.fdfs_client = FDFSUtils()
        self.res_status = dict()
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', 'X-Requested-With')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.set_header('Access-Control-Max-Age', 1000)
        self.set_header('Access-Control-Allow-Headers', '*')
        self.set_header('Content-type', 'application/json')

    @tornado.gen.coroutine
    @tornado.web.asynchronous
    def get(self, *args, **kwargs):
        try:
            fdfs_all_status, fdfs_all_info = self.fdfs_client.list_all_groups()
            if fdfs_all_info:
                all_info, all_group, group_detail = fdfs_all_info
                result = {
                    "all_info": all_info,
                    "all_group": all_group,
                    "group_detail": group_detail
                }
                self.res_status['status'], self.res_status['result'] = 0, result
            else:
                raise FdfsExcept(fdfs_all_info)
        except FdfsExcept as error:
            logging.error(error.msg)
            self.res_status['status'], self.res_status['result'] = 1, error.msg
        except Exception as error:
            logging.error(str(error))
            self.res_status['status'], self.res_status['result'] = 2, str(error)
        finally:
            self.write(json.dumps(self.res_status))
            self.finish()


# noinspection PyAbstractClass,PyAttributeOutsideInit,PyBroadException
class IndexHandlerV1(tornado.web.RequestHandler):
    def initialize(self):
        self.fdfs_client = FDFSUtils()

    @tornado.gen.coroutine
    @tornado.web.asynchronous
    def get(self, *args, **kwargs):
        try:
            fdfs_all_status, fdfs_all_info = self.fdfs_client.list_all_groups()
            if fdfs_all_info:
                all_info, all_group, group_detail = fdfs_all_info
                self.render('index.html', all_info=all_info, all_group=all_group, group_detail=group_detail)
            else:
                pass
        except:
            pass
        finally:
            pass


# noinspection PyAbstractClass,PyAttributeOutsideInit,PyBroadException
class GetDomainHandlerV1(tornado.web.RequestHandler):
    def initialize(self):
        self.set_header('Content-type', 'application/json')
        self.mysql_client = MySQLUtils()
        self.res_status = dict()

    @tornado.gen.coroutine
    @tornado.web.asynchronous
    def get(self, *args, **kwargs):
        try:
            all_domain_stat, all_domain_info = self.mysql_client.get_all_domain()
            if all_domain_stat == 0:
                self.res_status['status'], self.res_status['result'] = 0, all_domain_info
            elif all_domain_stat == 1:
                self.res_status['status'], self.res_status['result'] = 0, all_domain_info
            else:
                MysqlExcept('query all domain error: %s' % all_domain_info)
        except MysqlExcept as error:
            logging.error("%s" % error.msg)
            self.res_status['status'], self.res_status['result'] = 1, error.msg
        except Exception as error:
            logging.error(str(error))
            self.res_status['status'], self.res_status['result'] = 2, str(error)
        finally:
            self.mysql_client.close_connetc()
            self.write(json.dumps(self.res_status))
            self.finish()


# noinspection PyAbstractClass,PyAttributeOutsideInit,PyBroadException
class CreateDomainHandlerV1(tornado.web.RequestHandler):
    def initialize(self):
        self.set_header('Content-type', 'application/json')
        self.mysql_client = MySQLUtils()
        self.res_status = dict()

    @tornado.gen.coroutine
    @tornado.web.asynchronous
    def get(self, domain):
        try:
            if domain:
                domain_exist_stat, domain_exist_info = self.mysql_client.domain_id_exist(domain)
                if domain_exist_stat == 1:
                    domain_insert_stat, domain_insert_info = self.mysql_client.id_insert(domain)
                    if domain_exist_stat:
                        logging.info("domain %s create success" % domain)
                        self.res_status['status'], self.res_status['result'] = 0, 'domain create success'
                    else:
                        raise MysqlExcept('create domain error: %s' % domain_insert_info)
                elif domain_exist_stat == 0:
                    raise MysqlExcept('create domain error: domain exist')
                else:
                    raise MysqlExcept('create domain error: %s' % domain_exist_info)
            else:
                raise HandlerExcept("No domain")
        except HandlerExcept as error:
            self.res_status['status'], self.res_status['result'] = 1, error.msg
        except MysqlExcept as error:
            logging.error("%s" % error.msg)
            self.res_status['status'], self.res_status['result'] = 2, error.msg
        except Exception as error:
            logging.error(str(error))
            self.res_status['status'], self.res_status['result'] = 3, str(error)
        finally:
            self.mysql_client.close_connetc()
            self.write(json.dumps(self.res_status))
            self.finish()


# noinspection PyAbstractClass,PyAttributeOutsideInit,PyBroadException
class DeleteDomainHandlerV1(tornado.web.RequestHandler):
    def initialize(self):
        self.set_header('Content-type', 'application/json')
        self.mysql_client = MySQLUtils()
        self.res_status = dict()

    @tornado.gen.coroutine
    @tornado.web.asynchronous
    def get(self, domain):
        try:
            if domain:
                domain_exist_stst, domain_exist_info = self.mysql_client.domain_id_exist(domain)
                if domain_exist_stst == 0:
                    domain_empty_stat, domain_empty_info = self.mysql_client.fdfs_empty(domain)
                    if domain_empty_stat == 0:
                        domain_delete_stat, domain_delete_info = self.mysql_client.delete_domain(domain)
                        if domain_delete_stat == 0:
                            logging.info("domain %s delete success" % domain)
                            self.res_status['status'], self.res_status['result'] = 0, 'domain delete success'
                        else:
                            raise MysqlExcept('delete domain error: %s' % domain_delete_info)
                    elif domain_empty_stat == 1:
                        raise MysqlExcept('Domain not empty')
                    else:
                        raise MysqlExcept(domain_empty_info)
                elif domain_exist_stst == 1:
                    raise MysqlExcept('not this domain')
                else:
                    raise MysqlExcept(domain_exist_info)
            else:
                raise HandlerExcept("No domain")
        except HandlerExcept as error:
            self.res_status['status'], self.res_status['result'] = 1, error.msg
        except MysqlExcept as error:
            logging.error("%s" % error.msg)
            self.res_status['status'], self.res_status['result'] = 2, error.msg
        except Exception as error:
            logging.error(str(error))
            self.res_status['status'], self.res_status['result'] = 3, str(error)
        finally:
            self.mysql_client.close_connetc()
            self.write(json.dumps(self.res_status))
            self.finish()


# noinspection PyAbstractClass,PyAttributeOutsideInit,PyBroadException
class ListFileHandlerV1(tornado.web.RequestHandler):
    def initialize(self):
        self.set_header('Content-type', 'application/json')
        self.mysql_client = MySQLUtils()
        self.res_status = dict()

    @tornado.gen.coroutine
    @tornado.web.asynchronous
    def get(self):
        domain = self.get_argument('domain', default='test', strip=True)
        limit = self.get_argument('limit', default='10', strip=True)
        try:
            if isinstance(int(limit), int):
                domain_file_stat, domain_file_info = self.mysql_client.list_file(domain, int(limit))
                if domain_file_stat == 0:
                    self.res_status['status'], self.res_status['result'] = 0, domain_file_info
                elif domain_file_stat == 1:
                    self.res_status['status'], self.res_status['result'] = 0, domain_file_info
                else:
                    raise MysqlExcept(domain_file_info)
            else:
                raise HandlerExcept("Limit Not Number")
        except HandlerExcept as error:
            self.res_status['status'], self.res_status['result'] = 1, error.msg
        except MysqlExcept as error:
            logging.error("%s" % error.msg)
            self.res_status['status'], self.res_status['result'] = 2, error.msg
        except Exception as error:
            logging.error(str(error))
            self.res_status['status'], self.res_status['result'] = 3, str(error)
        finally:
            self.mysql_client.close_connetc()
            self.write(json.dumps(self.res_status))
            self.finish()


# noinspection PyAbstractClass,PyAttributeOutsideInit
class GetPoolHandlerV1(tornado.web.RequestHandler):
    def initialize(self):
        self.set_header('Content-type', 'application/json')
        self.mysql_client = MySQLUtils()
        self.res_status = dict()

    @tornado.gen.coroutine
    @tornado.web.asynchronous
    def get(self):
        try:
            connections_pool = self.mysql_client.get_pool()
            self.res_status['status'], self.res_status['result'] = 0, connections_pool
        except Exception as error:
            logging.error(str(error))
            self.res_status['status'], self.res_status['result'] = 1, str(error)
        finally:
            self.mysql_client.close_connetc()
            self.write(json.dumps(self.res_status))
            self.finish()



