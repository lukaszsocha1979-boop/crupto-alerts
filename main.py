import os
import requests

from news_sources import get_news
from filters import analyze

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def send(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "text": msg
        }
    )


news = get_news()

alerts = analyze(news)

if not alerts:
    print("Brak nowych alertów.")
else:

    for a in alerts:

        message = (
            f"{a['level']}\n\n"
            f"{a['project']}\n\n"
            f"{a['title']}\n\n"
            f"{a['link']}"
        )

        send(message)

        print(message)
