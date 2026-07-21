import requests

BASE_URL = "https://api.dexscreener.com/latest/dex/tokens/"


def get_token(address):
    try:
        response = requests.get(BASE_URL + address, timeout=20)

        if response.status_code != 200:
            return None

        data = response.json()

        if "pairs" not in data:
            return None

        if len(data["pairs"]) == 0:
            return None

        pair = data["pairs"][0]

        return {
            "price": float(pair.get("priceUsd", 0)),
            "volume24h": float(pair.get("volume", {}).get("h24", 0)),
            "liquidity": float(pair.get("liquidity", {}).get("usd", 0)),
            "fdv": float(pair.get("fdv", 0)),
            "dex": pair.get("dexId", ""),
            "chain": pair.get("chainId", "")
        }

    except Exception as e:
        print(e)
        return None
