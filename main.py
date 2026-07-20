import feedparser
import requests

from news_sources import RSS_FEEDS
from filters import is_interesting, get_priority
from storage import already_sent, save_sent
from translator import translate


def send_telegram(message):
    url = f"https://api.telegram.org/bot{__import__('os').environ['TELEGRAM_BOT_TOKEN']}/sendMessage"

    requests.post(
        url,
        data={
            "chat_id": __import__("os").environ["TELEGRAM_CHAT_ID"],
            "text": message,
            "disable_web_page_preview": False,
        },
        timeout=20,
    )


for feed_url in RSS_FEEDS:

    feed = feedparser.parse(feed_url)

    for entry in feed.entries:

        title = entry.title
        link = entry.link

        if already_sent(link):
            continue

        if not is_interesting(title):
            continue

        translated = translate(title)

        priority, score = get_priority(title)

        message = (
            f"{priority} ({score}/10)\n\n"
            f"📰 {translated}\n\n"
            f"🔗 {link}"
        )

        send_telegram(message)
        save_sent(link)
