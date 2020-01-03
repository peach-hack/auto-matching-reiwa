import scrapy
from scrapy.utils.response import open_in_browser
from scrapy.http import Request

import datetime

import engine.env as env

from ..items.post import PostItem

IKUKURU_DOMAIN = 'sp.194964.com'
IKUKURU_DOMAIN2 = 'www.194964.com'
IKUKURU_BASE_URL = 'https://sp.194964.com'
IKUKURU_ENTRY_URL = ""
IKUKURU_LOGIN_URL = "https://www.194964.com/registration/login/show_login_tel.html"

IKUKURU_SETTING_TOKYO_URL = IKUKURU_ENTRY_URL + "/setting/set_city?mode=area&city=237&pref=14"  # noqa 東京都渋谷区
IKUKURU_SETTING_KANAGAWA_URL = IKUKURU_ENTRY_URL + "/setting/set_city?mode=area&city=892&pref=13"  # noqa 神奈川県川崎市中原区


def get_wakuwaku_board_url(genre):
    return IKUKURU_ENTRY_URL + "/bbs/list?genre=" + str(genre)


IKUKURU_BOARD_SUGUAITAI_URL = get_wakuwaku_board_url(3)
IKUKURU_BOARD_KYOJANAIKEDO_URL = get_wakuwaku_board_url(20)
IKUKURU_BOARD_ADULT_URL = get_wakuwaku_board_url(4)
IKUKURU_BOARD_OTONANOKOIBITOKOUHO_URL = get_wakuwaku_board_url(6)
IKUKURU_BOARD_ABNORMAL_URL = get_wakuwaku_board_url(8)
IKUKURU_BOARD_MIDDLEAGE_URL = get_wakuwaku_board_url(15)
IKUKURU_BOARD_KIKONSHA_URL = get_wakuwaku_board_url(21)


class IkukuruSpider(scrapy.Spider):
    name = 'ikukuru'
    allowed_domains = [IKUKURU_DOMAIN, IKUKURU_DOMAIN2]
    start_urls = [IKUKURU_LOGIN_URL]

    def __init__(self, area="神奈川県", days=7, *args, **kwargs):
        super(IkukuruSpider, self).__init__(*args, **kwargs)
        self.area = area
        self.days = int(days)

    def parse(self, response):
        return scrapy.FormRequest.from_response(response,
                                                formdata={
                                                    'tel':
                                                    env.IKUKURU_LOGIN_USER,
                                                    'password':
                                                    env.IKUKURU_LOGIN_PASSWORD
                                                },
                                                callback=self.after_login)

    def after_login(self, response):
        pass
        # if self.area == "東京都":
        #     yield Request(IKUKURU_SETTING_TOKYO_URL, self.set_area)
        # else:
        #     yield Request(IKUKURU_SETTING_KANAGAWA_URL, self.set_area)

    def set_area(self, response):
        board_url_list = [
            IKUKURU_BOARD_SUGUAITAI_URL, IKUKURU_BOARD_KYOJANAIKEDO_URL,
            IKUKURU_BOARD_ADULT_URL, IKUKURU_BOARD_OTONANOKOIBITOKOUHO_URL,
            IKUKURU_BOARD_ABNORMAL_URL, IKUKURU_BOARD_MIDDLEAGE_URL,
            IKUKURU_BOARD_KIKONSHA_URL
        ]

        for board_url in board_url_list:
            yield Request(url=board_url + "&p=1", callback=self.parse_board)

    def parse_board(self, response):
        # open_in_browser(response)
        # post_list = []

        post_list = response.css("ul.profile_list")

        for p in post_list:
            post = PostItem()

            item = p.css("div.profile__item")

            partial_url = item.css('a::attr(href)').extract_first()

            post['id'] = partial_url.split('id=')[1]
            post["url"] = IKUKURU_BASE_URL + partial_url

            post["name"] = item.css('p.profile__name::text').extract_first()
            post["prefecture"] = self.area
            post["genre"] = item.css(
                'p.icon_bbs_category::text').extract_first()
            post["city"] = item.css(
                'span.profile__address::text').extract_first()

            image_url = item.css('div.profile__image').css(
                'img::attr(src)').extract_first()
            if 'thumbnail_no_image.png' in image_url:
                post[
                    'image_url'] = IKUKURU_BASE_URL + "/img/wmsp/common/thumbnail_no_image.png"  # noqa
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

            days_ago = now - datetime.timedelta(days=self.days)
            if post_at > days_ago:
                page_no = int(response.url.split("&p=")[1])
                next_url = get_wakuwaku_board_url(3) + "&p=" + str(page_no + 1)
                yield Request(url=next_url, callback=self.parse_board)
