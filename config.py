
"""
Crypto Alerts
Config v1.3

Konfiguracja alertów i DEX Screener.
"""

import os

# Telegram
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Progi alertów cenowych
NEXT_PRICE_ALERT_STEP = 6

# Kolejne progi:
# 9%, 18%, 24%, 30%, 36%, 42%...
PRICE_ALERT_LEVELS = [9, 18, 24, 30]

# Alert wolumenu
VOLUME_ALERT_PERCENT = 100

# Preferowana częstotliwość kontroli
CHECK_INTERVAL_MINUTES = 5

# Plik historii i poziomów alertów
STORAGE_FILE = "storage.json"

# Emoji Telegram
GREEN = "🟢"
BLUE = "🔵"
RED = "🔴"

# Tokeny do wiadomości
NEWS_TOKENS = [
    "BTC",
    "ZEUS",
    "PYTH",
    "W",
    "JUP",
    "SKR",
    "MEW"
]
