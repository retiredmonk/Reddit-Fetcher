from pathlib import Path

DB_PATH = Path("reddit_fetches.db")
LOG_PATH = Path("logs/reddit_fetches.log")
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
SUBREDDITS = ["manhwa", "memes"]
SORT = "hot"
CACHE_SECONDS = 15 * 60
LIMIT = 50
SLEEP_TIME = 1.5
USER_AGENT = "myredditfetcher/1.0"  