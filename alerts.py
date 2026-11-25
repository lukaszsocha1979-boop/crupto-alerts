
"""
Crypto Alerts
Alerts v1.8

Interwały:
15m / 30m / 1h / 4h / 1d

Progi:
9% / 18% / 24% / 30%
Następnie co 6%.

Ponowne alerty:
Próg zostaje ponownie uzbrojony po zejściu
zmiany ceny poniżej jego wartości.
"""

import time

from config import (
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

# Dopuszczalne odchylenie przy wyszukiwaniu ceny historycznej.
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
    """Sprawdza, czy zapisany próg należy do aktualnej skali."""

    if level is None:
        return False

    try:
        level = float(level)
    except (TypeError, ValueError):
        return False

    if level in PRICE_ALERT_LEVELS:
        return True

    return (
        level >= 30
        and (level - 30) % NEXT_PRICE_ALERT_STEP == 0
    )


def _highest_reached_level(change):
    """Zwraca najwyższy osiągnięty próg."""

    change = abs(change)
    levels = list(PRICE_ALERT_LEVELS)

    if change >= 30:
        next_level = 30 + NEXT_PRICE_ALERT_STEP

        while next_level <= change:
            levels.append(next_level)
            next_level += NEXT_PRICE_ALERT_STEP

    reached = [
        level for level in levels
        if change >= level
    ]

    return max(reached) if reached else None


def _update_alert_level(previous_level, current_change):
    """
    Aktualizuje poziom alertu.

    Zwraca:
    - nowy zapamiętany poziom,
    - poziom, dla którego należy wysłać alert.

    Po zejściu poniżej poprzedniego progu
    próg zostaje ponownie uzbrojony.
    """

    highest = _highest_reached_level(current_change)

    if previous_level is None:
        return highest, highest

    if not _valid_level(previous_level):
        return highest, highest

    previous_level = float(previous_level)

    if highest is None:
        return None, None

    if highest > previous_level:
        return highest, highest

    if highest < previous_level:
        return highest, None

    return previous_level, None


def _find_price(history, target_time):
    """
    Wybiera najnowszą cenę zapisaną przed czasem docelowym.
    Nie korzysta z próbek z przyszłości.
    """

    candidates = []

    for entry in history:
        timestamp = entry.get("timestamp")
        price = entry.get("price")

        if timestamp is None or price is None:
            continue

        try:
            timestamp = float(timestamp)
            price = float(price)
        except (TypeError, ValueError):
            continue

        difference = target_time - timestamp

        if 0 <= difference <= TIME_TOLERANCE_SECONDS:
            candidates.append((timestamp, price))

    if not candidates:
        return None

    candidates.sort(
        key=lambda item: item[0],
        reverse=True
    )

    return candidates[0][1]


def _clean_history(history, current_time):
    """Usuwa wpisy starsze niż 24 godziny i 10 minut."""

    minimum_time = current_time - HISTORY_SECONDS
    cleaned = []

    for entry in history:

        try:
            timestamp = float(entry.get("timestamp"))
            price = float(entry.get("price"))

        except (TypeError, ValueError, AttributeError):
            continue

        if timestamp >= minimum_time and price > 0:
            cleaned.append({
                "timestamp": timestamp,
                "price": price
            })

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

        try:
            price = float(price)

            if price <= 0:
                raise ValueError("Cena musi być większa od zera")

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
                interval_state = {
                    "up": None,
                    "down": None
                }

            # Ruch wzrostowy.
            if change > 0:

                interval_state["down"] = None

                new_level, alert_level = _update_alert_level(
                    interval_state.get("up"),
                    change
                )

                interval_state["up"] = new_level

                if alert_level is not None:

                    messages.append(
                        f"{GREEN} {symbol} "
                        f"+{change:.2f}% / {interval_name} "
                        f"(próg {alert_level}%)"
                    )

            # Ruch spadkowy.
            elif change < 0:

                interval_state["up"] = None

                new_level, alert_level = _update_alert_level(
                    interval_state.get("down"),
                    change
                )

                interval_state["down"] = new_level

                if alert_level is not None:

                    messages.append(
                        f"{RED} {symbol} "
                        f"{change:.2f}% / {interval_name} "
                        f"(próg -{alert_level}%)"
                    )

            # Powrót dokładnie do poziomu odniesienia.
            else:

                interval_state["up"] = None
                interval_state["down"] = None

            alert_levels[interval_name] = interval_state

        token["alert_levels"] = alert_levels

        # Alerty wolumenowe.
        start_volume = token.get("start_volume")

        if volume is not None:

            try:
                volume = float(volume)

                if start_volume is None:

                    token["start_volume"] = volume

                elif start_volume and volume:

                    start_volume = float(start_volume)

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
                print(
                    f"⚠️ {symbol}: nieprawidłowy wolumen"
                )

        storage[symbol] = token

    save_storage(storage)

    if not messages:
        return None

    return "\n".join(messages)
