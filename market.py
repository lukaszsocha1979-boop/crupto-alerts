import os
import requests


BIRDEYE_URL = "https://public-api.birdeye.so/defi/token_overview"


def get_token(token):
    try:

        # -----------------------------
        # CoinGecko (BTC)
        # -----------------------------
        if token["type"] == "coingecko":

            url = (
                "https://api.coingecko.com/api/v3/simple/price"
                f"?ids={token['id']}"
                "&vs_currencies=usd"
                "&include_market_cap=true"
                "&include_24hr_vol=true"
            )

            r = requests.get(url, timeout=20)

            if r.status_code != 200:
                print("CoinGecko:", r.text)
                return None

            data = r.json()[token["id"]]

            return {
                "price": float(data["usd"]),
                "market_cap": float(data["usd_market_cap"]),
                "volume24h": float(data["usd_24h_vol"]),
            }

        # -----------------------------
        # Solana (BirdEye)
        # -----------------------------
        if token["type"] == "solana":

            api_key = os.getenv("BIRDEYE_API_KEY")

            if not api_key:
                print("Brak BIRDEYE_API_KEY")
                return None

            headers = {
                "accept": "application/json",
                "x-api-key": api_key,
                "x-chain": "solana",
            }

            r = requests.get(
                BIRDEYE_URL,
                params={
                    "address": token["mint"]
                },
                headers=headers,
                timeout=20,
            )

            if r.status_code != 200:
                print("BirdEye:", r.status_code, r.text)
                return None

            body = r.json()

            if not body.get("success"):
                print(body)
                return None

            data = body["data"]

            return {
                "price": float(data.get("price") or 0),
                "market_cap": float(data.get("marketCap") or 0),
                "fdv": float(data.get("fdv") or 0),
                "volume24h": float(data.get("v24hUSD") or 0),
                "liquidity": float(data.get("liquidity") or 0),
                "buys24h": int(data.get("buy24h") or 0),
                "sells24h": int(data.get("sell24h") or 0),
                "holders": int(data.get("holder") or 0),
                "price_change_24h": float(data.get("priceChange24hPercent") or 0),
            }

        return None

    except Exception as e:
        print("MARKET ERROR:", e)
        return None
