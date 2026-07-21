import re

TRANSLATIONS = {
    "bitcoin": "Bitcoin",
    "btc": "BTC",
    "ethereum": "Ethereum",
    "solana": "Solana",
    "zeus": "ZEUS",

    "price": "cena",
    "prices": "ceny",

    "surges": "gwałtownie rośnie",
    "surged": "gwałtownie wzrósł",
    "rises": "rośnie",
    "rose": "wzrósł",
    "falls": "spada",
    "fell": "spadł",
    "drops": "spada",
    "drop": "spadek",

    "launch": "uruchamia",
    "launches": "uruchamia",
    "launched": "uruchomił",

    "announces": "ogłasza",
    "announced": "ogłosił",

    "introduces": "wprowadza",
    "introduced": "wprowadził",

    "reveals": "ujawnia",
    "revealed": "ujawnił",

    "support": "wsparcie",
    "integration": "integracja",
    "partnership": "partnerstwo",
    "listing": "listing",
    "listed": "notowany",

    "exchange": "giełda",
    "wallet": "portfel",
    "network": "sieć",
    "token": "token",
    "bridge": "most",

    "security": "bezpieczeństwo",
    "hack": "atak hakerski",
    "airdrop": "airdrop",

    "proposal": "propozycja",
    "recovery": "odzyskiwanie",
    "attack": "atak",
    "quantum": "kwantowy",
    "trading": "handel",
    "market": "rynek",
    "fund": "fundusz",
    "etf": "ETF",
}


def translate(text):

    result = text

    for eng in sorted(TRANSLATIONS.keys(), key=len, reverse=True):

        pl = TRANSLATIONS[eng]

        result = re.sub(
            rf"\b{re.escape(eng)}\b",
            pl,
            result,
            flags=re.IGNORECASE,
        )

    result = re.sub(r"\s+", " ", result).strip()

    return result
