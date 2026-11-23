
"""
Crypto Alerts
DEX Screener v1.0

Pobieranie cen sześciu tokenów Solana
jednym zapytaniem API.
"""

import requests

from tokens import TOKENS


BASE_URL = "https://api.dexscreener.com/tokens/v1/solana/"


def get_all_market_data():

    market = {}

    addresses = [
        token["mint"]
        for token in TOKENS.values()
        if token.get("mint")
    ]

    if not addresses:
        raise RuntimeError("Brak adresów tokenów")

    response = requests.get(
        BASE_URL + ",".join(addresses),
        timeout=30
    )

    print("=== DEX SCREENER ===")
    print("HTTP:", response.status_code)

    response.raise_for_status()

    pairs = response.json()

    print("Liczba znalezionych par:", len(pairs))

    for symbol, token in TOKENS.items():

        mint = token.get("mint")

        matching = [
            pair for pair in pairs
            if pair.get("chainId") == "solana"
            and pair.get("baseToken", {}).get("address") == mint
            and pair.get("priceUsd") is not None
        ]

        matching.sort(
            key=lambda pair: (
                pair.get("liquidity", {}).get("usd") or 0
            ),
            reverse=True
        )

        if not matching:
            print(f"❌ {symbol}: brak odpowiedniej pary")
            continue

        pair = matching[0]

        price = float(pair["priceUsd"])

        liquidity = (
            pair.get("liquidity", {}).get("usd") or 0
        )

        volume = (
            pair.get("volume", {}).get("h24")
        )

        market[symbol] = {
            "price": price,
            "price_change_24h": None,
            "volume_24h": volume,
            "market_cap": pair.get("marketCap"),
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

    print("====================")

    return market
