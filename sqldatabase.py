import sqlite3

conn = sqlite3.connect('behas.db')

cursor = conn.cursor()

cursor.execute("""CREATE TABLE cars (year TEXT, model TEXT, price TEXT, url TEXT PRIMARY KEY)""")

conn.commit()

conn.close()