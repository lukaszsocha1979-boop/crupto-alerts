"""
Crypto Alerts
Birdeye API v1.0
"""

import requests

from config import BIRDEYE_API_KEY

BASE_URL = "https://public-api.birdeye.so"


def _headers():
    return {
        "X-API-KEY": BIRDEYE_API_KEY,
        "x-chain": "solana",
        "accept": "application/json"
    }


def _request(endpoint: str, params: dict | None = None):

    if not BIRDEYE_API_KEY:
        raise ValueError("Brak BIRDEYE_API_KEY")

    url = f"{BASE_URL}{endpoint}"

    response = requests.get(
        url,
        headers=_headers(),
        params=params,
        timeout=20
    )

    response.raise_for_status()

    data = response.json()

    if not data.get("success", False):
        raise RuntimeError(
            f"Birdeye API error: {data}"
        )

    return data.get("data", {})


def get_token_overview(mint: str):
    return _request(
        "/defi/token_overview",
        {
            "address": mint
        }
    )


def get_price(mint: str):
    overview = get_token_overview(mint)
    return overview.get("price")


def get_market_data(mint: str):
    overview = get_token_overview(mint)

    return {
        "price": overview.get("price"),
        "price_change_24h": overview.get("priceChange24hPercent"),
        "volume_24h": overview.get("v24hUSD"),
        "market_cap": overview.get("marketCap"),
        "liquidity": overview.get("liquidity"),
    }


if __name__ == "__main__":
    print("Birdeye module OK")
