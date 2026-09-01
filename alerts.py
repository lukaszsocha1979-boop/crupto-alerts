"""
Crypto Alerts
Alerts v1.2

Alerty cenowe:
15m / 30m / 1h

Progi:
11%
20%
30%
40%
...

Bot sprawdza ceny co 5 minut.
"""

import time

from config import (
    FIRST_PRICE_ALERT,
    NEXT_PRICE_ALERT_STEP,
    VOLUME_ALERT_PERCENT,
    GREEN,
    RED,
    BLUE
)

from storage import (
    load_storage,
    save_storage
)


HISTORY_SECONDS = 60 * 60 + 10

INTERVALS = {
    "15m": 15 * 60,
    "30m": 30 * 60,
    "1h": 60 * 60,
}


def _percent_change(old_price, new_price):
    """
    Oblicza zmianę procentową.
    """

    if old_price in (None, 0):
        return 0.0

    return ((new_price - old_price) / old_price) * 100


def _next_level(previous_level, current_change):
    """
    Wyznacza kolejny próg alertu.

    11%
    20%
    30%
    40%
    ...
    """

    change = abs(current_change)

    if change < FIRST_PRICE_ALERT:
        return None

    if previous_level is None:
        return FIRST_PRICE_ALERT

    next_level = previous_level + NEXT_PRICE_ALERT_STEP

    if change >= next_level:
        return next_level

    return None


def _find_price(history, target_time):
    """
    Znajduje najbliższą cenę z historii
    dla wymaganego czasu.
    """

    if not history:
        return None

    best_price = None
    best_difference = None

    for entry in history:

        timestamp = entry.get("timestamp")
        price = entry.get("price")

        if timestamp is None or price is None:
            continue

        difference = abs(timestamp - target_time)

        if best_difference is None or difference < best_difference:
            best_difference = difference
            best_price = price

    return best_price


def _clean_history(history, current_time):
    """
    Usuwa stare wpisy.

    Zostawiamy trochę ponad 1 godzinę,
    aby zawsze można było policzyć interwał 1h.
    """

    minimum_time = current_time - HISTORY_SECONDS

    cleaned = []

    for entry in history:

        timestamp = entry.get("timestamp")

        if timestamp is None:
            continue

        if timestamp >= minimum_time:
            cleaned.append(entry)

    return cleaned


def check_alerts(market):

    storage = load_storage()

    messages = []

    current_time = int(time.time())

    for symbol, data in market.items():

        price = data.get("price")
        volume = data.get("volume_24h")

        if price is None:
            continue

        token = storage.get(symbol, {})

        # -------------------------------------------------
        # HISTORIA CEN
        # -------------------------------------------------

        history = token.get("price_history", [])

        if not isinstance(history, list):
            history = []

        history.append({
            "timestamp": current_time,
            "price": price
        })

        history = _clean_history(
            history,
            current_time
        )

        token["price_history"] = history

        # -------------------------------------------------
        # STAN ALERTÓW
        # -------------------------------------------------

        alert_levels = token.get(
            "alert_levels",
            {}
        )

        if not isinstance(alert_levels, dict):
            alert_levels = {}

        # -------------------------------------------------
        # SPRAWDZANIE 15m / 30m / 1h
        # -------------------------------------------------

        for interval_name, interval_seconds in INTERVALS.items():

            target_time = (
                current_time - interval_seconds
            )

            old_price = _find_price(
                history,
                target_time
            )

            if old_price is None:
                continue

            change = _percent_change(
                old_price,
                price
            )

            interval_state = alert_levels.get(
                interval_name,
                {
                    "up": None,
                    "down": None
                }
            )

            last_up = interval_state.get("up")
            last_down = interval_state.get("down")

            # ---------------------------------------------
            # WZROST
            # ---------------------------------------------

            if change >= 0:

                level = _next_level(
                    last_up,
                    change
                )

                if level is not None:

                    messages.append(
                        f"{GREEN} {symbol} "
                        f"+{change:.2f}% / {interval_name}"
                    )

                    interval_state["up"] = level
                    interval_state["down"] = None

            # ---------------------------------------------
            # SPADEK
            # ---------------------------------------------

            else:

                level = _next_level(
                    last_down,
                    change
                )

                if level is not None:

                    messages.append(
                        f"{RED} {symbol} "
                        f"{change:.2f}% / {interval_name}"
                    )

                    interval_state["down"] = level
                    interval_state["up"] = None

            alert_levels[interval_name] = interval_state

        token["alert_levels"] = alert_levels

        # -------------------------------------------------
        # WOLUMEN
        # -------------------------------------------------

        start_volume = token.get("start_volume")

        if start_volume is None:

            token["start_volume"] = volume

        elif start_volume and volume:

            volume_change = (
                (volume - start_volume)
                / start_volume
            ) * 100

            if volume_change >= VOLUME_ALERT_PERCENT:

                messages.append(
                    f"{BLUE} {symbol} "
                    f"Wolumen +{volume_change:.0f}%"
                )

                token["start_volume"] = volume

        storage[symbol] = token

    save_storage(storage)

    if not messages:
        return None

    return "\n".join(messages)
