"""
Crypto Alerts
Main - Debug
"""

import os

print("=" * 40)
print("CRYPTO ALERTS - DEBUG")
print("=" * 40)

print("BIRDEYE_API_KEY :", "OK" if os.getenv("BIRDEYE_API_KEY") else "BRAK")
print("TELEGRAM_BOT_TOKEN :", "OK" if os.getenv("TELEGRAM_BOT_TOKEN") else "BRAK")
print("TELEGRAM_CHAT_ID :", "OK" if os.getenv("TELEGRAM_CHAT_ID") else "BRAK")

print("=" * 40)

if os.getenv("BIRDEYE_API_KEY"):
    print("✅ GitHub przekazuje BIRDEYE_API_KEY")
else:
    print("❌ GitHub NIE przekazuje BIRDEYE_API_KEY")
