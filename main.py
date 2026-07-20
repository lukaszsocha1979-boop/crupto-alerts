import os
import requests

from news_sources import get_news
from filters import analyze
from storage import already_sent, mark_sent

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def send(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "text": message
        }
    )


news = get_news()
alerts = analyze(news)

count = 0
MAX_ALERTS = 10

for alert in alerts:

    if already_sent(alert["link"]):
        continue

    text = (
        f"{alert['level']}\n\n"
        f"📌 {alert['project']}\n\n"
        f"{alert['title']}\n\n"
        f"🔗 {alert['link']}"
    )

    send(text)

    mark_sent(alert["link"])

    count += 1

    if count >= MAX_ALERTS:
        break

print(f"Wysłano {count} nowych alertów.")
