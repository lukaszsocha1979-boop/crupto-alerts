"""
Crypto Alerts
Market v1.1
"""

import time

from tokens import TOKENS
from birdeye import get_market_data


def get_market():

    market = {}

    for symbol, token in TOKENS.items():

        mint = token.get("mint")

        if not mint:
            print(f"⚠️ Brak mint dla {symbol}")
            continue

        try:

            market[symbol] = get_market_data(mint)

            print(f"✅ {symbol} OK")

            # Krótka przerwa, aby nie przekroczyć limitu API Birdeye
            time.sleep(1)

        except Exception as e:

            print(f"❌ {symbol}: {e}")

    return market


def get_token(symbol: str):

    token = TOKENS.get(symbol)

    if token is None:
        return None

    mint = token.get("mint")

    if not mint:
        return None

    return get_market_data(mint)
