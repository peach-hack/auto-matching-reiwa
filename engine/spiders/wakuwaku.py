import scrapy
from scrapy.utils.response import open_in_browser
from scrapy.http import Request

import datetime

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
            yield Request(url=get_wakuwaku_board_url(3) + "&p=1",
                          callback=self.parse_board)

    def parse_board(self, response):
        # open_in_browser(response)
        # post_list = []

        post_list = response.css("ul.profile_list")

        for p in post_list:
            post = PostItem()

            item = p.css("div.profile__item")

            partial_url = item.css('a::attr(href)').extract_first()

            post['id'] = partial_url.split('id=')[1]
            post["url"] = WAKUWAKU_BASE_URL + partial_url

            post["name"] = item.css('p.profile__name::text').extract_first()
            post["prefecture"] = "神奈川県"
            post["genre"] = 3
            post["city"] = item.css(
                'span.profile__address::text').extract_first()

            image_url = item.css('div.profile__image').css(
                'img::attr(src)').extract_first()
            if 'thumbnail_no_image.png' in image_url:
                post[
                    'image_url'] = WAKUWAKU_BASE_URL + "/img/wmsp/common/thumbnail_no_image.png"  # noqa
            else:
                post['image_url'] = image_url
            post['age'] = item.css('span.profile__age::text').extract_first()
            post['title'] = item.css('p.profile__text::text').extract_first()
            post['post_at'] = item.css('p.profile__date::text').extract_first()

            yield post

            now = datetime.datetime.now()
            try:
                post_at = datetime.datetime.strptime(post['post_at'],
                                                     '%m/%d %H:%M')
            except Exception:
                post_at = datetime.datetime.strptime(post['post_at'],
                                                     '%Y/%m/%d %H:%M')

            if now.month == 1 and post_at.month == 12:
                post_at = post_at.replace(year=now.year - 1)
            else:
                post_at = post_at.replace(year=now.year)

            yesterday = now - datetime.timedelta(days=7)
            if post_at > yesterday:
                page_no = int(response.url.split("&p=")[1])
                next_url = get_wakuwaku_board_url(3) + "&p=" + str(page_no + 1)
                yield Request(url=next_url, callback=self.parse_board)
