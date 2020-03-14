#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import requests
from lxml import etree

from apps.found_handler import FoundHandler
from lib.routes import route


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
        node_text = "".join(node_content)

        temp_path_base = str(url[33:])
        tp_list = temp_path_base.split("/")
        # print(tp_list)
        temp_path = tp_list[1]
        chapter_url_base = tp_list[-1]
        cur_path = "/volume/novel_context" + os.path.sep + "35kushu.com"
        target_path = cur_path + os.path.sep + str(category_id) + os.path.sep + temp_path
        filename_path = cur_path + os.path.sep + str(category_id) + os.path.sep + temp_path + os.path.sep + \
                        str(chapter_url_base[:-5]) + '.txt'

        # print(target_path, filename_path)

        if not os.path.exists(target_path):
            os.makedirs(target_path)
        with open(filename_path, 'w', encoding='utf-8') as f:
            f.write(node_text)




