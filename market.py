import requests

BASE_URL = "https://api.dexscreener.com/latest/dex/tokens/"


def get_token(address):
    try:
        r = requests.get(BASE_URL + address, timeout=20)

        if r.status_code != 200:
            return None

        data = r.json()

        if not data.get("pairs"):
            return None

        pair = data["pairs"][0]

        return {
            "price": float(pair["priceUsd"]),
            "volume24h": float(pair["volume"]["h24"]),
            "liquidity": float(pair["liquidity"]["usd"]),
            "fdv": pair.get("fdv", 0),
            "chain": pair["chainId"],
            "dex": pair["dexId"]
        }

    except Exception as e:
        print(e)
        return None
