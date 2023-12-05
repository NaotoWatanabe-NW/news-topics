# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import datetime
import os
import sqlite3


class NewsScrapyPipeline(object):
    _db = None

    @classmethod
    def get_database(cls):
        cls._db = sqlite3.connect(
            os.path.join(os.getcwd(), "yahoo_news_spider.db")
        )
        cursor = cls._db.cursor()
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS post(\
                id INTEGER PRIMARY KEY AUTOINCREMENT, \
                url TEXT UNIQUE NOT NULL, \
                title TEXT NOT NULL, \
                date DATE NOT NULL, \
                site TEXT NOT NULL, \
            );')
        return cls._db

    def process_item(self, item, spider):
        self.save_post(item)
        return item

    def save_post(self, item):
        if self.find_post(item["url"]):
            return
        db = self.get_database()
        db.execute(
            'INSERT INTO post (title, url, date, site) VALUES (?, ?, ?, ?)',
            (item["title"], item["url"], item["date"], item["site"]),
        )
        db.commit()

    def find_post(self, url):
        db = self.get_database()
        cursor = db.execute(
            "SELECT * FROM post WHERE url=?",
            (url,)
        )
        return cursor.fetchall()
