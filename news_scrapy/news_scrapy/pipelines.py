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

    @classmethod
    def get_database(cls):
        cls._client = NewsClient()
        return cls._client

    def process_item(self, item, spider):
        self.save_post(item)
        return item

    def save_post(self, item):
        if self.find_post(item["url"]):
            return
        db = self.get_database()
        db.add(item)

    def find_post(self, url):
        post = self._client.collection.find_one({"url": url})
        if post is None:
            return True
        else:
            return False


class NewsClient:
    client = None
    db = None
    collection = None

    def __init__(self):
        self.client = MongoClient("mongodb+srv://NaotoWatanabe:jack0719@cluster0.dr5vnlh.mongodb.net/?retryWrites"
                                  "=true&w=majority")
        self.db = self.client["Cluster0"]
        self.collection = self.db["NewsStorage"]

    def add(self, item):
        item["date"] = datetime.now()
        self.collection.insert_one(item)


