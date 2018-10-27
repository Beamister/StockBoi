from scrapy import *
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


class StockCrawler(Spider):
    name = "stock_business_insider"
    start_urls = []

    def __init__(self, urls):
        self.start_urls = urls

    def parse(self, response):

        print(response)
        # for article in results_links
        #   article = xpath shit
        #   result_articles =

        result_articles = response.xpath('//div[@id="article-body"]/p/text()').extract()
        print(result_articles)


# Takes a stock name - Returns a dictionary of information to do sentiment analysis on
def scrape(stock):

    urlsToPass = [stock]
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })
    process.crawl(StockCrawler, urlsToPass)
    process.start()


scrape('http://feeds.marketwatch.com/~r/marketwatch/marketpulse/~3/fldo14144Ng/story.aspx')


