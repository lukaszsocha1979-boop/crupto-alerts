"""
Crypto Alerts
Telegram Sender v1.0
"""

import requests

from config import (
    TELEGRAM_BOT_TOKEN,
    TELEGRAM_CHAT_ID
)


def send_message(message: str) -> bool:
    """
    Wysyła wiadomość na Telegram.
    """

    if not TELEGRAM_BOT_TOKEN:
        print("❌ Brak TELEGRAM_BOT_TOKEN")
        return False

    if not TELEGRAM_CHAT_ID:
        print("❌ Brak TELEGRAM_CHAT_ID")
        return False

    url = (
        f"https://api.telegram.org/bot"
        f"{TELEGRAM_BOT_TOKEN}/sendMessage"
    )

    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }

    try:

        response = requests.post(
            url,
            json=payload,
            timeout=15
        )

        if response.status_code == 200:
            print("✅ Telegram OK")
            return True

        print(response.text)
        return False

    except Exception as e:
        print(e)
        return False


def send_test():
    """
    Test połączenia z Telegramem.
    """

    message = (
        "🟢 <b>Crypto Alerts</b>\n\n"
        "Połączenie z Telegram działa poprawnie ✅"
    )

    send_message(message)


if __name__ == "__main__":
    send_test()
