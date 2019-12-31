import scrapy

WAKUWAKU_DOMAIN = '550909.com'
WAKUWAKU_URL = 'http://550909.com/m/'


class WakuwakuSpider(scrapy.Spider):
    name = 'wakuwaku'
    allowed_domains = [WAKUWAKU_DOMAIN]
    start_urls = [WAKUWAKU_URL]

    def parse(self, response):
        pass
