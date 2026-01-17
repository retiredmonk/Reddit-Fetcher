import sqlite3
from config import DB_PATH

def init_db():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            title TEXT,
            upvotes INTEGER,
            author TEXT,
            url TEXT unique,
            created_utc INTEGER
    )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subreddits_fetch (
            subreddit TEXT PRIMARY KEY,
            last_fetched INTEGER
            )
        """)

    connection.commit()

    return connection, cursor

def insert_posts(connection, cursor, rows):

    sql = """
    INSERT or IGNORE INTO posts (title, upvotes, author, url, created_utc)
    VALUES (?, ?, ?, ?, ?)
    """

    cursor.executemany(sql, rows)
    connection.commit()


def get_last_fetch_time (connection, cursor, subreddit):
    cursor.execute(
        "SELECT last_fetched FROM subreddits_fetch WHERE subreddit = ?",
        (subreddit,)
    )

    row = cursor.fetchone()
    return row[0] if row else None


def update_last_fetch_time (connection, cursor, subreddit, now_ts):
    cursor.execute("""
        INSERT INTO subreddits_fetch (subreddit, last_fetched) VALUES (?, ?)
        ON CONFLICT (subreddit)
        DO UPDATE SET last_fetched = excluded.last_fetched
    """, (subreddit, now_ts))

    connection.commit()

