import os
import feedparser
import requests

from news_sources import RSS_FEEDS
from filters import is_interesting, get_priority
from translator import translate

from storage import (
    already_sent,
    save_sent,
    load_market,
    save_market,
)

from market import get_token
from tokens import TOKENS
from alerts import check_alert


def send_telegram(message):

    url = f"https://api.telegram.org/bot{os.environ['TELEGRAM_BOT_TOKEN']}/sendMessage"

    requests.post(
        url,
        data={
            "chat_id": os.environ["TELEGRAM_CHAT_ID"],
            "text": message,
            "disable_web_page_preview": False,
        },
        timeout=20,
    )


print("========== START ==========")

####################################################
# RSS
####################################################

for feed_url in RSS_FEEDS:

    print("RSS:", feed_url)

    feed = feedparser.parse(feed_url)

    for entry in feed.entries:

        title = entry.title
        link = entry.link

        if already_sent(link):
            continue

        if not is_interesting(title):
            continue

        priority, score = get_priority(title)

        if score < 4:
            continue

        translated = translate(title)

        message = (
            f"{priority} ({score}/10)\n\n"
            f"📰 {translated}\n\n"
            f"🔗 {link}"
        )

        print("NEWS:", translated)

        send_telegram(message)

        save_sent(link)

####################################################
# MARKET
####################################################

market_cache = load_market()

new_cache = {}

for symbol, address in TOKENS.items():

    print("Market:", symbol)

    data = get_token(address)

    if data is None:
        continue

    old = market_cache.get(symbol)

    alert = check_alert(symbol, old, data)

    if alert:
        print(alert)
        send_telegram(alert)

    new_cache[symbol] = data

save_market(new_cache)
from market import get_token

print("===== MARKET =====")

try:
    btc = get_token({"type": "coingecko", "id": "bitcoin"})
    print("BTC:", btc)
except Exception as e:
    print("Błąd BTC:", e)

print("==================")
print("========== KONIEC ==========")
