#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
API接口服务器主进程
"""

import os
import sys
import site
import logging

import redis
from tornado.options import parse_command_line
import tornado.httpserver
import tornado.ioloop
import tornado.web

from settings import *
from utils.routes import route

ROOT = os.path.abspath(os.path.dirname(__file__))
path = lambda *a: os.path.join(*a)
site.addsitedir(path('vendor'))


class Application(tornado.web.Application):
    def __init__(self):
        handlers = route.get_routes()

        app_settings = dict(
            debug=DEBUG,
            autoescape=None,
            gzip=True,
            static_path=os.path.join(ROOT, "static"),
        )

        tornado.web.Application.__init__(self, handlers, **app_settings)
        # self.session_manager = session.SessionManager(app_settings["session_secret"], app_settings["store_options"],
        #                                               app_settings["session_timeout"])


for app_name in APPS:
    __import__("apps.%s" % app_name, fromlist=["handlers"])


def main():
    parse_command_line()
    logging.getLogger().setLevel(LOGGING_LEVEL)
    application = Application()

    http_server = tornado.httpserver.HTTPServer(application, xheaders=True)
    api_port = API_PORT if len(sys.argv) == 1 else int(sys.argv[1])

    http_server.bind(api_port)
    http_server.start()

    print("API Server start on port %s" % api_port)

    try:
        tornado.ioloop.IOLoop.current().start()
    except KeyboardInterrupt:
        logging.info("API Server stoped")
        sys.exit(0)


if __name__ == "__main__":
    main()
