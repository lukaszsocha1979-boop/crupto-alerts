import os
import requests
import feedparser

from config import KEYWORDS, HIGH_PRIORITY
from news_sources import RSS_FEEDS
from filters import is_interesting
from storage import already_sent, mark_sent
from translator import translate

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def send(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "text": text,
            "disable_web_page_preview": True
        }
    )


for rss in RSS_FEEDS:

    try:
        feed = feedparser.parse(rss)

        for entry in feed.entries:

            title_original = entry.title
            title = translate(title_original)

            link = entry.link

            if already_sent(link):
                continue

            if not is_interesting(title_original):
                continue

            title_lower = title_original.lower()

            token = "CRYPTO"

            for name, words in KEYWORDS.items():
                if any(word.lower() in title_lower for word in words):
                    token = name
                    break

            priority = "🔴 NISKA"

            for word in HIGH_PRIORITY:
                if word.lower() in title_lower:
                    priority = "🟢 WYSOKA"
                    break

            message = (
                f"{priority}\n\n"
                f"🪙 {token}\n\n"
                f"{title}\n\n"
                f"🔗 {link}"
            )

            send(message)
            mark_sent(link)

    except Exception as e:
        print(f"Błąd RSS: {rss}")
        print(e)
