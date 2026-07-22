import re


def contains(text, words):
    text = text.lower()
    return any(word.lower() in text for word in words)


def translate(title):

    if not title:
        return ""

    t = title.lower()

    coin = []

    if contains(t, ["bitcoin", "btc"]):
        coin.append("Bitcoin")

    if contains(t, ["ethereum", "eth"]):
        coin.append("Ethereum")

    if contains(t, ["solana", "sol"]):
        coin.append("Solana")

    if contains(t, ["jupiter"]):
        coin.append("Jupiter")

    if contains(t, ["wormhole"]):
        coin.append("Wormhole")

    if contains(t, ["pyth"]):
        coin.append("Pyth")

    if contains(t, ["zeus"]):
        coin.append("ZEUS")

    if coin:
        coin_text = ", ".join(coin)
    else:
        coin_text = "Rynek kryptowalut"

    if contains(t, ["launch", "launches", "launched"]):
        return f"🚀 {coin_text}: ogłoszono uruchomienie nowej usługi lub produktu."

    if contains(t, ["listing", "listed", "lists"]):
        return f"📈 {coin_text}: pojawił się nowy listing na giełdzie."

    if contains(t, ["etf"]):
        return f"💰 {coin_text}: wiadomość dotycząca funduszy ETF."

    if contains(t, ["hack", "hacked", "exploit", "stolen"]):
        return f"🚨 {coin_text}: wykryto atak lub problem z bezpieczeństwem."

    if contains(t, ["security"]):
        return f"🛡️ {coin_text}: wiadomość dotycząca bezpieczeństwa."

    if contains(t, ["quantum"]):
        return f"⚛️ {coin_text}: pojawiły się informacje dotyczące zagrożeń lub rozwiązań związanych z komputerami kwantowymi."

    if contains(t, ["proposal"]):
        return f"🗳️ {coin_text}: opublikowano nową propozycję zmian."

    if contains(t, ["partnership", "partner"]):
        return f"🤝 {coin_text}: ogłoszono nowe partnerstwo."

    if contains(t, ["airdrop"]):
        return f"🎁 {coin_text}: informacje o airdropie."

    if contains(t, ["staking", "stake"]):
        return f"💎 {coin_text}: wiadomość dotycząca stakingu."

    if contains(t, ["upgrade", "update"]):
        return f"⬆️ {coin_text}: zapowiedziano aktualizację projektu."

    if contains(t, ["integration"]):
        return f"🔗 {coin_text}: ogłoszono nową integrację."

    if contains(t, ["adoption"]):
        return f"🌍 {coin_text}: rośnie wykorzystanie kryptowalut."

    if contains(t, ["institution", "morgan stanley", "blackrock", "fidelity"]):
        return f"🏦 {coin_text}: instytucje finansowe zwiększają zaangażowanie."

    if contains(t, ["price"]):
        return f"💹 {coin_text}: wiadomość dotycząca zmian ceny."

    if contains(t, ["whale"]):
        return f"🐋 {coin_text}: odnotowano dużą aktywność dużych inwestorów."

    if contains(t, ["record", "ath"]):
        return f"🏆 {coin_text}: osiągnięto nowy rekord."

    if contains(t, ["drop", "falls", "fall", "crash"]):
        return f"📉 {coin_text}: pojawiły się informacje o spadkach."

    if contains(t, ["rise", "surge", "rally", "gain"]):
        return f"📈 {coin_text}: pojawiły się informacje o wzrostach."

    return f"📰 {coin_text}: {title}"
