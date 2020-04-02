# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ArticleItem(scrapy.Item):
    article_title = scrapy.Field()
    chapter_name = scrapy.Field()
    chapter_content = scrapy.Field()
    chapter_url_base = scrapy.Field()
    article_url = scrapy.Field()
    chapter_sort = scrapy.Field()
    category_id = scrapy.Field()
