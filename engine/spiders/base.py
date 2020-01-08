import scrapy

# from scrapy.utils.response import open_in_browser

from selenium.webdriver import Chrome, ChromeOptions
from ..constants.common import USER_AGENT_PIXEL3, CHROMEDRIVER_PATH


class BaseSpider(scrapy.Spider):
    def __init__(self, *args, **kwargs):

        options = ChromeOptions()

        # options.add_argument("--headless")

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

    def closed(self, reason):
        self.driver.close()
