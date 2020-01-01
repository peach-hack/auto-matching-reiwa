import scrapy
from scrapy.utils.response import open_in_browser
from scrapy.http import Request

import engine.env as env

from ..items.post import PostItem

WAKUWAKU_DOMAIN = '550909.com'
WAKUWAKU_BASE_URL = 'https://550909.com'
WAKUWAKU_ENTRY_URL = WAKUWAKU_BASE_URL + '/m'
WAKUWAKU_LOGIN_URL = "https://login.550909.com/login/"


def get_wakuwaku_board_url(genre):
    return WAKUWAKU_ENTRY_URL + "/bbs/list?genre=" + str(genre)


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
        if authentication_failed(response):
            self.logger.error("Login failed")
            return
        else:
            yield Request(url=get_wakuwaku_board_url(3),
                          callback=self.parse_board)

    def parse_board(self, response):
        post_list = response.css("ul.profile_list")

        for p in post_list:
            post = PostItem()

            item = p.css("div.profile__item")

            partial_url = item.css('a::attr(href)').extract_first()

            post['id'] = int(partial_url.split('id=')[1])
            post["url"] = WAKUWAKU_BASE_URL + partial_url

            post["name"] = item.css('p.profile__name::text').extract_first()
            post["prefecture"] = "神奈川県"
            post["genre"] = 3
            post["city"] = item.css(
                'span.profile__address::text').extract_first()

            post["image_url"] = WAKUWAKU_BASE_URL + item.css(
                'div.profile__image').xpath('//img/@src').extract_first()
            post['age'] = item.css('span.profile__age::text').extract_first()
            post['title'] = item.css('p.profile__text::text').extract_first()
            post['post_at'] = item.css(
                'span.profile__date::text').extract_first()

            yield post
        # open_in_browser(response)
