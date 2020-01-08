import scrapy


class PostItem(scrapy.Item):
    id = scrapy.Field()
    url = scrapy.Field()
    profile_id = scrapy.Field()
    profile_url = scrapy.Field()
    site = scrapy.Field()
    name = scrapy.Field()
    age = scrapy.Field()
    title = scrapy.Field()
    image_url = scrapy.Field()
    posted_at = scrapy.Field()
    genre = scrapy.Field()
    prefecture = scrapy.Field()
    city = scrapy.Field()
    keyword = scrapy.Field()
