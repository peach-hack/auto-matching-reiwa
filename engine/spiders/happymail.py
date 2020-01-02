import scrapy
from scrapy.utils.response import open_in_browser
from scrapy.http import Request

# import datetime

from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import engine.env as env

from ..items.post import PostItem
from ..constants.common import USER_AGENT_PIXEL3

HAPPYMAIL_DOMAIN = 'happymail.co.jp'
HAPPYMAIL_BASE_URL = 'https://happymail.co.jp'
HAPPYMAIL_LOGIN_URL = "https://happymail.co.jp/login/?Log=newpc"
HAPPYMAIL_ENTRY_URL = HAPPYMAIL_BASE_URL + '/sp/app/html/'
HAPPYMAIL_BOARD_URL = HAPPYMAIL_ENTRY_URL + "keijiban.php"
HAPPYMAIL_BOARD_URL = HAPPYMAIL_ENTRY_URL + "area.php"


class HappymailSpider(scrapy.Spider):
    name = 'happymail'
    allowed_domains = [HAPPYMAIL_DOMAIN]
    start_urls = [HAPPYMAIL_LOGIN_URL]

    def __init__(self, area="神奈川県", days=7, *args, **kwargs):
        super(HappymailSpider, self).__init__(*args, **kwargs)
        self.area = area
        self.days = int(days)

        options = ChromeOptions()

        # options.add_argument("--headless")

        options.add_argument('--user-agent={}'.format(USER_AGENT_PIXEL3))
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")

        self.driver = Chrome(options=options)

    def parse(self, response):

        # Login
        self.driver.get(response.url)

        self.driver.find_element_by_name("TelNo").send_keys(
            env.HAPPYMAIL_LOGIN_USER)
        self.driver.find_element_by_name("Pass").send_keys(
            env.HAPPYMAIL_LOGIN_PASSWORD)
        self.driver.find_element_by_id("login_btn").click()

        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "p.ds_user_display_name")))

    def closed(self, reason):
        self.driver.close()