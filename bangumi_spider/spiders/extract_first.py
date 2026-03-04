import scrapy
from scrapy.linkextractors import LinkExtractor
from ..items import BangumiSpiderItem
import re

class ExtractFirstSpider(scrapy.Spider):
    name = "extract_first"
    allowed_domains = ["bangumi.tv"]
    start_urls = ["https://bangumi.tv/anime/browser/?sort=trends&page=23"]
    max_page = 22
    current_page = 1

    def parse(self, response):
        #获取详情页
        le1 = LinkExtractor(
        restrict_css='ul#browserItemList.browserFull.browser-list li.item a.subjectCover',
        allow=r'/subject/\d+'
        )
        for link in le1.extract_links(response):
            yield scrapy.Request(link.url, callback=self.parse_each)
        #翻页逻辑，加最大页数
        if self.current_page < self.max_page:
            le2 = LinkExtractor(
                restrict_css='strong.p_cur + a.p',
                allow=r'\?sort=trends&page=(\d+)'
                )
            next_page = le2.extract_links(response)
            if next_page:
                self.current_page += 1
                next_url = next_page[0].url
                yield scrapy.Request(next_url, callback=self.parse)
            else:
                self.logger.info("达到单次页数上线")

    def parse_each(self, response):
        #判断是否是首作
        have_pre = len(response.xpath("//span[text()='前传']/following-sibling::a[2]/text()"))
        have_post = len(response.xpath("//span[text()='续集']/following-sibling::a[2]/text()"))
        if not have_pre and have_post:
            anime = BangumiSpiderItem()

            index_match = re.findall(r'/subject/(\d+)', response.url)
            anime['index'] = index_match[0] if index_match else '无序号'
            
            anime['name'] = response.xpath(
                "//span[contains(@class, 'tip') and contains(text(), '中文名: ')]/following-sibling::text()"
                ).get(default='无名称').strip()
            
            anime['score'] = response.xpath(
                "//div[@class='global_score']/span[@class='number']/text()"
                ).get(default='无评分').strip()
            
            self.logger.info(f"序号：{anime['index']}, 动漫名：{anime['name']}, 评分:{anime['score']}")
            
            yield anime
        else:
            self.logger.info("非首作，已跳过")