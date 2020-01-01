import scrapy
from scrapy.utils.response import open_in_browser
from scrapy.http import Request

import engine.env as env

WAKUWAKU_DOMAIN = '550909.com'
WAKUWAKU_BASE_URL = 'https://550909.com'
WAKUWAKU_ENTRY_URL = WAKUWAKU_BASE_URL + '/m'
WAKUWAKU_LOGIN_URL = "https://login.550909.com/login/"


def authentication_failed(response):
    # TODO: Check the contents of the response and return True if it failed
    # or False if it succeeded.
    pass


class WakuwakuSpider(scrapy.Spider):
    name = 'wakuwaku'
    allowed_domains = [WAKUWAKU_DOMAIN]
    start_urls = [WAKUWAKU_LOGIN_URL]

    def parse(self, response):
        return scrapy.FormRequest.from_response(response,
                                                formdata={
                                                    'email':
                                                    env.WAKUWAKU_LOGIN_USER,
                                                    'password':
                                                    env.WAKUWAKU_LOGIN_PASSWORD
                                                },
                                                callback=self.after_login)

    def after_login(self, response):
        after_login_url = response.url
        wakuwaku_entry_url = after_login_url + "/m/"
        if authentication_failed(response):
            self.logger.error("Login failed")
            return
        else:
            yield Request(url=wakuwaku_entry_url, callback=self.parse_board)

    def parse_board(self, response):
        open_in_browser(response)
