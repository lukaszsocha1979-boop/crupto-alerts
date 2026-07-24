"""
Crypto Alerts
Main v1.0
"""

from market import get_market
from alerts import check_alerts
from telegram_sender import send_message


def main():

    market = get_market()

    alerts = check_alerts(market)

    if alerts:
        send_message(alerts)


if __name__ == "__main__":
    main()
