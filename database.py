import sqlite3

connection = sqlite3.connect("emotion.db")

cursor = connection.cursor()

cursor.execute("""

CREATE TABLE IF NOT EXISTS history(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    emotion TEXT,

    confidence REAL,

    date TEXT,

    time TEXT

)

""")

connection.commit()

connection.close()

print("Database Created Successfully")