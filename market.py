import requests


def get_token(token):
    try:

        # CoinGecko (BTC itd.)
        if token["type"] == "coingecko":

            url = (
                "https://api.coingecko.com/api/v3/simple/price"
                f"?ids={token['id']}"
                "&vs_currencies=usd"
                "&include_market_cap=true"
                "&include_24hr_vol=true"
                "&include_24hr_change=true"
            )

            r = requests.get(url, timeout=20)

            if r.status_code != 200:
                return None

            data = r.json()[token["id"]]

            return {
                "price": data["usd"],
                "market_cap": data["usd_market_cap"],
                "volume24h": data["usd_24h_vol"],
                "change24h": data["usd_24h_change"],
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

            if "pairs" not in data or not data["pairs"]:
                return None

            # wybierz parę z największą płynnością
            pair = max(
                data["pairs"],
                key=lambda x: float(
                    x.get("liquidity", {}).get("usd", 0)
                ),
            )

            return {
                "price": float(pair["priceUsd"]),
                "market_cap": float(pair.get("marketCap") or 0),
                "volume24h": float(pair.get("volume", {}).get("h24", 0)),
                "change24h": float(pair.get("priceChange", {}).get("h24", 0)),
                "liquidity": float(pair.get("liquidity", {}).get("usd", 0)),
                "fdv": float(pair.get("fdv") or 0),
                "dex": pair.get("dexId"),
                "chain": pair.get("chainId"),
            }

        return None

    except Exception as e:
        print("MARKET ERROR:", e)
        return None
