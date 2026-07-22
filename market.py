import requests


def get_token(token):
    try:

        # CoinGecko (BTC)
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
                return None

            data = r.json()[token["id"]]

            return {
                "price": float(data["usd"]),
                "market_cap": float(data["usd_market_cap"]),
                "volume24h": float(data["usd_24h_vol"]),
            }

        # Solana (DexScreener)
        if token["type"] == "solana":

            url = (
                "https://api.dexscreener.com/latest/dex/tokens/"
                f"{token['mint']}"
            )

            r = requests.get(url, timeout=20)

            if r.status_code != 200:
                return None

            data = r.json()

            pairs = data.get("pairs")

            if not pairs:
                return None

            # Para z największą płynnością
            pair = max(
                pairs,
                key=lambda p: float(
                    p.get("liquidity", {}).get("usd", 0)
                ),
            )

            txns = pair.get("txns", {})
            h24 = txns.get("h24", {})

            return {
                "price": float(pair.get("priceUsd") or 0),
                "market_cap": float(pair.get("marketCap") or 0),
                "fdv": float(pair.get("fdv") or 0),
                "volume24h": float(
                    pair.get("volume", {}).get("h24", 0)
                ),
                "liquidity": float(
                    pair.get("liquidity", {}).get("usd", 0)
                ),
                "buys24h": int(
                    h24.get("buys", 0)
                ),
                "sells24h": int(
                    h24.get("sells", 0)
                ),
                "pair": pair.get("pairAddress"),
                "dex": pair.get("dexId"),
                "chain": pair.get("chainId"),
                "url": pair.get("url"),
            }

        return None

    except Exception as e:
        print("MARKET ERROR:", e)
        return None
