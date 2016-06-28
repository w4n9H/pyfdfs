# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: mango
@contact: w4n9@sina.com
@create: 16/3/30
redis 相关接口封装
"""

__author__ = "mango"
__version__ = "0.1"


import redis


# noinspection PyBroadException
class RedisUtils(object):
    def __init__(self, hosts, port, db):
        self.redis_client = redis.Redis(host=hosts, port=port, db=db)

    def set_string(self, key, value_string, ex=None, px=None, nx=False, xx=False):
        """
        存储字符串
        :param key: key  str
        :param value_string:  字符串 value str
        :param ex: 设置过期时间(s) ()
        :param px: 设置过期时间(ms) ()
        :param nx: 如果key不存在则建立
        :param xx: 如果key存在则修改其值
        :return:
        """
        try:
            self.redis_client.set(key, value_string, ex=ex, px=px, nx=nx, xx=xx)
        except:
            return False
        return True

    def get_string(self, key):
        """
        获取字符串 value
        :param key: key  str
        :return:
        """
        r = None
        try:
            r = self.redis_client.mget(key)
        except:
            pass
        finally:
            return r

    def set_list(self, key, value_list):
        """
        存储列表
        :param key: key str
        :param value_list: 列表value  list
        :return:
        """
        try:
            for i in value_list:
                self.redis_client.rpush(key, i.strip())
        except:
            return False
        return True

    def get_list(self, key):
        """
        获取列表 value
        :param key: key  str
        :return:
        """
        r = []
        try:
            r = self.redis_client.lrange(key, 0, -1)
        except:
            pass
        finally:
            return r

    def set_hash(self, key, value_dict):
        """
        存储hash
        :param key: key  (str)
        :param value_dict: hash value  (dict)
        :return:
        """
        try:
            self.redis_client.hmset(key, value_dict)
        except:
            return False
        return True

    def get_hash(self, key):
        """
        获取 hash value
        :param key: key (str)
        :return:
        """
        r = dict()
        try:
            r = self.redis_client.hgetall(key)
        except:
            pass
        finally:
            return r

    def set_set(self, key, value_set):
        """
        存储 集合
        :param key: key (str)
        :param value_set: 集合 (set)
        :return:
        """
        try:
            self.redis_client.sadd(key, value_set)
        except:
            return False
        return True

    def get_set(self, key):
        """
        获取集合
        :param key: key  (str)
        :return:
        """
        r = set()
        try:
            r = self.redis_client.spop(key)
        except:
            pass
        finally:
            return r

    def db_size(self):
        """
        获取db数量
        :return:
        """
        r = 0
        try:
            r = self.redis_client.dbsize()
        except:
            pass
        finally:
            return r

    def get_keys(self):
        """
        获取所有的keys
        :return:
        """
        r = []
        try:
            r = self.redis_client.keys()
        except:
            pass
        finally:
            return r

    def get_type(self, key):
        """
        获取key类型
        :param key: key  (str)
        :return:
        """
        return self.redis_client.type(key)

    def random_key(self):
        """
        随机获取 key
        :return:
        """
        random_key = self.redis_client.randomkey()
        return random_key


if __name__ == '__main__':
    r = RedisUtils(hosts='192.168.13.193', port=6379, db=0)
    print r.set_string('aaaa', '01', ex=10, nx=True)
    print r.get_string('aaaa')
    import time
    time.sleep(11)
    print r.set_string('aaaa', '011', ex=10, nx=True)
    print r.get_string('aaaa')



