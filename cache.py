def is_cache_fresh(last_fetched, now_ts, cache_seconds):
    """
    Returns True if cached data is still fresh, False otherwise.

    last_fetch_ts: int or None (last fetch timestamp)
    now_ts: int (current UTC timestamp)
    cache_seconds: int (freshness window)
    """

    if last_fetched is None:
        return False

    return (now_ts - last_fetched) < cache_seconds
