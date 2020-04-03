import scrapy


class ArticleSpider(scrapy.Spider):
    def __init__(self, article_id=None, *args, **kwargs):
        super(ArticleSpider, self).__init__(*args, **kwargs)
        article_id = int(article_id)
        self.start_urls = ['https://www.xkushu.com/35zwhtml/%s/%s/' % (article_id // 1000, article_id)]
        self.article_id = article_id