import logging
from datetime import datetime, timezone

import config
from config import SUBREDDITS, CACHE_SECONDS
from database import *
from cache import is_cache_fresh
from reddit_fetch import fetch_posts

def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Clear existing handlers
    if logger.hasHandlers():
        logger.handlers.clear()

    file_handler = logging.FileHandler(config.LOG_PATH)
    stream_handler = logging.StreamHandler()

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

def main():
    setup_logging()

    connection, cursor = init_db()
    logging.info("Database setup complete")

    for subreddit in SUBREDDITS:
        logging.info("Starting subreddit r/%s", subreddit)

        last_fetched = get_last_fetch_time(connection,cursor,subreddit)
        now_ts = int(datetime.now(timezone.utc).timestamp())

        if is_cache_fresh(last_fetched, now_ts, CACHE_SECONDS):
            logging.info("Cache fresh, skipping %s", subreddit)
            continue

        rows = fetch_posts(subreddit, config)
        logging.info("Found %d posts in r/%s", len(rows), subreddit)

        if rows:
            insert_posts(connection, cursor, rows)
            logging.info("Saved %d posts in r/%s", len(rows), subreddit)
        else:
            logging.warning("No posts found, skipping %s", subreddit)

        update_last_fetch_time(connection, cursor, subreddit, now_ts)
        logging.info("Update cache timestamp for r/%s", subreddit)


    cursor.close()
    connection.close()
    logging.info("Reddit Fetcher complete")


if __name__ == "__main__":
    main()