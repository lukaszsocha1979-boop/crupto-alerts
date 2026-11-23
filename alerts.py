
"""
Crypto Alerts
Alerts v1.5

Interwały:
15m / 30m / 1h / 4h / 1d

Progi:
9% / 18% / 24% / 30%
Następnie co 6%.
"""

import time

from config import (
    FIRST_PRICE_ALERT,
    NEXT_PRICE_ALERT_STEP,
    PRICE_ALERT_LEVELS,
    VOLUME_ALERT_PERCENT,
    GREEN,
    RED,
    BLUE
)

from storage import load_storage, save_storage


# Historia obejmuje 24 godziny i 10 minut.
HISTORY_SECONDS = 24 * 60 * 60 + 10 * 60

# Przy sprawdzaniu co 5 minut dopuszczamy niewielkie
# opóźnienie wykonania GitHub Actions.
TIME_TOLERANCE_SECONDS = 7 * 60


INTERVALS = {
    "15m": 15 * 60,
    "30m": 30 * 60,
    "1h": 60 * 60,
    "4h": 4 * 60 * 60,
    "1d": 24 * 60 * 60,
}


def _percent_change(old_price, new_price):
    if old_price in (None, 0):
        return 0.0

    return ((new_price - old_price) / old_price) * 100


def _valid_level(level):
    """Sprawdza, czy zapisany próg należy do nowej skali."""

    if level is None:
        return False

    try:
        level = float(level)
    except (TypeError, ValueError):
        return False

    if level in PRICE_ALERT_LEVELS:
        return True

    return level >= 30 and (level - 30) % NEXT_PRICE_ALERT_STEP == 0


def _highest_reached_level(change):
    """Zwraca najwyższy osiągnięty próg."""

    change = abs(change)

    levels = list(PRICE_ALERT_LEVELS)

    if change >= 30:
        next_level = 36

        while next_level <= change:
            levels.append(next_level)
            next_level += NEXT_PRICE_ALERT_STEP

    reached = [
        level for level in levels
        if change >= level
    ]

    return max(reached) if reached else None


def _next_level(previous_level, current_change):
    """Wyznacza następny próg alertu."""

    change = abs(current_change)

    if previous_level is None:
        return _highest_reached_level(change)

    if not _valid_level(previous_level):
        return _highest_reached_level(change)

    if previous_level < 30:
        if previous_level == 9:
            next_level = 18
        elif previous_level == 18:
            next_level = 24
        elif previous_level == 24:
            next_level = 30
        else:
            return _highest_reached_level(change)
    else:
        next_level = previous_level + NEXT_PRICE_ALERT_STEP

    if change >= next_level:
        return next_level

    return None


def _find_price(history, target_time):
    """Znajduje najbliższą cenę do wymaganego czasu."""

    best_entry = None
    best_difference = None

    for entry in history:

        timestamp = entry.get("timestamp")
        price = entry.get("price")

        if timestamp is None or price is None:
            continue

        difference = abs(timestamp - target_time)

        if difference > TIME_TOLERANCE_SECONDS:
            continue

        if best_difference is None or difference < best_difference:
            best_difference = difference
            best_entry = entry

    if best_entry is None:
        return None

    return best_entry.get("price")


def _clean_history(history, current_time):
    """Usuwa wpisy starsze niż 24 godziny i 10 minut."""

    minimum_time = current_time - HISTORY_SECONDS

    return [
        entry for entry in history
        if entry.get("timestamp") is not None
        and entry["timestamp"] >= minimum_time
    ]


def check_alerts(market):

    storage = load_storage()
    messages = []
    current_time = int(time.time())

    for symbol, data in market.items():

        price = data.get("price")
        volume = data.get("volume_24h")

        if price is None:
            continue

        try:
            price = float(price)
        except (TypeError, ValueError):
            print(f"❌ {symbol}: nieprawidłowa cena")
            continue

        token = storage.get(symbol, {})

        history = token.get("price_history", [])

        if not isinstance(history, list):
            history = []

        history.append({
            "timestamp": current_time,
            "price": price
        })

        history = _clean_history(history, current_time)
        token["price_history"] = history

        alert_levels = token.get("alert_levels", {})

        if not isinstance(alert_levels, dict):
            alert_levels = {}

        for interval_name, interval_seconds in INTERVALS.items():

            target_time = current_time - interval_seconds

            old_price = _find_price(history, target_time)

            if old_price is None:
                continue

            change = _percent_change(old_price, price)

            interval_state = alert_levels.get(
                interval_name,
                {"up": None, "down": None}
            )

            if not isinstance(interval_state, dict):
                interval_state = {"up": None, "down": None}

            last_up = interval_state.get("up")
            last_down = interval_state.get("down")

            if change >= 0:

                level = _next_level(last_up, change)

                if level is not None:
                    messages.append(
                        f"{GREEN} {symbol} "
                        f"+{change:.2f}% / {interval_name} "
                        f"(próg {level}%)"
                    )

                    interval_state["up"] = level
                    interval_state["down"] = None

            else:

                level = _next_level(last_down, change)

                if level is not None:
                    messages.append(
                        f"{RED} {symbol} "
                        f"{change:.2f}% / {interval_name} "
                        f"(próg -{level}%)"
                    )

                    interval_state["down"] = level
                    interval_state["up"] = None

            alert_levels[interval_name] = interval_state

        token["alert_levels"] = alert_levels

        # Alerty wolumenowe
        start_volume = token.get("start_volume")

        if volume is not None:
            try:
                volume = float(volume)

                if start_volume is None:
                    token["start_volume"] = volume

                elif start_volume and volume:
                    volume_change = (
                        (volume - start_volume) / start_volume
                    ) * 100

                    if volume_change >= VOLUME_ALERT_PERCENT:
                        messages.append(
                            f"{BLUE} {symbol} "
                            f"Wolumen +{volume_change:.0f}%"
                        )

                        token["start_volume"] = volume

            except (TypeError, ValueError):
                print(f"⚠️ {symbol}: nieprawidłowy wolumen")

        storage[symbol] = token

    save_storage(storage)

    if not messages:
        return None

    return "\n".join(messages)
