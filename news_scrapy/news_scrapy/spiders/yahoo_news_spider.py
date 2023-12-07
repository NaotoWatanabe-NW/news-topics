import scrapy
from ..items import NewsScrapyItem
from datetime import datetime


class YahooNewsSpiderSpider(scrapy.Spider):
    name = "yahoo_news_spider"
    allowed_domains = ["news.yahoo.co.jp"]
    start_urls = ["https://news.yahoo.co.jp"]
    temp_url = None
    category = None

    def parse(self, response):
        categories = response.xpath("/html/body/div/header/nav/div[@id='snavi']/ul[1]")
        for category in categories.xpath(".//li"):  # カテゴリごとに処理する
            self.category = category.xpath(".//a/text()").get()
            link = category.xpath(".//a/@href").get()  # カテゴリのリンク
            link = response.urljoin(link)
            yield scrapy.Request(link, callback=self.topic_parse)

    def topic_parse(self, response):
        topics = response.xpath("/html/body/div/div/main/div/div/section/div/div/div/ul")
        for topic in topics.xpath(".//li"):  # トピックごとに処理
            url = topic.xpath(".//a/@href").get()  # トピックのリンク
            self.temp_url = url  # リンクを保存しておく
            yield scrapy.Request(url=url, callback=self.body_parse)

    def body_parse(self, response):
        title = response.xpath("/html/body/div/div/main/div/div/article/header/h1/text()").get()  # yahoo以外
        if title is None:  # yahooニュース
            url = response.xpath("/html/body/div/div/main]/div/div/article/div/div/p/a/@href").get()
            self.temp_url = url
            yield scrapy.Request(url=url, callback=self.body_parse)
            title = response.xpath("/html/body/div/div/main/div/div/article/div/span/a/p/text()").get()
        article = response.xpath("/html/body/div/div/main/div/div/article/div/div/p/text()").get()
        date = datetime.today().strftime("%Y/%m/%d-%H:%M:%S")
        yield NewsScrapyItem(
            title=title,
            category=self.category,
            article=article,
            date=date,
            site="YahooNews",
            url=self.temp_url,
        )
