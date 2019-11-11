import sqlite3
conn = sqlite3.connect('data/sqlite3/sqlite3');
conn.execute('DROP TABLE IF EXISTS url')
# CREATE文を記載する。
conn.execute('CREATE TABLE url(id INTEGER AUTO_INCREMENT, url TEXT, docs TEXT)')
conn.close()
