import scrapy
# from scrapy.utils.response import open_in_browser

import time
import datetime

from selenium.webdriver import Chrome, ChromeOptions

import engine.env as env

from ..items.post import PostItem
from ..constants.common import USER_AGENT_PIXEL3, CHROMEDRIVER_PATH

MINT_DOMAIN = 'mintj.com'
MINT_BASE_URL = 'https://mintj.com'
MINT_LOGIN_URL = "https://mintj.com/msm/login"
MINT_ENTRY_URL = MINT_BASE_URL + '/msm'
MINT_BOARD_URL = MINT_ENTRY_URL + "/BBS/?sid=&ma=ad1&cid=0"

MINT_MOVE_TOKYO_URL = "https://mintj.com/ms/mb/Prof.aspx?sid=&f=6&s=8&r=2"
MINT_MOVE_KANAGAWA_URL = "https://mintj.com/ms/mb/Prof.aspx?sid=&f=6&s=9&r=2"


class MintSpider(scrapy.Spider):
    name = 'mint'
    allowed_domains = [MINT_DOMAIN]
    start_urls = [MINT_LOGIN_URL]

    def __init__(self, area="神奈川県", days=7, *args, **kwargs):
        super(MintSpider, self).__init__(*args, **kwargs)
        self.area = area
        self.days = int(days)

        options = ChromeOptions()

        options.add_argument("--headless")

        options.add_argument('--user-agent={}'.format(USER_AGENT_PIXEL3))

        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")

        mobile_emulation = {"deviceName": "Nexus 5"}
        options.add_experimental_option("mobileEmulation", mobile_emulation)

        self.driver = Chrome(options=options,
                             executable_path=CHROMEDRIVER_PATH)

    def parse(self, response):

        # Login
        self.driver.get(response.url)

        self.driver.find_element_by_id("loginid").send_keys(
            env.MINT_LOGIN_USER)
        self.driver.find_element_by_id("pwd").send_keys(
            env.MINT_LOGIN_PASSWORD)
        self.driver.find_element_by_name("B1login").click()

        time.sleep(1)

        # 地域の設定
        if self.area == "東京都":
            move_url = MINT_MOVE_TOKYO_URL
        else:
            move_url = MINT_MOVE_KANAGAWA_URL

        self.driver.get(move_url)
        time.sleep(1)

        self.driver.find_element_by_name("B2City").click()
        time.sleep(1)

        # 掲示板へ移動
        self.driver.get(MINT_BOARD_URL)
        time.sleep(1)

        now = datetime.datetime.now()

        def is_scroll_end():
            response_body = self.driver.page_source.encode('cp932', 'ignore')
            temp_resp = response.replace(body=response_body)
            last_item = temp_resp.css('ul#ulList>li')[-1]
            posted_at_str = last_item.css('time::text').extract_first().strip()

            try:
                posted_at = datetime.datetime.strptime(posted_at_str,
                                                       '%m/%d %H:%M')
            except Exception:
                posted_at = datetime.datetime.strptime(posted_at_str,
                                                       '%Y/%m/%d %H:%M')
            if now.month == 1 and posted_at.month == 12:
                last_posted_at = posted_at.replace(year=now.year - 1)
            else:
                last_posted_at = posted_at.replace(year=now.year)

            days_ago = now - datetime.timedelta(days=self.days)

            if last_posted_at > days_ago:
                return False
            else:
                return True

        scroll_counter = 0

        while not is_scroll_end():
            script = 'document.getElementById("nextPageLink").click();'
            self.driver.execute_script(script)
            time.sleep(1)

            scroll_counter += 1
            if scroll_counter > 10:
                break

        response_body = self.driver.page_source.encode('cp932', 'ignore')
        response = response.replace(body=response_body)

        post_list = response.css('ul#ulList>li')

        for item in post_list:
            post = PostItem()

            id = item.css('dd>a::attr(href)').re_first(
                '/msm/BBS/Read/(.*)\/\?sid=&*')  # noqa

            if id is None:
                continue

            post['id'] = id
            post['profile_id'] = ""
            post['profile_url'] = ""
            partial_url = item.css('dd>a::attr(href)').extract_first()
            post["url"] = MINT_BASE_URL + partial_url

            post["image_url"] = item.css(
                'dt>span>img::attr(src)').extract_first()

            post["name"] = item.css(
                'span.list_text::text').extract_first().strip()
            post["prefecture"] = self.area

            post["genre"] = item.css('dd>a>span::text').extract_first().strip()

            city_base = item.css('span.list_subtext::text').extract()[1]
            if self.area == "東京都":
                post['city'] = city_base.replace('東京', '').strip()
            else:
                post['city'] = city_base.replace('神奈川', '').strip()

            post["age"] = item.css('span.list_subtext::text').extract_first(
            ).split("\xa0")[0].strip()

            post['title'] = item.css(
                'span.list_title::text').extract_first().strip()

            posted_at_str = item.css('time::text').extract_first().strip()
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

            post['site'] = "ミントJメール"

            yield post

    def closed(self, reason):
        self.driver.close()
