"""
Crypto Alerts
Market v1.0
"""

from tokens import TOKENS
from birdeye import get_market_data


def get_market():
    """
    Pobiera dane wszystkich monitorowanych tokenów.
    """

    market = {}

    for symbol, token in TOKENS.items():

        mint = token.get("mint")

        if not mint:
            print(f"⚠️ Brak mint dla {symbol}")
            continue

        try:

            market[symbol] = get_market_data(mint)

            print(f"✅ {symbol} OK")

        except Exception as e:

            print(f"❌ {symbol}: {e}")

    return market


def get_token(symbol: str):
    """
    Pobiera dane jednego tokena.
    """

    token = TOKENS.get(symbol)

    if token is None:
        return None

    mint = token.get("mint")

    if not mint:
        return None

    return get_market_data(mint)


if __name__ == "__main__":

    data = get_market()

    for symbol, info in data.items():

        print(
            symbol,
            info["price"],
            info["price_change_24h"],
            info["volume_24h"]
        )
