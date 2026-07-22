import json
import os

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


def snapshot_minutes(history, minutes):

    if not history:
        return None

    current = history[-1]["time"]
    target = current - minutes * 60

    candidate = None

    for item in history:
        if item["time"] <= target:
            candidate = item

    return candidate


def score_signal(price4h, volume, liquidity, buys, sells):

    score = 0

    if price4h is not None:
        if abs(price4h) >= 30:
            score += 4
        elif abs(price4h) >= 20:
            score += 3
        elif abs(price4h) >= 10:
            score += 2
        elif abs(price4h) >= 3:
            score += 1

    if volume is not None:
        if volume >= 300:
            score += 3
        elif volume >= 150:
            score += 2
        elif volume >= 50:
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

            if ratio >= 20:
                score += 2
            elif ratio >= 5:
                score += 1

    return min(score, 10)


def check_alert(symbol, data):

    history = data.get("history", [])

    if len(history) < 2:
        return None

    current = history[-1]

    p15 = snapshot_minutes(history, 15)
    p60 = snapshot_minutes(history, 60)
    p240 = snapshot_minutes(history, 240)

    price15 = percent_change(p15["price"], current["price"]) if p15 else None
    price60 = percent_change(p60["price"], current["price"]) if p60 else None
    price240 = percent_change(p240["price"], current["price"]) if p240 else None

    trigger = False

    for p in (price15, price60, price240):
        if p is not None and abs(p) >= 1:
            trigger = True

    if not trigger:
        return None

    previous = history[-2]

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
        price240,
        volume,
        liquidity,
        buys,
        sells,
    )

    direction = "UP" if (price15 or 0) >= 0 else "DOWN"

    cache = load_cache()

    rounded = round(price15 or 0, 1)
    key = f"{symbol}_{direction}"

    if cache.get(key) == rounded:
        return None

    cache[key] = rounded
    save_cache(cache)

    lines = [
        f"🚨 {symbol}",
        "",
        "📈 Cena"
    ]

    if price15 is not None:
        lines.append(f"15m : {price15:+.2f}%")

    if price60 is not None:
        lines.append(f"1h  : {price60:+.2f}%")

    if price240 is not None:
        lines.append(f"4h  : {price240:+.2f}%")

    if volume is not None:
        lines.extend([
            "",
            f"📊 Wolumen: {volume:+.2f}%"
        ])

    if liquidity is not None:
        lines.append(f"💧 Płynność: {liquidity:+.2f}%")

    if buys is not None and sells is not None:
        lines.extend([
            "",
            f"🟢 Buy: {buys}",
            f"🔴 Sell: {sells}",
        ])

    lines.extend([
        "",
        f"⭐ Siła sygnału: {score}/10"
    ])

    return "\n".join(lines)
