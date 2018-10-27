from scrapy import *
from scrapy.crawler import CrawlerProcess

base_request = 'http://markets.businessinsider.com/news/'

class StockCrawler(Spider):
    name = "stock_business_insider"
    start_urls = []

    def __init__(self, urls):
        self.start_urls = urls

    def parse(self, response):

        raw_links = response.css(".news-link::attr(href)").extract()

        # Clean relative links out.
        result_links = []
        for s in raw_links:
            if s[0:4] != "http":
                s = base_request[0:-6] + s
            result_links.append(s)
        print(result_links)

        result_titles = response.css(".news-link::text").extract()
        print(result_titles)


def scrape(stock):

    urlsToPass = [base_request + stock, base_request + "intc"]

    # Set the scraper up.
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })
    process.crawl(StockCrawler, urlsToPass)

    # Blocks until scraper finishes. Should also clean up after itself.
    process.start()

scrape('amd')
