import scrapy
# from scrapy.utils.response import open_in_browser
from scrapy.http import Request

import datetime

import engine.env as env

from ..items.post import PostItem

WAKUWAKU_DOMAIN = '550909.com'
WAKUWAKU_BASE_URL = 'https://550909.com'
WAKUWAKU_ENTRY_URL = WAKUWAKU_BASE_URL + '/m'
WAKUWAKU_LOGIN_URL = "https://login.550909.com/login/"

WAKUWAKU_SETTING_TOKYO_URL = WAKUWAKU_ENTRY_URL + "/setting/set_city?mode=area&city=237&pref=14"  # noqa 東京都渋谷区
WAKUWAKU_SETTING_KANAGAWA_URL = WAKUWAKU_ENTRY_URL + "/setting/set_city?mode=area&city=892&pref=13"  # noqa 神奈川県川崎市中原区


def get_wakuwaku_board_url(genre):
    return WAKUWAKU_ENTRY_URL + "/bbs/list?genre=" + str(genre)


WAKUWAKU_BOARD_SUGUAITAI_URL = get_wakuwaku_board_url(3)
WAKUWAKU_BOARD_KYOJANAIKEDO_URL = get_wakuwaku_board_url(20)
WAKUWAKU_BOARD_ADULT_URL = get_wakuwaku_board_url(4)
WAKUWAKU_BOARD_OTONANOKOIBITOKOUHO_URL = get_wakuwaku_board_url(6)
WAKUWAKU_BOARD_ABNORMAL_URL = get_wakuwaku_board_url(8)
WAKUWAKU_BOARD_MIDDLEAGE_URL = get_wakuwaku_board_url(15)
WAKUWAKU_BOARD_KIKONSHA_URL = get_wakuwaku_board_url(21)
WAKUWAKU_BOARD_HNAOHANASHI_URL = get_wakuwaku_board_url(7)


class WakuwakuSpider(scrapy.Spider):
    name = 'wakuwaku'
    allowed_domains = [WAKUWAKU_DOMAIN]
    start_urls = [WAKUWAKU_LOGIN_URL]

    def __init__(self, area="神奈川県", days=7, *args, **kwargs):
        super(WakuwakuSpider, self).__init__(*args, **kwargs)
        self.area = area
        self.days = int(days)

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
        if self.area == "東京都":
            yield Request(WAKUWAKU_SETTING_TOKYO_URL, self.set_area)
        else:
            yield Request(WAKUWAKU_SETTING_KANAGAWA_URL, self.set_area)

    def set_area(self, response):
        board_url_list = [
            WAKUWAKU_BOARD_SUGUAITAI_URL, WAKUWAKU_BOARD_KYOJANAIKEDO_URL,
            WAKUWAKU_BOARD_ADULT_URL, WAKUWAKU_BOARD_OTONANOKOIBITOKOUHO_URL,
            WAKUWAKU_BOARD_ABNORMAL_URL, WAKUWAKU_BOARD_MIDDLEAGE_URL,
            WAKUWAKU_BOARD_HNAOHANASHI_URL
        ]

        for board_url in board_url_list:
            yield Request(url=board_url + "&p=1", callback=self.parse_board)

    def parse_board(self, response):
        post_list = response.css("ul.profile_list")

        if len(post_list) == 0:
            return

        now = datetime.datetime.now()

        for p in post_list:
            post = PostItem()

            item = p.css("div.profile__item")

            partial_url = item.css('a::attr(href)').extract_first()

            post['id'] = partial_url.split('id=')[1]
            post["url"] = WAKUWAKU_BASE_URL + partial_url

            post["name"] = item.css(
                'p.profile__name::text').extract_first().strip()
            post["prefecture"] = self.area
            post["genre"] = item.css(
                'p.icon_bbs_category::text').extract_first().strip()
            post["city"] = item.css(
                'span.profile__address::text').extract_first().strip()

            image_url = item.css('div.profile__image').css(
                'img::attr(src)').extract_first()
            if 'thumbnail_no_image.png' in image_url:
                post[
                    'image_url'] = WAKUWAKU_BASE_URL + "/img/wmsp/common/thumbnail_no_image.png"  # noqa
            else:
                post['image_url'] = image_url

            post['age'] = item.css(
                'span.profile__age::text').extract_first().strip()
            post['title'] = item.css(
                'p.profile__text::text').extract_first().strip()
            posted_at_str = item.css('p.profile__date::text').extract_first()

            try:
                posted_at = datetime.datetime.strptime(posted_at_str,
                                                       '%m/%d %H:%M')
            except Exception:
                posted_at = datetime.datetime.strptime(posted_at_str,
                                                       '%Y/%m/%d %H:%M')
            if posted_at.month > now.month:
                posted_at = posted_at.replace(year=now.year - 1)
            else:
                posted_at = posted_at.replace(year=now.year)

            post['posted_at'] = posted_at

            post['site'] = "ワクワクメール"
            post['profile_id'] = ""
            post['profile_url'] = ""

            last_posted_at = posted_at
            yield post

        days_ago = now - datetime.timedelta(days=self.days)
        if last_posted_at > days_ago:
            url_info = response.url.split("&p=")
            page_no = int(url_info[1])
            next_url = url_info[0] + "&p=" + str(page_no + 1)
            yield Request(url=next_url, callback=self.parse_board)
