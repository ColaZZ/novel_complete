# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import os
import time
import pymysql
import redis
import requests

from .settings import REDIS_HOST, REDIS_PORT, REDIS_DB


class ArticlePipeline(object):
    def __init__(self):
        # self.conn = pymysql.connect(host='127.0.0.1', user='root',
        #                             passwd='123456', db='distributed_spider', charset='utf8')
        self.conn = pymysql.connect(host='47.56.7.182', user='root', port=3306,
                                    passwd='Fik2mcKWThRbEFyx', db='distributed_spider', charset='utf8')
        self.cur = self.conn.cursor()
        redis_pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB,
                                          decode_responses=True)  # redis缓存连接池
        self.redis = redis.StrictRedis(connection_pool=redis_pool, decode_responses=True)

    # 主要处理方法
    def process_item(self, item, spider):
        # article_title = item.get('article_title', '')
        chapter_name = item.get('chapter_name', '')
        # chapter_content = item.get('chapter_content', '')
        chapter_url_base = item.get('chapter_url_base', '')
        article_url = item.get('article_url', '')
        chapter_sort = item.get('chapter_sort', -1)
        category_id = item.get('category_id', 0)

        chapter_id = int(chapter_url_base[:-5])
        # 爬虫更新时间
        updated_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        # print("crawl_result", chapter_name, chapter_url_base, article_url, chapter_sort)

        sql_id = "select id from articles where url=%s"
        self.cur.execute(sql_id, [article_url])
        result = self.cur.fetchone()
        article_id = result[0] if result else -1

        sql_chapter = "insert into articles_chapter(article_id, chapter_id, chapter_name, updated_at, chapter_sort) " \
                      "values(%s, %s, %s, %s, %s)"

        try:
            if article_id != 1:
                self.cur.execute(sql_chapter, (article_id, chapter_id, chapter_name, updated_at, chapter_sort))
                self.conn.commit()
        except Exception as e:
            print("2", e)

        allowed_domain = '35kushu.com'
        temp_path_base = str(article_url)
        tp_list = temp_path_base.split("/")
        temp_path = tp_list[1]
        cur_path = "/volume/novel_context" + os.path.sep + allowed_domain
        target_path = cur_path + os.path.sep + str(category_id) + os.path.sep + temp_path
        filename_path = cur_path + os.path.sep + str(category_id) + os.path.sep + temp_path + \
                        str(chapter_url_base[:-5]) + '.txt'
        if not os.path.exists(target_path):
            os.makedirs(target_path)
        with open(filename_path, 'w', encoding='utf-8') as f:
            f.write(item['chapter_content'])

        return item
