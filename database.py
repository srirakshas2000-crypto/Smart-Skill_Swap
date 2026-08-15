import sqlite3

conn = sqlite3.connect("skillswap.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(

id INTEGER PRIMARY KEY AUTOINCREMENT,

name TEXT,

regno TEXT,

email TEXT,

password TEXT,

teach TEXT,

learn TEXT

)
""")

conn.commit()

conn.close()

print("Database Created Successfully")