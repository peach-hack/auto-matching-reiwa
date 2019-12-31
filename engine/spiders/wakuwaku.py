import scrapy


class WakuwakuSpider(scrapy.Spider):
    name = 'wakuwaku'
    allowed_domains = ['550909.com']
    start_urls = ['http://550909.com/']

    def parse(self, response):
        pass
