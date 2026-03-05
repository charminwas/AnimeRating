import scrapy
import json
from ..items import BangumiSeasonsItem

class ExtractSeasonsSpider(scrapy.Spider):
    name = "extract_seasons"
    allowed_domains = ["bangumi.tv"]

    def start_requests(self):
        #打开事先准备好的json
        # with open('bangumi_first.json', 'r', encoding='utf-8') as f:
        #     self.anime_list = json.load(f)

        #用测试文件调试
        with open('sec.json', 'r', encoding='utf-8') as f:
            self.anime_list = json.load(f)
        
        #提取现有的序号和评分，构造url
        for anime in self.anime_list:
            index = anime['index']
            score = anime['score']
            start_url = f'https://bangumi.tv/subject/{index}'
            yield scrapy.Request(
                url=start_url,
                callback=self.parse_first,
                meta={
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
        
        name = self.get_name(response)  #弥补之前提取名称的错误
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
        next_info = self.get_next(response)
        if next_info:
            yield scrapy.Request(
                url=next_info[0],
                callback=self.parse_next,
                meta={
                    'index':next_info[1],
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

        name = self.get_name(response)
        item['season_name'] = name

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
        next_info = self.get_next(response)
        if next_info:
            yield scrapy.Request(
                url=next_info[0],
                callback=self.parse_next,
                meta={
                    'index':next_info[1],
                    'series_name':series_name,
                    'season_num':season_num + 1
                },
                errback=self.handle_error
            )




    """
    辅助函数区域
    """

    #错误处理
    def handle_error(self, failure):
        self.logger.error(f"请求失败: {failure.request.url}，原因: {failure.value}")
    
    #获取名称
    def get_name(self, response):
        name = response.xpath(
            "//span[contains(@class, 'tip') and contains(text(), '中文名: ')]/following-sibling::text()"
            ).get(default=' ').strip()
        if not name:
            name = response.xpath(
                "//h1[@class='nameSingle']/a/text()"
                ).get(default='无名称').strip()
        return name
    
    #获取下一页url和index
    def get_next(self, response):
        next_season_sub = response.xpath(
            "//span[text()='续集']/following-sibling::a[1]/@href"
            ).get()
        if not next_season_sub:
            return None
        next_season_sub = next_season_sub.strip()
        next_index = next_season_sub[9:]
        next_season_url = response.urljoin(next_season_sub)
        return (next_season_url, next_index)