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
        self._client.add(item)
        return item


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
