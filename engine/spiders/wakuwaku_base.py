from .base import BaseSpider

WAKUWAKU_DOMAIN = '550909.com'
WAKUWAKU_BASE_URL = 'https://550909.com'
WAKUWAKU_ENTRY_URL = WAKUWAKU_BASE_URL + '/m'
WAKUWAKU_LOGIN_URL = "https://login.550909.com/login/"

WAKUWAKU_SETTING_TOKYO_URL = WAKUWAKU_ENTRY_URL + "/setting/set_city?mode=area&city=237&pref=14"  # noqa 東京都渋谷区
WAKUWAKU_SETTING_KANAGAWA_URL = WAKUWAKU_ENTRY_URL + "/setting/set_city?mode=area&city=892&pref=13"  # noqa 神奈川県川崎市中原区


class WakuwakuBaseSpider(BaseSpider):
    allowed_domains = [WAKUWAKU_DOMAIN]
    start_urls = [WAKUWAKU_LOGIN_URL]
