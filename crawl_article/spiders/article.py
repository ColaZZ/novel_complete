# -*- coding: utf-8 -*-

import re

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Request

from utils.chn_to_arab import changeChineseNumToArab
from ..items import ArticleItem
import crawl_article.spiders as cs


# class ArticleSpider(scrapy.Spider):
#     def __init__(self, article_id=None, *args, **kwargs):
#         super(ArticleSpider, self).__init__(*args, **kwargs)
#         print(article_id)
#         self.start_urls = ['https://www.35kushu.com/35zwhtml/%s/%s' % (article_id // 100, article_id)]
#         self.article_id = article_id

class ArticleSpider(cs.ArticleSpider):
    name = "crawl_article"
    allowed_domains = ["35kushu.com"]

    def parse(self, response):
        # start_ulrs = self.start_urls
        menu_list = response.xpath('//div[@id="indexmain"]//div[@id="list"]/dl/dd/a/@title '
                                   '| //div[@id="indexmain"]//div[@id="list"]/dl/dd/a/@href ').extract()
        head_list = response.xpath(
            '//head/meta[@property="og:description"]/@content | //head/meta[@property="og:image"]/@content').extract()
        category_list = response.xpath('//div[@id="indexmain"]//div[@id="indexsidebar"]//div[@id="bread"]/a/@href').extract()
        menu_list_group = [menu_list[i:i + 2] for i in range(0, len(menu_list), 2)]
        for index, ml in enumerate(menu_list_group):
            chapter_url_base = ml[0]
            chapter_name = ml[1]
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

            meta = response.meta
            article_title = meta.get("article_title", "")
            chapter_url = self.start_urls[0] + chapter_url_base
            meta["chapter_url_base"] = chapter_url_base
            meta["chapter_name"] = chapter_name
            meta["article_title"] = article_title
            meta["info"] = head_list[0][:511]
            meta["thumb"] = head_list[1]
            meta["chapter_sort"] = chapter_sort

            category_id = category_list[1].split('/')[1][-1]
            meta["category_id"] = category_id

            yield Request(chapter_url, meta=meta, callback=self.parse_content)

    def parse_content(self, response):
        content = response.xpath('//div[@id="main"]/div[@id="content"]/text()').extract()
        content = "<br><br>".join(content[1:])

        item = ArticleItem()
        item['article_title'] = response.meta["article_title"]
        item['chapter_name'] = response.meta["chapter_name"]
        item['chapter_content'] = content
        item['chapter_url_base'] = response.meta["chapter_url_base"]
        item['article_url'] = self.start_urls[0]
        item['chapter_sort'] = response.meta["chapter_sort"]
        item['category_id'] = response.meta["category_id"]
        yield item
