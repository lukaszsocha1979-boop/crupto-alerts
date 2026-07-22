import json
import os

PRICE_ALERT_15M = 1
PRICE_ALERT_1H = 10
PRICE_ALERT_4H = 15

VOLUME_ALERT = 100
LIQUIDITY_ALERT = 15

CACHE_FILE = "alert_cache.json"


def load_cache():
    if not os.path.exists(CACHE_FILE):
        return {}

    with open(CACHE_FILE, "r") as f:
        return json.load(f)


def save_cache(cache):
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=2)


def percent_change(old, new):
    if old in (None, 0) or new is None:
        return None
    return ((new - old) / old) * 100


def snapshot(history, back):
    if len(history) <= back:
        return None
    return history[-(back + 1)]


def score_signal(price, volume, liquidity, buys, sells):

    score = 0

    if abs(price) >= 20:
        score += 4
    elif abs(price) >= 10:
        score += 3
    elif abs(price) >= 5:
        score += 2
    elif abs(price) >= 1:
        score += 1

    if volume is not None:
        if volume >= 300:
            score += 3
        elif volume >= 150:
            score += 2
        elif volume >= 100:
            score += 1

    if liquidity is not None:
        if liquidity >= 30:
            score += 2
        elif liquidity >= 15:
            score += 1

    if buys is not None and sells is not None:

        total = buys + sells

        if total > 0:

            ratio = (buys - sells) / total * 100

            if ratio > 20:
                score += 2
            elif ratio > 5:
                score += 1

    return min(score, 10)


def check_alert(symbol, data):

    history = data.get("history", [])

    if len(history) < 2:
        return None

    current = history[-1]
    previous = snapshot(history, 1)

    price = percent_change(
        previous["price"],
        current["price"],
    )

    if price is None:
        return None

    if abs(price) < PRICE_ALERT_15M:
        return None

    volume = percent_change(
        previous.get("volume24h"),
        current.get("volume24h"),
    )

    liquidity = percent_change(
        previous.get("liquidity"),
        current.get("liquidity"),
    )

    buys = current.get("buys24h")
    sells = current.get("sells24h")

    score = score_signal(
        price,
        volume,
        liquidity,
        buys,
        sells,
    )

    direction = "UP" if price > 0 else "DOWN"

    cache = load_cache()

    key = f"{symbol}_{direction}"

    rounded = round(price, 1)

    if cache.get(key) == rounded:
        return None

    cache[key] = rounded
    save_cache(cache)

    lines = [
        f"🚨 {symbol}",
        "",
        f"{'🚀' if price > 0 else '📉'} Cena: {price:+.2f}%"
    ]

    if volume is not None:
        lines.append(f"📊 Wolumen: {volume:+.2f}%")

    if liquidity is not None:
        lines.append(f"💧 Płynność: {liquidity:+.2f}%")

    if buys is not None and sells is not None:
        lines.append(f"🟢 Buy: {buys}")
        lines.append(f"🔴 Sell: {sells}")

    lines.append("")
    lines.append(f"⭐ Siła sygnału: {score}/10")

    return "\n".join(lines)
