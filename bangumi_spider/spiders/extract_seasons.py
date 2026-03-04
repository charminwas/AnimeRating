import scrapy
import json
from ..items import BangumiSeasonsItem

class ExtractSeasonsSpider(scrapy.Spider):
    name = "extract_seasons"
    allowed_domains = ["bangumi.tv"]

    def start_requests(self):
        #打开事先准备好的json
        with open('../bangumi_first.json', 'r', encoding='utf-8') as f:
            self.anime_list = json.load(f)
        
        for anime in self.anime_list:
            index = anime['index']
            series_name = anime['name']
            score = anime['score']
            start_url = f'https://bangumi.tv/subject/{index}/'
            yield scrapy.Request(
                url=start_url,
                callback=self.parse_first,
                meta={
                    'series_name':series_name,
                    'season_num':1,
                    'index':index,
                    'score':score
                },
                errback=self.handle_error
            )

    def parse_first(self, response):
        #提取第一季信息
        item = BangumiSeasonsItem()
        
        item['index'] = response.meta['index']
        
        name = response.meta['series_name']
        item['series_name'] = name
        item['season_name'] = name  #用第一季名字当作系列名字
        
        season_num = response.meta['season_num']
        item['season_num'] = season_num    
        
        score_str = response.meta['score']
        item['score'] = float(score_str) if score_str and score_str.replace('.','').isdigit() else None
        
        rate_num_str = response.xpath(
            "//span[@property='v:votes']/text()"
            ).get(default='0').strip()
        item['rate_num'] = int(rate_num_str) if rate_num_str.isdigit() else 0
        
        yield item


        #续作处理逻辑
        next_season_sub = response.xpath(
            "//span[text()='续集']/following-sibling::a[1]/@href"
            ).get()
        
        if next_season_sub:
            next_season_sub = next_season_sub.strip()
            next_index = next_season_sub[9:]
            next_season_url = response.urljoin(next_season_sub)
            yield scrapy.Request(
                url=next_season_url,
                callback=self.parse_next,
                meta={
                    'index':next_index,
                    'series_name':name,
                    'season_num':season_num + 1
                },
                errback=self.handle_error
            )
            
    def parse_next(self, response):
        #提取本季信息
        item = BangumiSeasonsItem()
        
        item['index'] = response.meta['index']

        series_name = response.meta['series_name']
        item['series_name'] = series_name

        item['season_name'] = response.xpath(
            "//span[contains(@class, 'tip') and contains(text(), '中文名: ')]/following-sibling::text()"
            ).get(default='无名称').strip()

        season_num = response.meta['season_num']
        item['season_num'] = season_num

        score_str = response.xpath(
                "//div[@class='global_score']/span[@class='number']/text()"
                ).get(default='无评分').strip()
        item['score'] = float(score_str) if score_str and score_str.replace('.','').isdigit() else None
        
        rate_num_str = response.xpath(
            "//span[@property='v:votes']/text()"
            ).get(default='0').strip()
        item['rate_num'] = int(rate_num_str) if rate_num_str.isdigit() else 0
        
        yield item


        #寻找下一季
        next_season_sub = response.xpath(
            "//span[text()='续集']/following-sibling::a[1]/@href"
            ).get()
        if next_season_sub:
            next_season_sub = next_season_sub.strip()
            next_index = next_season_sub[9:]
            next_season_url = response.urljoin(next_season_sub)
            yield scrapy.Request(
                url=next_season_url,
                callback=self.parse_next,
                meta={
                    'index':next_index,
                    'series_name':series_name,
                    'season_num':season_num + 1
                },
                errback=self.handle_error
            )

    def handle_error(self, failure):
        self.logger.error(f"请求失败: {failure.request.url}，原因: {failure.value}")