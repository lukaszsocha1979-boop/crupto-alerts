import json
import os
from datetime import datetime, timedelta

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
        json.dump(data, f, indent=2)


def load_market():
    if not os.path.exists(MARKET_FILE):
        return {}

    with open(MARKET_FILE, "r") as f:
        return json.load(f)


def save_market(history):

    now = datetime.utcnow().isoformat()

    for symbol, values in history.items():

        if "history" not in values:
            values["history"] = []

        values["history"].append({
            "time": now,
            "price": values.get("price"),
            "market_cap": values.get("market_cap"),
            "volume24h": values.get("volume24h"),
            "liquidity": values.get("liquidity"),
            "buys24h": values.get("buys24h"),
            "sells24h": values.get("sells24h"),
        })

        cutoff = datetime.utcnow() - timedelta(hours=4)

        values["history"] = [
            h for h in values["history"]
            if datetime.fromisoformat(h["time"]) >= cutoff
        ]

    with open(MARKET_FILE, "w") as f:
        json.dump(history, f, indent=2)
