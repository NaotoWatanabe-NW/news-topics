import scrapy
from ..items import NewsScrapyItem
from datetime import datetime


class YahooNewsSpiderSpider(scrapy.Spider):
    name = "yahoo_news_spider"
    allowed_domains = ["news.yahoo.co.jp"]
    start_urls = ["https://news.yahoo.co.jp"]
    site = "YahooNews"

    def parse(self, response):
        categories = response.xpath("/html/body/div/header/nav/div[@id='snavi']/ul[1]")
        for category in categories.xpath(".//li"):  # カテゴリごとに処理する
            link = category.xpath(".//a/@href").get()  # カテゴリのリンク
            link = response.urljoin(link)
            yield scrapy.Request(link, callback=self.topic_parse)

    def topic_parse(self, response):
        topics = response.xpath("/html/body/div/div/main/div/div/section/div/div/div/ul")
        if topics is None:  # lifeはデータをとらない
            yield
        for topic in topics.xpath(".//li"):  # トピックごとに処理
            url = topic.xpath(".//a/@href").get()  # トピックのリンク
            yield scrapy.Request(url=url, callback=self.body_parse)

    def body_parse(self, response):
        title = response.xpath("/html/body/div/div/main/div/div/article/header/h1/text()").get()  # yahoo以外
        if title is None:  # yahooニュース
            link = response.xpath("/html/body/div/div/main/div/div/article/div[2]/div/p/a/@href").get()
            yield scrapy.Request(url=link, callback=self.article_parse)
        article = response.xpath("/html/body/div/div/main/div/div/article/div/div/p/text()").get()
        date = datetime.today().strftime("%Y/%m/%d-%H:%M:%S")
        url = response.request.url
        yield NewsScrapyItem(
            title=title,
            article=article,
            date=date,
            site=self.site,
            url=url,
        )

    def article_parse(self, response):
        title = response.xpath("/html/body/div/div/main/div/div/article/header/h1/text()").get()
        article = response.xpath("/html/body/div/div/main/div/div/article/div/div/p/text()").get()
        date = datetime.today().strftime("%Y/%m/%d-%H:%M:%S")
        site = self.site
        url = response.request.url
        yield NewsScrapyItem(
            title=title,
            article=article,
            date=date,
            site=self.site,
            url=url,
        )
