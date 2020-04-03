# -*- coding: utf-8 -*-

import re

import requests
from lxml import etree
from utils.chn_to_arab import changeChineseNumToArab


def testSpider():
    url = "https://www.xkushu.com/35zwhtml/98/98744/"
    content = requests.get(url).content.decode("utf-8")
    tree = etree.HTML(content)

    # path_content = '//div[@id="indexmain"]//div[@id="list"]/dl/dd/a/@title | //div[@id="indexmain"]//div[@id="list"]/dl/dd/a/@href '
    # node_content = tree.xpath(path_content)
    # menu_list_group = [node_content[i:i + 2] for i in range(0, len(node_content), 2)]

    # head_path = '//head/meta[@property="og:description"]/@content | //head/meta[@property="og:image"]/@content'
    # node_content = tree.xpath(head_path)

    category_path = '//div[@id="indexmain"]//div[@id="indexsidebar"]//div[@id="bread"]/a/@href'
    node_content = tree.xpath(category_path)
    ll = node_content[1].split('/')[1][-1]
    print(ll)

    # // *[ @ id = "bread"] / a[2]
    # print(menu_list_group)
    # for index, ml in enumerate(menu_list_group):
    #     chapter_url_base = ml[0]
    #     chapter_name = ml[1]
    #     count = chapter_name.count("第")
    #     re_str = (count - 1) * "." + "第(.*?)章"
    #     result = re.findall(re_str, chapter_name)
    #     if not result:
    #         if ("序" in result) or ("楔子" in result):
    #             chapter_sort = 0
    #         else:
    #             chapter_sort = -1
    #     else:
    #         try:
    #             chapter_sort = int(changeChineseNumToArab(result[0]))
    #         except:
    #             break
    #
    #     print(chapter_url_base, chapter_name)


if __name__ == "__main__":
    testSpider()
