TRANSLATIONS = {
    "bitcoin": "Bitcoin",
    "btc": "BTC",
    "price": "cena",
    "prices": "ceny",
    "surges": "gwałtownie rośnie",
    "falls": "spada",
    "rises": "rośnie",
    "drops": "spada",
    "partnership": "partnerstwo",
    "integration": "integracja",
    "listing": "listing",
    "listed": "notowany",
    "launch": "uruchomienie",
    "bridge": "most",
    "upgrade": "aktualizacja",
    "security": "bezpieczeństwo",
    "hack": "atak hakerski",
    "wallet": "portfel",
    "exchange": "giełda",
    "token": "token",
    "network": "sieć",
    "announces": "ogłasza",
    "introduces": "wprowadza",
    "reveals": "ujawnia",
    "support": "wsparcie",
    "stablecoin": "stablecoin",
    "airdrop": "airdrop"
}


def translate(text):
    result = text

    for eng, pl in TRANSLATIONS.items():
        result = result.replace(eng, pl)
        result = result.replace(eng.capitalize(), pl)

    return result
