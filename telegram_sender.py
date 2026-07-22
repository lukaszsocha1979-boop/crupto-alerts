"""
Crypto Alerts
Telegram Sender v1.1
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

    message = str(message)

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

        response.raise_for_status()

        print("✅ Telegram OK")
        return True

    except requests.exceptions.RequestException as e:
        print(f"❌ Telegram error: {e}")
        return False

    except Exception as e:
        print(f"❌ Nieoczekiwany błąd: {e}")
        return False


def send_test():
    """
    Test połączenia z Telegramem.
    """

    message = (
        "🟢 <b>Crypto Alerts</b>\n\n"
        "Połączenie z Telegram działa poprawnie ✅"
    )

    return send_message(message)


if __name__ == "__main__":
    send_test()
