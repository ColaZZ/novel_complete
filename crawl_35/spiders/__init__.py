import scrapy


class DailySpider(scrapy.Spider):
    def __init__(self, *args, **kwargs):
        super(DailySpider, self).__init__(*args, **kwargs)
        self.start_urls = ['https://www.35kushu.com']
