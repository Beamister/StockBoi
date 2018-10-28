from scrapy import *
from scrapy.crawler import CrawlerProcess

base_request = 'http://markets.businessinsider.com/news/'

result_articles = {}
article_links = []
result_titles = []


class StockCrawler(Spider):

    name = "stock_business_insider"
    start_urls = []
    seen_before = []

    def __init__(self, urls):
        self.start_urls = urls

    def parse_article(self, response):

        # print("Xpath at response: " + response.url)

        all_results = response.xpath('//p[string-length(text()) > 20]/text()').extract()

        # print(response.url)

        for string in all_results:
            if string in self.seen_before:
                all_results.remove(string)
            else:
                self.seen_before.append(string)

        all_results = " ".join(all_results)
        result_articles[response.url] = all_results


    def parse(self, response):

        raw_links = response.css(".news-link::attr(href)").extract()

        titles = response.css(".news-link::text").extract()

        # print(len(titles))

        for i in range(0, len(titles)):
            result_titles.append(titles[i])

        # Clean out relative links
        for s in raw_links:
            if s[0:4] != "http":
                s = base_request[0:-6] + s
            article_links.append(s)
            result_articles.update({s : ""})


        # print("result titles")
        # print(result_titles)

        for link in article_links:
            request = Request(link, self.parse_article)
            request.meta['dont_redirect'] = True
            yield request

# Takes a stock name - Returns a dictionary of information to do sentiment analysis on
def scrape_stock(stock):

    urls_to_pass = [base_request + stock]

    # Set the scraper up.
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })
    process.crawl(StockCrawler, urls_to_pass)

    # Blocks until scraper finishes. Should also clean up after itself.
    process.start()
    article_count = len(result_articles)

    # print(article_count)
    # print(result_articles)
    # print(len(result_titles))

    data = {"metadata": {"count": article_count, "name": stock}}
    i = 0
    for s in result_articles.keys():
        title = result_titles[i]
        link = s
        article = result_articles[link]
        toAdd = {"link": link, "title": title, "article": article}
        data[i] = toAdd
        i += 1

    # print(data)
    return data
