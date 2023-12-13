# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from datetime import datetime
import os
import sqlite3
from pymongo.mongo_client import MongoClient


class NewsScrapyPipeline(object):
    _client = None

    def open_spider(self, spider):
        self._client = NewsClient()

    def close_spider(self, spider):
        self._client.close()

    def process_item(self, item, spider):
        self.save_post(item)
        return item

    def save_post(self, item):
        if self.find_post(item["url"]) is False:
            self._client.add(item)

    def find_post(self, url):
        post = self._client.collection.find_one({"url": url})
        return post is None


class NewsClient:
    def __init__(self):
        self.client = MongoClient("mongodb+srv://NaotoWatanabe:jack0719@cluster0.dr5vnlh.mongodb.net/?retryWrites"
                                  "=true&w=majority")
        self.db = self.client["NewsStorage"]
        d = datetime.today().strftime("%Y-%m")
        self.collection = self.db[f"{d}"]

    def add(self, item):
        self.collection.insert_one(item)

    def close(self):
        self.client.close()
