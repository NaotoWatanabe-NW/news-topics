import scrapy
from items import YahooNewsItem


class YahooNewsSpider(scrapy.Spider):
    name = "yahoo_news"
    allowed_domains = ["news.yahoo.co.jp"]
    start_urls = ["https://news.yahoo.co.jp"]

    def parse(self, response):
        categories = response.xpath("/html/body/div/header/nav/div[@id='snavi']/ul/li")
        for category in categories:  # トピックスごとに処理する
            link = category
            link = response.urljoin(link)
            yield scrapy.Request(link, callback=self.topic_parse)

    def topic_parse(self, response):
        topics = response.xpath("/html/body/div/div/main/div/div/section/div/div/div/ul/li")
        for topic in topics:
            yield YahooNewsItem(
                title="",
                date="",
                site="",
                url="",
            )
