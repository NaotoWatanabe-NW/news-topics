from ..items import NewsScrapyItem
import scrapy
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class MinkabuNewsSpiderSpider(scrapy.Spider):
    name = "minkabu_news_spider"
    allowed_domains = ["minkabu.jp"]
    start_urls = [
        "https://minkabu.jp/news/search?category=all"
        "https://minkabu.jp/news/search?category=market",
        "https://minkabu.jp/news/search?category=stock",
        "https://minkabu.jp/news/search?category=fx",
        "https://minkabu.jp/news/search?category=worldmarket",
        "https://minkabu.jp/news/search?category=crypto",
        "https://minkabu.jp/news/search?category=product",
        "https://minkabu.jp/news/search?category=tatsujin",
        "https://minkabu.jp/news/search?category=column",
        ]
    site = "Minkabu"

    def parse(self, response):
        logger.info("Parse function called on %s", response.url)
        topics = response.xpath("/html/body/div/div[2]/div/div/div/div/div/div/div/ul/li/div/div[1]/div/a/@href").getall()
        # topics = response.xpath("/html/body/div/div[2]/div/div/div/div/div/div/div[3]/div/ul/li/a/@href").getall()
        for topic in topics:
            link = response.urljoin(topic)
            yield scrapy.Request(link, callback=self.parse_article)

    def parse_article(self, response):
        logger.info("Parse function called on %s", response.url)
        title = response.xpath("/html/body/div/div[2]/div/div/div[1]/div[1]/div/div/div[1]/div[1]/div[1]/h1/text()").get()
        article = "".join(response.xpath("/html/body/div/div[2]/div/div/div[1]/div[1]/div/div/div[1]/div[2]/text()").getall()).replace("\n", "").replace(" ", "")
        if article == "":
            article = "".join(response.xpath("/html/body/div/div[2]/div/div/div/div/div/div/div/div/p").getall()).replace("\n", "").replace(" ", "")
        date = datetime.today()
        url = response.request.url
        yield NewsScrapyItem(
            title=title,
            article=article,
            date=date,
            site=self.site,
            url=url,
        )
