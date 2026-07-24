"""
Crypto Alerts
Main v1.0
"""

from market import get_market
from alerts import check_alerts
from telegram_sender import send_message


def main():
    """
    Główna funkcja programu.
    """

    print("🚀 Crypto Alerts start...")

    market = get_market()

    alerts = check_alerts(market)

    if alerts:
        send_message(alerts)
    else:
        print("ℹ️ Brak nowych alertów.")

    print("✅ Crypto Alerts zakończył działanie.")


if __name__ == "__main__":
    main()
