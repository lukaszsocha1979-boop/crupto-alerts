import requests

BIRDEYE_API = "https://public-api.birdeye.so/defi/token_overview"

HEADERS = {
    "accept": "application/json"
}


def get_token_data(address):
    try:
        r = requests.get(
            BIRDEYE_API,
            params={"address": address},
            headers=HEADERS,
            timeout=20,
        )

        data = r.json()["data"]

        return {
            "price": data.get("price"),
            "priceChange1h": data.get("priceChange1hPercent"),
            "priceChange24h": data.get("priceChange24hPercent"),
            "volume24h": data.get("v24hUSD"),
            "marketCap": data.get("mc"),
        }

    except Exception:
        return None
