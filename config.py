
"""
Crypto Alerts
Config v1.2

Konfiguracja alertów i DEX Screener.
"""

import os

# Telegram
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Birdeye – pozostawiamy tymczasowo, ale nie używamy do cen
BIRDEYE_API_KEY = os.getenv("BIRDEYE_API_KEY")

# Bitcoin
BTC_SYMBOL = "BTC"

# Progi alertów cenowych
FIRST_PRICE_ALERT = 9
NEXT_PRICE_ALERT_STEP = 6

# Kolejne progi: 9%, 18%, 24%, 30%, 36%, 42%...
PRICE_ALERT_LEVELS = [9, 18, 24, 30]

# Alert wolumenu
VOLUME_ALERT_PERCENT = 100

# Kontrola co 5 minut
CHECK_INTERVAL_MINUTES = 5

# Historia cen
STORAGE_FILE = "storage.json"

# Telegram Emojis
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
