import scrapy

import time
import datetime

from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException

import engine.env as env

from ..items.post import PostItem
from ..constants.common import USER_AGENT_PIXEL3

PCMAX_DOMAIN = 'pcmax.jp'
PCMAX_BASE_URL = 'https://pcmax.jp'
PCMAX_LOGIN_URL = "https://pcmax.jp/pcm/index.php"
PCMAX_ENTRY_URL = PCMAX_LOGIN_URL
PCMAX_BOARD_URL = "https://pcmax.jp/mobile/bbs_reference.php"


class PcmaxSpider(scrapy.Spider):
    name = 'pcmax'
    allowed_domains = [PCMAX_DOMAIN]
    start_urls = [PCMAX_LOGIN_URL]

    def __init__(self, area="神奈川県", days=7, *args, **kwargs):
        super(PcmaxSpider, self).__init__(*args, **kwargs)
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

        self.driver = Chrome(options=options)

    def parse(self, response):

        # Login
        self.driver.get(response.url)

        self.driver.find_element_by_id("login-tab").click()
        self.driver.find_element_by_id("login_id").send_keys(
            env.PCMAX_LOGIN_USER)
        self.driver.find_element_by_id("login_pw").send_keys(
            env.PCMAX_LOGIN_PASSWORD)
        self.driver.find_element_by_name("login").click()

        time.sleep(1)

        # 掲示板へ移動
        self.driver.get(PCMAX_BOARD_URL)

        time.sleep(1)

        # カテゴリの選択
        # スグ会いたいは defaultで選択されている

        def select_category(n):
            script = 'document.querySelector("#bbs_category{}").click()'.format(  # noqa
                n)
            self.driver.execute_script(script)

        select_category(3)  # スグじゃないけど
        select_category(8)  # 既婚者OK
        select_category(21)  # 変態さん募集

        # 地域を選択
        pref_no = "22" if self.area == "東京都" else "23"
        element = self.driver.find_element_by_name('pref_no')
        select_element = Select(element)
        select_element.select_by_value(pref_no)

        # 40歳以上を検索から除外
        element = self.driver.find_element_by_name('to_age')
        select_element = Select(element)
        select_element.select_by_value("40")

        # 検索実行
        self.driver.find_element_by_name("search").click()
        time.sleep(5)

        def is_scroll_end():
            try:
                self.driver.find_element_by_id('ajax-message')
            except NoSuchElementException:
                return False
            return True

        while not is_scroll_end():
            script = 'window.scrollTo(0, document.body.scrollHeight);'
            self.driver.execute_script(script)
            time.sleep(3)

        response_body = self.driver.page_source.encode('cp932', 'ignore')
        response = response.replace(body=response_body)

        post_list = response.css('.item_box')

        for item in post_list:
            post = PostItem()

            id = item.css('.search_btn>a::attr(onclick)').re_first(
                'viewBbs\((.*)\)')  # noqa

            if id is None:
                continue

            post['id'] = id
            post['profile_id'] = item.css(
                '.search_btn>a::attr(id)').extract_first()
            post["url"] = "https://pcmax.jp/mobile/bbs_detail.php?bbs_id=" + id

            post["image_url"] = ""  # 小さすぎるのでとりあえずいらない

            post["name"] = item.css(
                'span.value1>span>font::text').extract_first().strip()
            post["prefecture"] = self.area

            post["genre"] = item.css('span.value1::text')[4].extract().strip()

            post["city"] = item.css('span.value1::text')[2].extract().strip(
                self.area).strip()
            post["age"] = item.css('span.value1::text')[1].extract().strip(
                '\xa0').strip()

            post['title'] = item.css(
                '.title_link::text').extract_first().strip()
            posted_at_str = item.css('span.value1::text')[3].extract()
            post['posted_at'] = datetime.datetime.strptime(
                posted_at_str, '%Y年%m月%d日 %H:%M')

            post['site'] = "PCMAX"

            yield post

    def closed(self, reason):
        self.driver.close()
