#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import re
import time

import requests
from lxml import etree

from apps.found_handler import FoundHandler
from lib.routes import route
from lib.chn_to_arab import changeChineseNumToArab


@route('/complete')
class CompleteHandler(FoundHandler):
    async def post(self):
        # url = "https://www.35kushu.com/35zwhtml/83/83344/11317960.html"
        url = self.get_argument("url", " ")
        category_id = int(self.get_argument("category_id", " ") or 0)
        if not url:
            return self.write_json(status=-1, msg="请稍后重试")

        url = "https://www.35kushu.com/35zwhtml/" + url
        content = requests.get(url).content.decode("utf-8")
        tree = etree.HTML(content)
        path_content = '//div[@id="main"]/div[@id="content"]/text()'
        node_content = tree.xpath(path_content)
        node_text = "<br><br>".join(node_content[1:])

        temp_path_base = str(url[33:])
        tp_list = temp_path_base.split("/")
        # print(tp_list)
        temp_path = tp_list[1]
        chapter_url_base = tp_list[-1]
        cur_path = "/volume/novel_context" + os.path.sep + "35kushu.com"
        # cur_path = "/mnt/d/"
        target_path = cur_path + os.path.sep + str(category_id) + os.path.sep + temp_path
        filename_path = cur_path + os.path.sep + str(category_id) + os.path.sep + temp_path + os.path.sep + \
                        str(chapter_url_base[:-5]) + '.txt'

        # print(target_path, filename_path)

        # print(node_text)
        if not os.path.exists(target_path):
            os.makedirs(target_path)
        with open(filename_path, 'w', encoding='utf-8') as f:
            f.write(node_text)


@route('/respider')
class ReSpiderHandler(FoundHandler):
    async def get(self):
        article_id = self.get_argument("article_id", " ")

        if not article_id:
            return self.write_json(status=-1, msg="请稍后重试")

        cur = self.cur
        # start_urls = ['https://www.35kushu.com']
        allowed_domain = '35kushu.com'
        sql = "select url, category_id from articles where id = %s"
        cur.execute(sql, (article_id))
        result = cur.fetchone()
        url = result.get("url", "") if result else ""
        category_id = result.get("category_id", 0) if result else 0

        content = requests.get(url).content.decode("utf-8")
        tree = etree.HTML(content)
        menu_list = tree.xpath('//div[@id="indexmain"]//div[@id="list"]/dl/dd/a/@title '
                                   '| //div[@id="indexmain"]//div[@id="list"]/dl/dd/a/@href ')
        menu_list_group = [menu_list[i:i + 2] for i in range(0, len(menu_list), 2)]
        for mlg in menu_list_group:
            chapter_url_base = mlg[0]
            chapter_name = mlg[1]

            count = chapter_name.count("第")
            re_str = (count - 1) * "." + "第(.*?)章"
            result = re.findall(re_str, chapter_name)
            if not result:
                if ("序" in result) or ("楔子" in result):
                    chapter_sort = 0
                else:
                    chapter_sort = -1
            else:
                try:
                    chapter_sort = int(changeChineseNumToArab(result[0]))
                except:
                    chapter_sort = 0

            chapter_id = int(chapter_url_base[:-5])
            updated_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            # article_url = self.start_urls[0] + tdd[0].xpath('a/@href').extract_first(default=' ')
            sql_chapter = "insert into articles_chapter(article_id, chapter_id, chapter_name, updated_at, chapter_sort) " \
                          "values(%s, %s, %s, %s, %s)"
            cur.execute(sql_chapter, (article_id, chapter_id, chapter_name, updated_at, chapter_sort))
            cur.connection.commit()

            chapter_url = url + chapter_url_base
            chapter_content = requests.get(chapter_url).content.decode("utf-8")
            tree = etree.HTML(chapter_content)
            chapter_txt = tree.xpath('//div[@id="main"]/div[@id="content"]/text()')
            chapter_txt = "<br><br>".join(chapter_txt[1:])

            print(article_id, chapter_id, chapter_name, updated_at, chapter_sort)

            temp_path_base = str(url)
            tp_list = temp_path_base.split("/")
            temp_path = tp_list[1]
            cur_path = "/volume/novel_context" + os.path.sep + allowed_domain
            target_path = cur_path + os.path.sep + str(category_id) + os.path.sep + temp_path
            filename_path = cur_path + os.path.sep + str(category_id) + os.path.sep + temp_path + \
                            str(chapter_url_base[:-5]) + '.txt'
            if not os.path.exists(target_path):
                os.makedirs(target_path)
            with open(filename_path, 'w', encoding='utf-8') as f:
                f.write(chapter_txt)







