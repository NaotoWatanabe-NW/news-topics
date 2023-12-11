from ..items import NewsScrapyItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from datetime import datetime


class MinkabuNewsSpiderSpider(CrawlSpider):
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
        "https://minkabu.jp/news/search?category=yutai",
                  ]
    site = "Minkabu"
    rules = (
        Rule(LinkExtractor(allow=r"/news/*"), callback="parse_article"),
    )

    def parse_article(self, response):
        item = NewsScrapyItem()
        item["title"] = response.xpath("/html/body/div/div[2]/div/div/div[1]/div[1]/div/div/div[1]/div[1]/div[1]/h1/text()")
        item["article"] = response.xpath("/html/body/div/div[2]/div/div/div[1]/div[1]/div/div/div[1]/div[2]")
        item["date"] = datetime.today().strftime("%Y/%m/%d-%H:%M:%S")
        item["site"] = self.site
        item["url"] = response.request.url
        return item
