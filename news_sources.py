from config import KEYWORDS

HIGH_PRIORITY = [
    "partnership",
    "integration",
    "listing",
    "listed",
    "binance",
    "coinbase",
    "kraken",
    "airdrop",
    "mainnet",
    "bridge",
    "hack",
    "exploit",
    "security",
    "upgrade",
    "token unlock",
]

MEDIUM_PRIORITY = [
    "update",
    "roadmap",
    "governance",
    "proposal",
    "staking",
    "wallet",
    "launch",
]


def is_interesting(text):
    text = text.lower()

    for words in KEYWORDS.values():
        if any(word.lower() in text for word in words):
            return True

    return False


def get_priority(text):
    text = text.lower()

    score = 1

    for word in HIGH_PRIORITY:
        if word in text:
            score += 6

    for word in MEDIUM_PRIORITY:
        if word in text:
            score += 3

    if score >= 7:
        return "🟢 WYSOKA", score
    elif score >= 4:
        return "🟡 ŚREDNIA", score
    else:
        return "🔴 NISKA", score
