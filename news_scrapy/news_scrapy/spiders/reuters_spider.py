import scrapy


class ReutersSpiderSpider(scrapy.Spider):
    name = "reuters_spider"
    allowed_domains = ["jp.reuters.com"]
    start_urls = ["https://jp.reuters.com"]
    temp_url = ""

    def parse(self, response):
        pass
