import json
import os

NEWS_FILE = "sent_links.json"
MARKET_FILE = "market_cache.json"


def already_sent(link):

    if not os.path.exists(NEWS_FILE):
        return False

    with open(NEWS_FILE, "r") as f:
        data = json.load(f)

    return link in data


def save_sent(link):

    if os.path.exists(NEWS_FILE):

        with open(NEWS_FILE, "r") as f:
            data = json.load(f)

    else:

        data = []

    data.append(link)

    with open(NEWS_FILE, "w") as f:
        json.dump(data, f)


def load_market():

    if not os.path.exists(MARKET_FILE):
        return {}

    with open(MARKET_FILE, "r") as f:
        return json.load(f)


def save_market(data):

    with open(MARKET_FILE, "w") as f:
        json.dump(data, f)
