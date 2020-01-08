import scrapy
from scrapy.utils.response import open_in_browser

import time
import engine.env as env

from .wakuwaku_base import WakuwakuBaseSpider

from ..items.post import PostItem
import datetime

WAKUWAKU_DOMAIN = '550909.com'
WAKUWAKU_BASE_URL = 'https://550909.com'
WAKUWAKU_ENTRY_URL = WAKUWAKU_BASE_URL + '/m'
WAKUWAKU_LOGIN_URL = "https://login.550909.com/login/"

WAKUWAKU_SEARCH_URL = WAKUWAKU_ENTRY_URL + "/search/multi/search?bbs=1&genre=adult"  # noqa


class WakuwakuSearchSpider(WakuwakuBaseSpider):
    name = 'wakuwaku_search'
    allowed_domains = [WAKUWAKU_DOMAIN]
    start_urls = [WAKUWAKU_LOGIN_URL]

    def __init__(self, keyword="", *args, **kwargs):
        super(WakuwakuSearchSpider, self).__init__(*args, **kwargs)
        self.keyword = keyword

    def parse(self, response):
        # Login
        self.driver.get(response.url)

        script = "document.getElementsByName('email')[1].value = '{}';".format(
            env.WAKUWAKU_LOGIN_USER)
        self.driver.execute_script(script)
        script = "document.getElementsByName('password')[0].value = '{}';".format(  # noqa
            env.WAKUWAKU_LOGIN_PASSWORD)
        self.driver.execute_script(script)
        self.driver.find_element_by_css_selector(".btn--submit").click()

        time.sleep(3)

        # 検索に移動
        self.driver.get(WAKUWAKU_SEARCH_URL)
        time.sleep(3)

        script = "document.getElementsByName('text')[0].value = '{}';".format(
            self.keyword)
        self.driver.execute_script(script)

        # 検索
        selector = ".BtnSubmit.shortWord"
        script = "document.querySelector('{}').click();".format(selector)
        self.driver.execute_script(script)

        time.sleep(5)

        response = response.replace(body=self.driver.page_source)

        open_in_browser(response)

        post_list = response.css(".ChargeProfList")

        if len(post_list) == 0:
            return

        now = datetime.datetime.now()

        for item in post_list:
            post = PostItem()

            partial_url = item.css('a::attr(href)').extract_first()

            post['id'] = partial_url.split('id=')[1]
            post["url"] = WAKUWAKU_BASE_URL + partial_url

            post["name"] = item.css('.name::text').extract_first().strip()
            post["prefecture"] = ""
            post["genre"] = item.css('.category::text').extract_first().strip()
            post["city"] = item.css('.place::text').extract_first().strip()

            try:
                image_url = item.css('.photoCover::attr(style)').extract_first(
                ).split('background-image: url(\'')[1].split('\')')[0]
                if 'thumbnail_no_image.png' in image_url:
                    post[
                        'image_url'] = WAKUWAKU_BASE_URL + "/img/wmsp/common/thumbnail_no_image.png"  # noqa
                else:
                    post['image_url'] = image_url
            except Exception:
                post['image_url'] = ""

            post['age'] = item.css('.age::text').extract_first().strip()
            post['title'] = item.css(
                'dd.message>span::text').extract_first().strip()
            posted_at_str = item.css('dd.time::text').extract_first().strip()

            try:
                posted_at = datetime.datetime.strptime(posted_at_str,
                                                       '%m/%d %H:%M')
            except Exception:
                posted_at = datetime.datetime.strptime(posted_at_str,
                                                       '%Y/%m/%d %H:%M')
            if now.month == 1 and posted_at.month == 12:
                posted_at = posted_at.replace(year=now.year - 1)
            else:
                posted_at = posted_at.replace(year=now.year)

            post['posted_at'] = posted_at

            post['site'] = "ワクワクメール"
            post['profile_id'] = ""
            post['profile_url'] = ""
            post['keyword'] = self.keyword

            # last_posted_at = posted_at
            yield post

        # days_ago = now - datetime.timedelta(days=self.days)
        # if parse_next and last_posted_at > days_ago:
        #     url_info = response.url.split("&p=")
        #     page_no = int(url_info[1])
        #     next_url = url_info[0] + "&p=" + str(page_no + 1)
        #     yield Request(url=next_url, callback=self.parse_board)
