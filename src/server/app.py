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
import logging
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import options, define
from tornado.web import url


from handlers import handler


# noinspection PyAbstractClass
class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            url(r'/v1/test', handler.TestHandlerV1),
            url(r'/v1/upload', handler.UploadHandlerV1),
            url(r'/v1/list_domain', handler.GetDomainHandlerV1),
            url(r'/v1/list_file', handler.ListFileHandlerV1),
            url(r'/v1/download/(.*)/(.*)', handler.DownloadHandlerV1),
            url(r'/v1/delete/(.*)/(.*)', handler.DeleteHandlerV1),
            url(r'/v1/info/(.*)/(.*)', handler.InfoHandlerV1),
            url(r'/v1/create_domain/(.*)', handler.CreateDomainHandlerV1),
            url(r'/v1/delete_domain/(.*)', handler.DeleteDomainHandlerV1),
            url(r'/v1/pool', handler.GetPoolHandlerV1),
            url(r'/v1/storage', handler.StorageHandlerV1),
            url(r'/', handler.IndexHandlerV1),
            url(r'/index.html', handler.IndexHandlerV1)
        ]
        # xsrf_cookies is for XSS protection add this to all forms: {{ xsrf_form_html() }}
        settings = {
            'static_path': os.path.join(os.path.dirname(__file__), 'static'),
            'template_path': os.path.join(os.path.dirname(__file__), 'templates'),
            'xsrf_cookies': False,
            'debug': True,
            'autoescape': None,
        }
        tornado.web.Application.__init__(self, handlers, **settings)


def main():
    define("port", default=80, type=int)
    define("log_file_prefix", default="tornado.log")
    define("log_to_stderr", default=True)
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application(), max_buffer_size=1024 * 1024 * 1024)
    http_server.listen(options.port)
    logging.info("start tornado server on port: %s" % options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()