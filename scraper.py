from scrapy import *
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


class StockCrawler(Spider):
    name = "stock_business_insider"
    start_urls = []

    def __init__(self, urls):
        self.start_urls = urls

    def parse(self, response):
        filename = response.url

        with open(filename, 'wb') as f:
            f.write(response.body)

        print(response)
        result_links = response.css(".news-link::attr(href)").extract()
        result_titles = response.css(".news-link::text").extract()
        print(result_links + "\n" + result_titles)

def scrape(stock):

    base_request = 'http://markets.businessinsider.com/news/'
    urlsToPass = [base_request + stock, base_request + "intc"]
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })
    process.crawl(StockCrawler, urlsToPass)
    process.start()

scrape('amd')
