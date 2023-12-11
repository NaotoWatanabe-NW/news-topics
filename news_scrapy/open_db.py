import sqlite3

db = sqlite3.connect("yahoo_news_spider.sqlite")
cursor = db.cursor()
cursor.execute('SELECT * FROM post;')
print(cursor.fetchall())
