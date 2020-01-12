import scrapy

import time
import datetime

# from scrapy.utils.response import open_in_browser

from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import engine.env as env

from ..items.post import PostItem
from ..constants.common import USER_AGENT_PIXEL3, CHROMEDRIVER_PATH

HAPPYMAIL_DOMAIN = 'happymail.co.jp'
HAPPYMAIL_BASE_URL = 'https://happymail.co.jp'
HAPPYMAIL_LOGIN_URL = "https://happymail.co.jp/login/?Log=newpc"
HAPPYMAIL_ENTRY_URL = HAPPYMAIL_BASE_URL + '/sp/app/html/'
HAPPYMAIL_BOARD_URL = HAPPYMAIL_ENTRY_URL + "keijiban.php"
HAPPYMAIL_AREA_URL = HAPPYMAIL_ENTRY_URL + "area.php"


class HappymailSpider(scrapy.Spider):
    name = 'happymail'
    allowed_domains = [HAPPYMAIL_DOMAIN]
    start_urls = [HAPPYMAIL_LOGIN_URL]

    def __init__(self, area="神奈川県", days=7, *args, **kwargs):
        super(HappymailSpider, self).__init__(*args, **kwargs)
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

        self.driver.find_element_by_name("TelNo").send_keys(
            env.HAPPYMAIL_LOGIN_USER)
        self.driver.find_element_by_name("Pass").send_keys(
            env.HAPPYMAIL_LOGIN_PASSWORD)
        self.driver.find_element_by_id("login_btn").click()

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "p.ds_user_display_name")))

        # 地域の選択
        self.driver.get(HAPPYMAIL_AREA_URL)
        selector = 'input#area-14-temporary' if self.area == "東京都" else 'input#area-13-temporary'  # noqa
        script = "document.querySelector('{}').click();".format(selector)
        self.driver.execute_script(script)
        script = "document.querySelector('button.ds_round_btn_shadow_blue').click();"  # noqa
        self.driver.execute_script(script)

        time.sleep(5)

        # 掲示板へ移動
        self.driver.get(HAPPYMAIL_BOARD_URL)
        time.sleep(3)

        # その他掲示板を選択
        self.driver.find_elements_by_css_selector(
            'li.ds_link_tab_item_bill')[1].click()

        time.sleep(3)

        try:
            while True:
                script = 'window.scrollTo(0, document.body.scrollHeight);'
                self.driver.execute_script(script)
                script = 'document.querySelector("div#load_list_billboard_200.list_load").click();'  # noqa
                self.driver.execute_script(script)
                time.sleep(3)
        except Exception:
            pass

        response = response.replace(body=self.driver.page_source)

        post_list = response.css("li.ds_user_post_link_item_bill")

        now = datetime.datetime.now()

        for item in post_list:
            post = PostItem()
            partial_url = item.css(
                '.ds_post_button>a::attr(onclick)').extract_first().split(
                    "');return")[0].split("(this, '")[1]
            post['id'] = partial_url.split('Mid=')[1]
            post['url'] = 'https:' + partial_url

            partial_url = item.css('a::attr(href)').extract_first()
            post['profile_id'] = partial_url.split('tid=')[1]
            post["profile_url"] = "https:" + partial_url

            post["name"] = item.css(
                '.ds_post_body_name_bill::text').extract_first().strip(
                    '♀\xa0').strip()  # noqa
            post["prefecture"] = self.area

            post["genre"] = item.css(
                'p.round-btn::text').extract_first().strip()

            age_info = item.css(
                '.ds_post_body_age::text').extract_first().split(
                    '\xa0')  # noqa
            post["city"] = age_info[1].strip()
            post["age"] = age_info[0].strip()

            image_url = item.css(
                '.ds_thum_contain_s::attr(style)').extract_first().strip(
                    'background-image: url(').strip(')')

            if 'noimage' in image_url:
                post['image_url'] = "https:" + image_url
            elif 'avatar' in image_url:
                post['image_url'] = "https:" + image_url
            else:
                post['image_url'] = image_url

            post['title'] = item.css(
                '.ds_post_title::text').extract_first().strip()
            posted_at_str = item.css('.ds_post_date::text').extract_first()

            posted_at = datetime.datetime.strptime(posted_at_str,
                                                   '%m/%d %H:%M')  # noqa
            if posted_at.month > now.month:
                posted_at = posted_at.replace(year=now.year - 1)
            else:
                posted_at = posted_at.replace(year=now.year)

            post['posted_at'] = posted_at

            post['site'] = "ハッピーメール"

            yield post

    def closed(self, reason):
        self.driver.close()
