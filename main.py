"""
Crypto Alerts
Main v1.1
"""

from market import get_market
from alerts import check_alerts
from telegram_sender import send_message


def main():
    print("🚀 Crypto Alerts start...")

    market = get_market()

    # Test Telegrama (usuń tę linię po potwierdzeniu działania)
    send_message("✅ Crypto Alerts działa!")

    alerts = check_alerts(market)

    if alerts:
        send_message(alerts)

    print("✅ Crypto Alerts zakończył działanie.")


if __name__ == "__main__":
    main()
