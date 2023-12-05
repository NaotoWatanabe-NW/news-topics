import scrapy


class YahooNewsSpider(scrapy.Spider):
    name = "yahoo_news"
    allowed_domains = ["news.yahoo.co.jp"]
    start_urls = ["https://news.yahoo.co.jp"]

    def parse(self, response):
        pass
