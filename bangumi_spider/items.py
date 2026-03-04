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
    index = scrapy.Field()  #唯一序号

    series_name = scrapy.Field()
    season_name = scrapy.Field()
    season_num = scrapy.Field()
    score = scrapy.Field()

    rate_num = scrapy.Field()  #用评分人数代表数据置信度