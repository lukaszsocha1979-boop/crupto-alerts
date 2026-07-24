"""
Crypto Alerts
Config v1.1

W tym pliku NIE przechowujemy kluczy API.
Klucze pobierane są z GitHub Secrets.
"""

import os

# ==================================================
# Telegram
# ==================================================

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# ==================================================
# API
# ==================================================

BIRDEYE_API_KEY = os.getenv("BIRDEYE_API_KEY")

# ==================================================
# Bitcoin
# ==================================================

BTC_SYMBOL = "BTC"

# ==================================================
# Alerty
# ==================================================

FIRST_PRICE_ALERT = 11
NEXT_PRICE_ALERT_STEP = 10
VOLUME_ALERT_PERCENT = 100

# Co ile minut uruchamia się GitHub Actions
CHECK_INTERVAL_MINUTES = 5

# ==================================================
# Storage
# ==================================================

STORAGE_FILE = "storage.json"

# ==================================================
# Telegram Emojis
# ==================================================

GREEN = "🟢"
BLUE = "🔵"
RED = "🔴"

# ==================================================
# News
# ==================================================

NEWS_TOKENS = [
    "BTC",
    "ZEUS",
    "PYTH",
    "W",
    "JUP",
    "BOME",
    "MEW"
]
