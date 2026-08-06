"""
Crypto Alerts
Main v1.2
"""

from market import get_market
from alerts import check_alerts
from news import get_news
from telegram_sender import send_message


def main():
    """
    Główna funkcja programu.
    """

    try:

        print("🚀 Crypto Alerts start...")

        market = get_market()

        messages = []

        alerts = check_alerts(market)
        if alerts:
            messages.append(alerts)

        news = get_news()
        if news:
            if isinstance(news, list):
                messages.extend(news)
            else:
                messages.append(news)

        if messages:
            send_message("\n\n".join(messages))
        else:
            print("ℹ️ Brak nowych alertów.")

        print("✅ Crypto Alerts zakończył działanie.")

    except Exception as e:
        print(f"❌ Błąd: {type(e).__name__}: {e}")
        raise


if __name__ == "__main__":
    main()
