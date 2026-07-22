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
            "disable_web_page_preview": True,
        },
        timeout=20,
    )


def human(value):

    if value is None:
        return "-"

    value = float(value)

    if value >= 1_000_000_000_000:
        return f"{value/1_000_000_000_000:.2f}T"

    if value >= 1_000_000_000:
        return f"{value/1_000_000:.2f}B"

    if value >= 1_000_000:
        return f"{value/1_000_000:.2f}M"

    if value >= 1_000:
        return f"{value/1_000:.2f}K"

    return f"{value:.2f}"


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

market_report = ["📊 RAPORT RYNKU", ""]

for symbol, token in TOKENS.items():

    print("Market:", symbol)

    data = get_token(token)

    if data is None:
        print(f"Brak danych dla {symbol}")
        continue

    history = market_cache.get(symbol, {})
    history.update(data)
    new_cache[symbol] = history

save_market(new_cache)

market_cache = load_market()

for symbol, data in market_cache.items():

    alert = check_alert(symbol, data)

    if alert:
        print(alert)
        send_telegram(alert)

for symbol, data in market_cache.items():

    if symbol == "BTC":

        market_report.extend([
            "🟠 BTC",
            f"💰 ${data['price']:,.2f}",
            f"🏦 MC: {human(data['market_cap'])}",
            f"📊 Vol: {human(data['volume24h'])}",
            ""
        ])

    else:

        market_report.extend([
            f"⚡ {symbol}",
            f"💰 ${data['price']:.8f}",
            f"🏦 MC: {human(data['market_cap'])}",
            f"📊 Vol: {human(data['volume24h'])}",
            f"💧 Liq: {human(data.get('liquidity'))}",
            ""
        ])

send_telegram("\n".join(market_report))

print("========== KONIEC ==========")
