import scrapy
# from scrapy.utils.response import open_in_browser
from scrapy.spiders.init import InitSpider
from scrapy_splash import SplashRequest

import engine.env as env

from ..items.post import PostItem

HAPPYMAIL_DOMAIN = 'happymail.co.jp'
HAPPYMAIL_BASE_URL = 'https://happymail.co.jp'
HAPPYMAIL_LOGIN_URL = "https://happymail.co.jp/sp/loginform.php"
HAPPYMAIL_ENTRY_URL = HAPPYMAIL_BASE_URL + '/sp/app/html/'
HAPPYMAIL_BOARD_URL = HAPPYMAIL_ENTRY_URL + "keijiban.php"


class HappymailSpider(InitSpider):
    name = 'happymail'
    allowed_domains = [HAPPYMAIL_DOMAIN]
    start_urls = [HAPPYMAIL_BOARD_URL]

    def __init__(self, area="神奈川県", days=7, *args, **kwargs):
        super(HappymailSpider, self).__init__(*args, **kwargs)
        self.area = area
        self.days = int(days)

    def parse(self, response):
        script = open('./engine/spiders/lua/happymail_read_board.lua').read()
        script = script.replace("happymail_tel_no", env.HAPPYMAIL_LOGIN_USER)
        script = script.replace("happymail_password",
                                env.HAPPYMAIL_LOGIN_PASSWORD)

        yield SplashRequest(
            response.url,
            self.parse_board,
            endpoint='execute',
            args={
                'wait': 0.5,
                'lua_source': script,
                'timeout': 3600
            },
        )

    def parse_board(self, response):
        # open_in_browser(response)

        post_list = response.css("li.ds_user_post_link_item_bill")

        for item in post_list:
            post = PostItem()

            partial_url = item.css('a::attr(href)').extract_first()

            post['id'] = partial_url.split('tid=')[1]
            post["url"] = "https:" + partial_url

            post["name"] = item.css(
                '.ds_post_body_name_bill::text').extract_first().strip(
                    '♀\xa0')  # noqa
            post["prefecture"] = self.area

            post["genre"] = item.css('p.round-btn::text').extract_first()

            age_info = item.css(
                '.ds_post_body_age::text').extract_first().split(
                    '\xa0')  # noqa
            post["city"] = age_info[1]
            post["age"] = age_info[0]

            image_url = item.css(
                '.ds_thum_contain_s::attr(style)').extract_first().strip(
                    'background-image: url(').strip(')')

            if 'noimage' in image_url:
                post['image_url'] = "https:" + image_url
            elif 'avatar' in image_url:
                post['image_url'] = "https:" + image_url
            else:
                post['image_url'] = image_url

            post['title'] = item.css('.ds_post_title::text').extract_first()
            post['post_at'] = item.css('.ds_post_date::text').extract_first()

            yield post
