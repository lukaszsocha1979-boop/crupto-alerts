
"""
Crypto Alerts
DEX Screener v1.1

Pobieranie cen sześciu tokenów Solana
jednym zapytaniem API.
"""

import requests

from tokens import TOKENS


BASE_URL = "https://api.dexscreener.com/tokens/v1/solana/"


def _to_float(value, default=None):
    """Bezpieczna konwersja wartości na float."""

    try:
        if value is None:
            return default

        result = float(value)

        if result != result or result in (float("inf"), float("-inf")):
            return default

        return result

    except (TypeError, ValueError):
        return default


def get_all_market_data():

    market = {}

    addresses = [
        token["mint"]
        for token in TOKENS.values()
        if token.get("mint")
    ]

    if not addresses:
        raise RuntimeError("Brak adresów tokenów")

    print("=== DEX SCREENER ===")
    print("Liczba monitorowanych tokenów:", len(addresses))

    response = requests.get(
        BASE_URL + ",".join(addresses),
        timeout=30
    )

    print("HTTP:", response.status_code)

    response.raise_for_status()

    pairs = response.json()

    if not isinstance(pairs, list):
        raise RuntimeError(
            "DEX Screener zwrócił nieprawidłowy format danych"
        )

    print("Liczba znalezionych par:", len(pairs))

    for symbol, token in TOKENS.items():

        mint = token.get("mint")

        if not mint:
            print(f"⚠️ {symbol}: brak adresu mint")
            continue

        matching = []

        for pair in pairs:

            if not isinstance(pair, dict):
                continue

            base_token = pair.get("baseToken")

            if not isinstance(base_token, dict):
                continue

            if pair.get("chainId") != "solana":
                continue

            if base_token.get("address") != mint:
                continue

            price = _to_float(pair.get("priceUsd"))

            if price is None or price <= 0:
                continue

            liquidity_data = pair.get("liquidity")

            if not isinstance(liquidity_data, dict):
                liquidity_data = {}

            liquidity = _to_float(
                liquidity_data.get("usd"),
                0
            )

            matching.append({
                "pair": pair,
                "price": price,
                "liquidity": liquidity
            })

        matching.sort(
            key=lambda item: item["liquidity"],
            reverse=True
        )

        if not matching:
            print(f"❌ {symbol}: brak prawidłowej pary")
            continue

        selected = matching[0]

        pair = selected["pair"]
        price = selected["price"]
        liquidity = selected["liquidity"]

        volume_data = pair.get("volume")

        if isinstance(volume_data, dict):
            volume = _to_float(volume_data.get("h24"))
        else:
            volume = None

        market_cap = _to_float(pair.get("marketCap"))

        market[symbol] = {
            "price": price,
            "price_change_24h": None,
            "volume_24h": volume,
            "market_cap": market_cap,
            "liquidity": liquidity,
            "dex": pair.get("dexId"),
            "pair_address": pair.get("pairAddress")
        }

        print(
            f"✅ {symbol}: "
            f"${price} | "
            f"Płynność: ${liquidity} | "
            f"DEX: {pair.get('dexId')}"
        )

    print("Pobrano dane dla tokenów:", len(market))
    print("====================")

    return market
