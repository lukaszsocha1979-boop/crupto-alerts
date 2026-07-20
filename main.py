import os
import feedparser
import requests

from news_sources import RSS_FEEDS
from filters import is_interesting, get_priority
from storage import already_sent, save_sent
from translator import translate


def send_telegram(message):
    url = f"https://api.telegram.org/bot{os.environ['TELEGRAM_BOT_TOKEN']}/sendMessage"

    response = requests.post(
        url,
        data={
            "chat_id": os.environ["TELEGRAM_CHAT_ID"],
            "text": message,
            "disable_web_page_preview": False,
        },
        timeout=20,
    )

    print(response.text)


print("=== Start monitora ===")

for feed_url in RSS_FEEDS:

    print(f"\nSprawdzam: {feed_url}")

    feed = feedparser.parse(feed_url)

    for entry in feed.entries:

        title = entry.title
        link = entry.link

        if already_sent(link):
            continue

        if not is_interesting(title):
            continue

        priority, score = get_priority(title)

        # Pomiń mało ważne wiadomości
        if score < 4:
            continue

        translated = translate(title)

        message = (
            f"{priority} ({score}/10)\n\n"
            f"📰 {translated}\n\n"
            f"🔗 {link}"
        )

        print(f"Wysyłam: {translated}")

        send_telegram(message)

        save_sent(link)

print("\n=== Koniec monitora ===")
