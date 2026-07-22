import json
import os

PRICE_ALERT_15M = 10
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


def _find_snapshot(history, steps_back):
    if len(history) <= steps_back:
        return None

    return history[-(steps_back + 1)]


def check_alert(symbol, data):

    history = data.get("history", [])

    if len(history) < 2:
        return None

    current = history[-1]
    previous15 = history[-2]

    cache = load_cache()

    text = []
    score = 0
    key = None

    periods = [
        ("15 min", 1, PRICE_ALERT_15M),
        ("1 h", 4, PRICE_ALERT_1H),
        ("4 h", 16, PRICE_ALERT_4H),
    ]

    for label, steps, threshold in periods:

        previous = _find_snapshot(history, steps)

        if previous is None:
            continue

        change = percent_change(
            previous["price"],
            current["price"],
        )

        if change is None:
            continue

        if abs(change) >= threshold:

            direction = "UP" if change > 0 else "DOWN"
            key = f"{symbol}_{label}_{direction}"

            last = cache.get(key)

            rounded = round(change, 1)

            if last == rounded:
                return None

            cache[key] = rounded
            save_cache(cache)

            score += 5

            icon = "🚀" if change > 0 else "📉"

            text.append(
                f"{icon} Cena ({label}): {change:+.2f}%"
            )

    volume_change = percent_change(
        previous15.get("volume24h"),
        current.get("volume24h"),
    )

    if volume_change is not None and volume_change >= VOLUME_ALERT:
        score += 2
        text.append(f"📊 Wolumen: +{volume_change:.2f}%")

    liquidity_change = percent_change(
        previous15.get("liquidity"),
        current.get("liquidity"),
    )

    if (
        liquidity_change is not None
        and abs(liquidity_change) >= LIQUIDITY_ALERT
    ):
        score += 2
        text.append(f"💧 Płynność: {liquidity_change:+.2f}%")

    if not text:
        return None

    return (
        f"🚨 {symbol}\n\n"
        + "\n".join(text)
        + f"\n\n⭐ Siła sygnału: {score}/10"
    )
