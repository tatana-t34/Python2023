import sqlite3
import datetime

def create_table():
    with sqlite3.connect("news_db.db") as db:
        cursor = db.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS news(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    content TEXT,
    date TEXT, 
    url TEXT                                  
    );""")
    db.commit()

def insert_news(col1, col2, col3, col4):
    with sqlite3.connect("news_db.db") as db:
        cursor = db.cursor()
        data_list = (col1, col2, col3, col4)
        cursor.execute("""
                        INSERT INTO news (title, content, date, url)
                        VALUES (?, ?, ?, ?)
                            """, data_list)

        db.commit()

def check_news(title):
    with sqlite3.connect("news_db.db") as db:
        cursor = db.cursor()
        cursor.execute("""SELECT title FROM news WHERE title = ? """, (title,))
        result = cursor.fetchall()
        if len(result) == 0:
            return 0
        else:
            return 1
        
def get_data_from_db():
    with sqlite3.connect("news_db.db") as db:
        cursor = db.cursor()
        cursor.execute("""SELECT title, content, date, url FROM news""")
        data_set = cursor.fetchall()
        return data_set