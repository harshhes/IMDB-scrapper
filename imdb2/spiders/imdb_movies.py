import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class ImdbMoviesSpider(CrawlSpider):
    name = 'imdb_movies'
    allowed_domains = ['www.imdb.com']
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36'

    def start_requests(self):
        yield scrapy.Request(url='https://www.imdb.com/chart/top/?ref_=nv_mv_250', headers={'User-Agent':self.user_agent}) 

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//td[@class='titleColumn']/a"), callback='parse_item', follow=True, process_request='get_user_agent'),
    )

    def get_user_agent(self, request, spider):
        request.headers['User-Agent'] = self.user_agent
        return request

    def parse_item(self, response):
       title = response.xpath("//h1/text()").get()
       year = response.xpath("//div[@class='sc-80d4314-2 iJtmbR']/ul/li[1]/a/text()").get()
       rating = response.xpath("(//span[@class='sc-7ab21ed2-1 jGRxWM'])[1]/text()").get()
       views = response.xpath("(//div[@class='sc-7ab21ed2-3 dPVcnq'])[1]/text()").get()
       duration = response.xpath("//div[@class='sc-80d4314-2 iJtmbR']/ul/li/text()").getall()
       director = response.xpath("(//a[@class='ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link'])[1]/text()").get()
       genre = response.xpath("(//div[contains(@class,'ipc-chip-list__scroller')])[1]/child::a/span/text()").get()

       yield {
           "title": title,
           "year": year,
           "rating": f'{rating}/10',
           "views": views,
           "genre": genre,
           "duration": "".join(duration),
           "director": director
        }