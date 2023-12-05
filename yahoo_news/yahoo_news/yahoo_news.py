import scrapy
from items import YahooNewsItem
from datetime import datetime


class YahooNewsSpider(scrapy.Spider):
    name = "yahoo_news"
    allowed_domains = ["news.yahoo.co.jp"]
    start_urls = ["https://news.yahoo.co.jp"]

    def parse(self, response):
        categories = response.xpath("/html/body/div/header/nav/div[@id='snavi']/ul[1]/li")
        for category in categories:  # トピックスごとに処理する
            link = category.xpath("//a/@href").get()
            link = response.urljoin(link)
            yield scrapy.Request(link, callback=self.topic_parse)

    def topic_parse(self, response):
        topics = response.xpath("/html/body/div/div/main/div/div/section/div/div/div/ul/li")
        for topic in topics:
            yield YahooNewsItem(
                title=topic.xpath("//a/text()").get(),
                date=datetime.today().strftime("%Y/%m/%d-%H:%M:%S"),
                site="YahooNews",
                url=topic.xpath("//a/@href").get(),
            )
