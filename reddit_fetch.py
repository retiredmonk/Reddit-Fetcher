import requests, time, logging

def fetch_posts(subreddit, config):
    after = None
    rows = []
    count = 1

    url = f"https://www.reddit.com/r/{subreddit}/{config.SORT}.json"

    headers = {
        "User-Agent": config.USER_AGENT,
    }

    while True:

        params = {
            "limit": config.LIMIT,
            "after": after,
        }

        try:
            response = requests.get(url, params=params,headers=headers, timeout=10)

            if response.status_code == 429:
                logging.error("Too many requests for r/%s at Page: %d", subreddit, count)
                break

            if response.status_code != 200:
                logging.error("Error fetching r/%s: Status Code - %d at Page: %d", subreddit, count, response.status_code)
                break

        except requests.exceptions.Timeout as e:

            logging.error("Time Out Error for r/%s: %s at page %d", subreddit, e, count)
            break

        except requests.exceptions.TooManyRedirects as e:
            logging.error("Too many Redirects for r/%s: %s at page %d", subreddit, e, count)
            break

        except requests.exceptions.RequestException as e:
            logging.error("Request Exception for r/%s: %s at page %d", subreddit, e, count)
            break

        try:
            data = response.json()["data"]
            children = data["children"]
            after = data["after"]

        except ValueError as e:
            logging.error("Bad JSON for r/%s: %s at page %d", subreddit, e, count)
            break

        except KeyError as e:
            logging.error("Bad JSON for r/%s: %s at page %d", subreddit, e, count)
            break

        if len(children) == 0:
            break

        for child in children:
            post = child["data"]
            rows.append((
                post["title"],
                post["score"],
                post["author"],
                post["url"],
                post["created_utc"]
            ))

        if after is None:
            break

        time.sleep(config.SLEEP_TIME)

        count += 1

    return rows

