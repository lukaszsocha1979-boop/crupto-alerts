import requests


def get_token(token):

    try:

        # BTC z CoinGecko
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

        # Pozostałe tokeny (tymczasowo)
        return None

    except Exception as e:
        print(e)
        return None
