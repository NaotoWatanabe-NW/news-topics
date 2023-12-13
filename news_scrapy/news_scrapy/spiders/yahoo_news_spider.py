import scrapy
from ..items import NewsScrapyItem
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class YahooNewsSpiderSpider(scrapy.Spider):
    name = "yahoo_news_spider"
    allowed_domains = ["news.yahoo.co.jp"]
    start_urls = ["https://news.yahoo.co.jp"]
    site = "YahooNews"

    def parse(self, response):
        logger.info("Parse function called on %s", response.url)
        categories = response.xpath("/html/body/div/header/nav/div[@id='snavi']/ul[1]/li/a/@href").getall()
        for category in categories:  # カテゴリごとに処理する
            if category == "/categories/life":
                continue
            link = response.urljoin(category)
            yield scrapy.Request(link, callback=self.topic_parse)

    def topic_parse(self, response):
        logger.info("Parse function called on %s", response.url)
        topics = response.xpath("/html/body/div/div/main/div/div/section/div/div/div/ul/li/a/@href").getall()  # topicのリンク
        for topic in topics:  # トピックごとに処理
            yield scrapy.Request(url=topic, callback=self.body_parse)

    def body_parse(self, response):
        logger.info("Parse function called on %s", response.url)
        title = response.xpath("/html/body/div/div/main/div/div/article/header/h1/text()").get()  # yahoo以外
        if title is None:  # yahooニュース
            link = response.xpath("/html/body/div/div/main/div/div/article/div[2]/div/p/a/@href").get()
            yield scrapy.Request(url=link, callback=self.body_parse)
        else:
            article = "".join(response.xpath("/html/body/div/div/main/div/div/article/div/div/p/text()").getall()).replace("\n", "").replace(" ", "")
            date = datetime.today()
            url = response.request.url
            yield NewsScrapyItem(
                title=title,
                article=article,
                date=date,
                site=self.site,
                url=url,
            )
