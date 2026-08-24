"""
Crypto Alerts
Birdeye API v1.3
"""

import requests

from config import BIRDEYE_API_KEY


BASE_URL = "https://public-api.birdeye.so"


def _headers():
    return {
        "X-API-KEY": BIRDEYE_API_KEY,
        "x-chain": "solana",
        "accept": "application/json",
    }


def _request(endpoint: str, params: dict | None = None):

    if not BIRDEYE_API_KEY:
        raise ValueError("Brak BIRDEYE_API_KEY")

    url = f"{BASE_URL}{endpoint}"

    response = requests.get(
        url,
        headers=_headers(),
        params=params,
        timeout=20,
    )

    # Diagnostyka odpowiedzi Birdeye
    print("=== BIRDEYE DEBUG ===")
    print("URL:", response.url)
    print("Status:", response.status_code)
    print(
        "Remaining-CU:",
        response.headers.get("x-credits-remaining")
    )
    print(
        "Used-CU:",
        response.headers.get("x-credits-used")
    )
    print("Message:", response.text)
    print("=====================")

    if not response.ok:
        print(f"❌ Birdeye HTTP {response.status_code}")
        print(f"❌ Birdeye response: {response.text}")

        response.raise_for_status()

    data = response.json()

    if not data.get("success", False):
        raise RuntimeError(
            f"Birdeye API error: {data}"
        )

    return data.get("data", {})


def get_price(mint: str):
    """
    Pobiera aktualną cenę tokena.

    Endpoint:
    /defi/price

    Koszt:
    3 CU
    """

    data = _request(
        "/defi/price",
        {
            "address": mint,
        },
    )

    return data.get("value")


def get_market_data(mint: str):
    """
    Zwraca dane w formacie zgodnym z market.py.

    W tej wersji pobieramy tylko aktualną cenę,
    aby ograniczyć zużycie Compute Units.
    """

    price = get_price(mint)

    return {
        "price": price,
        "price_change_24h": None,
        "volume_24h": None,
        "market_cap": None,
        "liquidity": None,
    }


if __name__ == "__main__":
    print("Birdeye module OK")
