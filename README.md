# Reddit Multi-Subreddit Scraper (Python)

A Python automation script that fetches posts from multiple subreddits using
Reddit’s public JSON API, supports pagination and rate limiting, and stores
results in a local SQLite database with caching and deduplication.

This project demonstrates how to build reliable API ingestion pipelines
similar to real-world automation and data collection workflows.

---

## 🚀 Features

- Fetches posts from multiple subreddits
- Cursor-based pagination using Reddit `after` tokens
- Rate-limit friendly requests with delay
- Defensive API error handling (timeouts, 429, bad responses)
- SQLite storage with duplicate prevention
- Caching to avoid unnecessary API calls
- Structured logging to file and console
- Modular project structure

---

## 🛠 Tech Stack

- Python
- Requests (HTTP client)
- SQLite (built-in database)

---

## 📁 Project Structure

```
reddit-fetcher/
│
├── main.py          # Pipeline orchestrator
├── reddit_fetch.py # Reddit API client + pagination
├── database.py     # SQLite storage layer
├── cache.py        # Cache freshness logic
├── config.py       # Configuration settings
├── logs/           # Runtime logs (ignored by git)
├── requirements.txt
└── README.md
```


## ⚙️ Setup & Run

### 1. Clone repository

```bash
git clone <repo-url>
cd Reddit_Subreddit_Scraper
```

### 2. Create virtual environment (optional but recommended)

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\Activate      # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Subreddits

Edit `config.py`:

```python
SUBREDDITS = ["manhwa", "memes"]
SORT = "hot"
LIMIT = 50
```

### 5. Run

```bash
python main.py
```
