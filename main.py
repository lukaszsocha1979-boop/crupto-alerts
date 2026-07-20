import requests
import feedparser

from config import KEYWORDS, HIGH_PRIORITY
from news_sources import RSS_FEEDS
from filters import is_interesting
from storage import already_sent, mark_sent

import os

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def send(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "text": text
        }
    )


for rss in RSS_FEEDS:

    try:
        feed = feedparser.parse(rss)

        for entry in feed.entries:

            title = entry.title
            link = entry.link

            if already_sent(link):
                continue

            if not is_interesting(title):
                continue

            title_lower = title.lower()

            token = None

            for name, words in KEYWORDS.items():
                for w in words:
                    if w in title_lower:
                        token = name
                        break
                if token:
                    break

            priority = "🟢 WYSOKA"

            for word in HIGH_PRIORITY:
                if word in title_lower:
                    priority = "🟢 WYSOKA"
                    break
            else:
                priority = "🔴 NISKA"

            msg = (
                f"{priority}\n\n"
                f"🪙 {token}\n\n"
                f"{title}\n\n"
                f"{link}"
            )

            send(msg)
            mark_sent(link)

    except Exception as e:
        print(e)
