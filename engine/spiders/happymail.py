import scrapy
from scrapy.utils.response import open_in_browser
from scrapy.http import Request
from scrapy.spiders.init import InitSpider

import datetime

import engine.env as env

from ..items.post import PostItem

HAPPYMAIL_DOMAIN = 'happymail.co.jp'
HAPPYMAIL_BASE_URL = 'https://happymail.co.jp'
HAPPYMAIL_LOGIN_URL = "https://happymail.co.jp/sp/loginform.php"
HAPPYMAIL_ENTRY_URL = HAPPYMAIL_BASE_URL + '/sp/app/html/'
HAPPYMAIL_BOARD_URL = HAPPYMAIL_ENTRY_URL + "keijiban.php"


def authentication_failed(response):
    # TODO: Check the contents of the response and return True if it failed
    # or False if it succeeded.
    pass


class HappymailSpider(InitSpider):
    name = 'happymail'
    allowed_domains = [HAPPYMAIL_DOMAIN]
    start_urls = [HAPPYMAIL_BOARD_URL]

    def __init__(self, area="神奈川県", days=7, *args, **kwargs):
        super(HappymailSpider, self).__init__(*args, **kwargs)
        self.area = area
        self.days = int(days)

    def init_request(self):
        yield scrapy.Request(HAPPYMAIL_LOGIN_URL, callback=self.login)

    def login(self, response):
        return scrapy.FormRequest.from_response(
            response,
            formdata={
                'TelNo': env.HAPPYMAIL_LOGIN_USER,
                'Pass': env.HAPPYMAIL_LOGIN_PASSWORD
            },
            callback=self.initialized)

    def parse(self, response):
        open_in_browser(response)

        # if authentication_failed(response):
        #     self.logger.error("Login failed")
        #     return
        # else:
        #     pass
        # yield Request(HAPPYMAIL_BOARD_URL, self.set_area)
        # if self.area == "東京都":
        #     yield Request(WAKUWAKU_SETTING_TOKYO_URL, self.set_area)
        # else:
        #     yield Request(WAKUWAKU_SETTING_KANAGAWA_URL, self.set_area)

    def set_area(self, response):
        # open_in_browser(response)
        # board_url_list = [
        #     WAKUWAKU_BOARD_SUGUAITAI_URL, WAKUWAKU_BOARD_KYOJANAIKEDO_URL,
        #     WAKUWAKU_BOARD_ADULT_URL, WAKUWAKU_BOARD_OTONANOKOIBITOKOUHO_URL,
        #     WAKUWAKU_BOARD_ABNORMAL_URL, WAKUWAKU_BOARD_MIDDLEAGE_URL,
        #     WAKUWAKU_BOARD_KIKONSHA_URL
        # ]

        # for board_url in board_url_list:
        #     yield Request(url=board_url + "&p=1", callback=self.parse_board)

    # def parse_board(self, response):
    #     # open_in_browser(response)
    #     # post_list = []

    #     post_list = response.css("ul.profile_list")

    #     for p in post_list:
    #         post = PostItem()

    #         item = p.css("div.profile__item")

    #         partial_url = item.css('a::attr(href)').extract_first()

    #         post['id'] = partial_url.split('id=')[1]
    #         post["url"] = WAKUWAKU_BASE_URL + partial_url

    #         post["name"] = item.css('p.profile__name::text').extract_first()
    #         post["prefecture"] = self.area
    #         post["genre"] = item.css(
    #             'p.icon_bbs_category::text').extract_first()
    #         post["city"] = item.css(
    #             'span.profile__address::text').extract_first()

    #         image_url = item.css('div.profile__image').css(
    #             'img::attr(src)').extract_first()
    #         if 'thumbnail_no_image.png' in image_url:
    #             post[
    #                 'image_url'] = WAKUWAKU_BASE_URL + "/img/wmsp/common/thumbnail_no_image.png"  # noqa
    #         else:
    #             post['image_url'] = image_url
    #         post['age'] = item.css('span.profile__age::text').extract_first()
    #         post['title'] = item.css('p.profile__text::text').extract_first()
    #         post['post_at'] = item.css('p.profile__date::text').extract_first()

    #         yield post

    #         now = datetime.datetime.now()
    #         try:
    #             post_at = datetime.datetime.strptime(post['post_at'],
    #                                                  '%m/%d %H:%M')
    #         except Exception:
    #             post_at = datetime.datetime.strptime(post['post_at'],
    #                                                  '%Y/%m/%d %H:%M')

    #         if now.month == 1 and post_at.month == 12:
    #             post_at = post_at.replace(year=now.year - 1)
    #         else:
    #             post_at = post_at.replace(year=now.year)

    #         days_ago = now - datetime.timedelta(days=self.days)
    #         if post_at > days_ago:
    #             page_no = int(response.url.split("&p=")[1])
    #             next_url = get_wakuwaku_board_url(3) + "&p=" + str(page_no + 1)
    #             yield Request(url=next_url, callback=self.parse_board)
