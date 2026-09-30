"""
Crypto Alerts
Birdeye API v1.4

Aktualny endpoint cenowy:
 /defi/v3/price/stats/single

Stary:
 /defi/price

Stary endpoint zwracał:
Compute units usage limit exceeded
mimo dostępnych CU.
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

    return data.get("data", [])


def get_price(mint: str):
    """
    Pobiera aktualną cenę tokena.

    Używamy:
    /defi/v3/price/stats/single

    Pobieramy jeden timeframe: 30m.
    Aktualna cena jest zwracana w polu price.
    """

    data = _request(
        "/defi/v3/price/stats/single",
        {
            "address": mint,
            "list_timeframe": "30m",
        },
    )

    if not data:
        raise RuntimeError(
            "Birdeye V3: brak danych dla tokena"
        )

    token_data = data[0]

    timeframe_data = token_data.get("data", [])

    if not timeframe_data:
        raise RuntimeError(
            "Birdeye V3: brak danych timeframe"
        )

    price = timeframe_data[0].get("price")

    if price is None:
        raise RuntimeError(
            "Birdeye V3: brak aktualnej ceny"
        )

    return price


def get_market_data(mint: str):
    """
    Zwraca dane w formacie zgodnym z market.py.

    Aktualnie pobieramy tylko aktualną cenę.
    Historię i alerty nadal obsługuje alerts.py
    oraz storage.json.
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
