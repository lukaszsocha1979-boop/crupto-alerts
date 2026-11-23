
import requests

from tokens import TOKENS

URL = "https://api.dexscreener.com/tokens/v1/solana/"

addresses = [
    token["mint"]
    for token in TOKENS.values()
]

print("Sprawdzam DEX Screener...")
print("Liczba tokenów:", len(addresses))

response = requests.get(
    URL + ",".join(addresses),
    timeout=30
)

print("HTTP:", response.status_code)
response.raise_for_status()

pairs = response.json()

print("Liczba znalezionych par:", len(pairs))

for symbol, token in TOKENS.items():
    mint = token["mint"]

    matching = [
        pair for pair in pairs
        if pair.get("chainId") == "solana"
        and pair.get("baseToken", {}).get("address") == mint
        and pair.get("priceUsd") is not None
    ]

    matching.sort(
        key=lambda pair: (
            pair.get("liquidity", {}).get("usd") or 0
        ),
        reverse=True
    )

    if not matching:
        print(f"{symbol}: BRAK ODPOWIEDNIEJ PARY")
        continue

    pair = matching[0]

    print(
        f"{symbol}: "
        f"${pair['priceUsd']} | "
        f"Płynność: "
        f"${pair.get('liquidity', {}).get('usd', 0)} | "
        f"DEX: {pair.get('dexId')} | "
        f"Para: {pair.get('pairAddress')}"
    )
