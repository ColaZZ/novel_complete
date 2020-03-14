#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
服务器静态配置项数据
"""

import logging

APPS = ("api_v1", )
DEBUG = True
LOGGING_LEVEL = logging.INFO
API_PORT = 8300

# reids服务器
# REDIS_HOST = "127.0.0.1"
# REDIS_PORT = "6379"
# REDIS_DB = 0
# REDIS_DB_SPARE = 2

# mysql服务器
MYSQL_HOST = "47.244.114.115"
MYSQL_PORT = 3306
MYSQL_DB = "distributed_spider"
MYSQL_USER = "root"
MYSQL_PWD = "Fik2mcKWThRbEFyx"

# session配置
# SESSION_TIMEOUT = 600
# SESSION_REDIS_HOST = "127.0.0.1"
# SESSION_REDIS_PORT = "6379"
# SESSION_REDIS_DB = 1