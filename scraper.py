from scrapy import *
from scrapy.crawler import CrawlerProcess
from time import sleep

base_request = 'http://markets.businessinsider.com/news/'


class StockCrawler(Spider):

    name = "stock_business_insider"
    start_urls = []
    seen_before = []
    result_articles = []

    def __init__(self, urls):
        self.start_urls = urls

    def parse_text(self, response):
        yield

    def parse_article(self, response):
        print("Xpath at response: " + response.url)
        all_results = response.xpath('//p[string-length(text()) > 150]/text()').extract()
        for string in all_results:
            if string in self.seen_before:
                all_results.remove(string)
            else:
                self.seen_before.append(string)

        all_results = " ".join(all_results)

        result = {"One": all_results}
        print("resulty boi " + result["One"])
        return result


    def parse(self, response):

        raw_links = response.css(".news-link::attr(href)").extract()

        # Clean relative links out.
        article_links = []
        for s in raw_links:
            if s[0:4] != "http":
                s = base_request[0:-6] + s
            article_links.append(s)
        # print(article_links)

        result_titles = response.css(".news-link::text").extract()
        # print("result titles")
        # print(result_titles)

        result_articles = []

        for link in article_links:
            sleep(0.5)
            print("link:" + link)
            one_article = yield Request(link, self.parse_article)
            print(one_article)

        print("result articles")
        print(result_articles)


# Takes a stock name - Returns a dictionary of information to do sentiment analysis on
def scrape_stock(stock):

    urls_to_pass = [base_request + stock, base_request + "intc"]

    # Set the scraper up.
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })
    process.crawl(StockCrawler, urls_to_pass)

    # Blocks until scraper finishes. Should also clean up after itself.
    process.start()

scrape_stock('amd')
