import sqlite3

db = sqlite3.connect("D:/scraping")
cursor = db.cursor()
cursor.execute('SELECT * FROM post')
print(cursor.fetchall())
