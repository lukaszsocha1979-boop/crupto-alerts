"""
Crypto Alerts
Config v1.0

W tym pliku NIE przechowujemy kluczy API.
Klucze będą pobierane z GitHub Secrets.

Autor: ChatGPT + Łukasz
"""

import os

# ===========================
# Telegram
# ===========================

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# ===========================
# API
# ===========================

BIRDEYE_API_KEY = os.getenv("BIRDEYE_API_KEY")
KUCOIN_API_KEY = os.getenv("KUCOIN_API_KEY")

# ===========================
# Monitorowane tokeny
# ===========================

TOKENS = [
    "ZEUS",
    "PYTH",
    "W",
    "JUP",
    "BOME",
    "MEW"
]

# ===========================
# BTC
# ===========================

BTC_SYMBOL = "BTC"

# ===========================
# Alerty
# ===========================

PRICE_ALERT_PERCENT = 11

VOLUME_ALERT_PERCENT = 100

CHECK_INTERVAL_MINUTES = 5

# ===========================
# Storage
# ===========================

STORAGE_FILE = "storage.json"

# ===========================
# Telegram
# ===========================

GREEN = "🟢"
BLUE = "🔵"
RED = "🔴"

# ===========================
# News
# ===========================

NEWS_TOKENS = [
    "BTC",
    "ZEUS",
    "PYTH",
    "W",
    "JUP",
    "BOME",
    "MEW"
]
