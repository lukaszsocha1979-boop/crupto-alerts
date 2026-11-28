"""
Crypto Alerts
Main v1.3
"""

import math

from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
from tokens import TOKENS
from market import get_market
from alerts import check_alerts
from news import get_news
from telegram_sender import send_message
from storage import save_storage


def validate_market(market):
    """Nie pozwala zapisać pustego lub niekompletnego odczytu rynku."""
    if not isinstance(market, dict) or not market:
        raise RuntimeError("DEX Screener nie zwrócił danych rynkowych.")

    missing = sorted(set(TOKENS) - set(market))
    if missing:
        raise RuntimeError(
            "Brak danych dla monitorowanych tokenów: " + ", ".join(missing)
        )

    for symbol in TOKENS:
        data = market[symbol]
        try:
            price = float(data.get("price"))
        except (AttributeError, TypeError, ValueError):
            raise RuntimeError(f"{symbol}: brak prawidłowej ceny.")

        if not math.isfinite(price) or price <= 0:
            raise RuntimeError(f"{symbol}: cena musi być dodatnia i skończona.")


def main():
    try:
        print("🚀 Crypto Alerts start...")

        if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
            raise RuntimeError(
                "Brak TELEGRAM_BOT_TOKEN lub TELEGRAM_CHAT_ID w GitHub Secrets."
            )

        market = get_market()
        validate_market(market)

        messages = []
        alerts, pending_storage = check_alerts(market, persist=False)
        if alerts:
            messages.append(alerts)

        news = get_news()
        if news:
            if isinstance(news, list):
                messages.extend(news)
            else:
                messages.append(news)

        if messages:
            sent = send_message("\n\n".join(messages))
            if not sent:
                raise RuntimeError("Nie udało się wysłać alertu na Telegram.")
        else:
            print("ℹ️ Brak nowych alertów.")

        # Zapisujemy historię i progi dopiero po potwierdzonej wysyłce
        # albo po przebiegu bez alertów. Błąd Telegrama nie zużywa progu.
        save_storage(pending_storage)

        print("✅ Crypto Alerts zakończył działanie.")

    except Exception as e:
        print(f"❌ Błąd: {type(e).__name__}: {e}")
        raise


if __name__ == "__main__":
    main()
