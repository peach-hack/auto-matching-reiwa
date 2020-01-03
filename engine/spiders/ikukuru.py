import scrapy
from scrapy.utils.response import open_in_browser
from scrapy.http import Request

import time
import datetime

import engine.env as env

from ..items.post import PostItem

IKUKURU_DOMAIN = 'sp.194964.com'
IKUKURU_DOMAIN2 = 'www.194964.com'
IKUKURU_BASE_URL = 'https://sp.194964.com'
IKUKURU_ENTRY_URL = "https://sp.194964.com"
IKUKURU_LOGIN_URL = "https://www.194964.com/registration/login/show_login_tel.html"

IKUKURU_SETTING_TOKYO_URL = IKUKURU_ENTRY_URL + "/bbs/exec_bbs_area_move.html?q=a2YxRkxVbk15bUc5OVJQQnFTbE4yS2N4NVNVUmdOZUtVZkNFbm8yMmtqcz0%3D"  # noqa 東京都
IKUKURU_SETTING_KANAGAWA_URL = IKUKURU_ENTRY_URL + "/bbs/exec_bbs_area_move.html?q=by9qUHBrQTl5eVJ6bnMvcnBzelZEWDlOZGc2V2pyMkRyT3YzSzJraWtTaz0%3D"  # noqa 神奈川県


def get_ikukuru_board_url(query_key):
    return IKUKURU_ENTRY_URL + "/bbs/show_bbs.html?q=" + query_key


IKUKURU_BOARD_SUGUAITAI_URL = get_ikukuru_board_url(
    "ZTJvTzJzRGhPQW5yRmsrdm5KeXhFdz09")
IKUKURU_BOARD_HIMITSU_URL = get_ikukuru_board_url(
    "TTVzV090eEJFdG42aEc3ZnYzeitXZz09")
# IKUKURU_BOARD_MAZUHASHOKUJIKARA_URL = "" バグなのかPC画面に飛ばされるので保留
IKUKURU_BOARD_KIKONSHABOSHU_URL = get_ikukuru_board_url(
    "cUg5aU93eGlVUmJCdEM3VVdGdkxpdz09")
IKUKURU_BOARD_MIDDLEAGE_URL = get_ikukuru_board_url(
    "R2psRFFSd3VPSE5oZFlBdTkrUXhPc0ZWeVhvdWpDd0JsaG9NTHNSSXpOWT0%3D")
IKUKURU_BOARD_ABNORMAL_URL = get_ikukuru_board_url(
    "NHB2TUxzTDZOTUVSaTZOUjFnWkJYZnNadkoxU2hQNVNQblRnT1ZJUlV4ND0%3D")


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
        if self.area == "東京都":
            yield Request(IKUKURU_SETTING_TOKYO_URL, self.set_area)
        else:
            yield Request(IKUKURU_SETTING_KANAGAWA_URL, self.set_area)

    def set_area(self, response):
        board_url_list = [
            IKUKURU_BOARD_SUGUAITAI_URL, IKUKURU_BOARD_HIMITSU_URL,
            IKUKURU_BOARD_ABNORMAL_URL, IKUKURU_BOARD_KIKONSHABOSHU_URL,
            IKUKURU_BOARD_MIDDLEAGE_URL
        ]

        for board_url in board_url_list:
            yield Request(url=board_url, callback=self.parse_board)

    def parse_board(self, response):
        time.sleep(1)
        post_list = response.css(".refinedBbsDesign.bgMiddle")

        if len(post_list) == 0:
            return

        for item in post_list:
            post = PostItem()

            partial_url = item.css('a::attr(href)').extract_first()

            post['id'] = partial_url.split('?q=')[1]
            post["url"] = IKUKURU_BASE_URL + partial_url

            try:
                name_age = item.css(
                    '.contentsTextContribute>div::text').extract()[1]
                post["name"] = name_age.split()[0].strip()
                post['age'] = name_age.split()[1].strip()
            except Exception:
                name_age = item.css(
                    '.contentsTextContribute>div::text').extract()
                post["name"] = name_age[1].strip()
                post['age'] = name_age[2].strip()

            post["prefecture"] = self.area
            post["genre"] = response.css(
                'article>div.bgTopBlue>p::text').extract_first().split('\n')[0]
            post["city"] = item.css(
                '.refinedBbsDesign>span::text').extract()[-1]

            image_url = item.css(
                ".contentsImgContribute>img::attr(src)").extract_first()
            post['image_url'] = image_url

            post['title'] = item.css(
                "p.textComment>a::text").extract_first().strip()
            post['post_at'] = item.css(
                "p.timeContribute::text").extract_first()
            # last_post_at = post['post_at']

            yield post

        # now = datetime.datetime.now()
        # try:
        #     post_at = datetime.datetime.strptime(last_post_at, '%m/%d %H:%M')
        # except Exception:
        #     post_at = datetime.datetime.strptime(last_post_at,
        #                                          '%Y/%m/%d %H:%M')

        # if now.month == 1 and post_at.month == 12:
        #     post_at = post_at.replace(year=now.year - 1)
        # else:
        #     post_at = post_at.replace(year=now.year)
        # days_ago = now - datetime.timedelta(days=self.days)

        # if post_at > days_ago:
        #     partial_url = response.css(
        #         '.nextBtn>a::attr(href)').extract_first()
        #     next_url = "https://sp.194964.com/bbs/show_bbs.html" + partial_url  # noqa
        #     yield Request(url=next_url, callback=self.parse_board)