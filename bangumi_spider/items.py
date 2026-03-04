# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BangumiSpiderItem(scrapy.Item):
    index = scrapy.Field()
    name = scrapy.Field()
    score = scrapy.Field()

class BangumiSeasonsItem(scrapy.Item):
    name = scrapy.Field()
    season = scrapy.Field()
    score = scrapy.Field()
    rate_num = scrapy.Field()