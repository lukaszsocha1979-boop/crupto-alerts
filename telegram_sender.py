"""
Crypto Alerts
Telegram Sender v1.2
"""

import requests

from config import (
    TELEGRAM_BOT_TOKEN,
    TELEGRAM_CHAT_ID
)


def send_message(message: str) -> bool:
    """
    Wysyła wiadomość na Telegram i wymaga potwierdzenia ok=true
    zwróconego przez Telegram Bot API.
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
        "text": str(message),
        "parse_mode": "HTML"
    }

    try:
        response = requests.post(
            url,
            json=payload,
            timeout=15
        )
    except requests.exceptions.RequestException as e:
        # Nie wypisujemy treści wyjątku: URL żądania zawiera token bota.
        print(f"❌ Telegram error: {type(e).__name__}")
        return False

    if response.status_code != 200:
        print(f"❌ Telegram HTTP error: {response.status_code}")
        return False

    try:
        result = response.json()
    except ValueError:
        print("❌ Telegram zwrócił nieprawidłowy JSON.")
        return False

    if not isinstance(result, dict) or result.get("ok") is not True:
        print("❌ Telegram API nie potwierdziło wysłania (ok != true).")
        return False

    print("✅ Telegram OK (HTTP 200, API ok=true)")
    return True


def send_test():
    """
    Test połączenia z Telegramem.
    """

    message = (
        "🟢 <b>Crypto Alerts</b>\\n\\n"
        "Połączenie z Telegram działa poprawnie ✅"
    )

    return send_message(message)


if __name__ == "__main__":
    send_test()
