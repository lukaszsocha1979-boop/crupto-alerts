
"""
Crypto Alerts
Market v1.4

Pobieranie cen przez DEX Screener.
Jedno zbiorcze zapytanie dla wszystkich tokenów.
"""

from tokens import TOKENS
from dex_screener import get_all_market_data


def get_market():
    return get_all_market_data()


def get_token(symbol: str):

    if symbol not in TOKENS:
        return None

    market = get_all_market_data()

    return market.get(symbol)
