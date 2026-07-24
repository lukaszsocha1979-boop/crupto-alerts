"""
Crypto Alerts
Alerts v1.0
"""

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

    if abs(current_change) < FIRST_PRICE_ALERT:
        return None

    if previous_level is None:
        return FIRST_PRICE_ALERT

    level = previous_level

    while abs(current_change) >= level + NEXT_PRICE_ALERT_STEP:
        level += NEXT_PRICE_ALERT_STEP

    if level != previous_level:
        return level

    return None


def check_alerts(market):

    storage = load_storage()

    messages = []

    for symbol, data in market.items():

        price = data.get("price")
        volume = data.get("volume_24h")

        if price is None:
            continue

        token = storage.get(symbol, {})

        start_price = token.get("start_price")
        start_volume = token.get("start_volume")

        last_up = token.get("last_up_alert")
        last_down = token.get("last_down_alert")

        if start_price is None:

            storage[symbol] = {
                "start_price": price,
                "start_volume": volume,
                "last_up_alert": None,
                "last_down_alert": None
            }

            continue

        change = _percent_change(start_price, price)

        if change >= 0:

            level = _next_level(last_up, change)

            if level is not None:

                messages.append(
                    f"{GREEN} {symbol} +{change:.2f}%"
                )

                token["last_up_alert"] = level
                token["last_down_alert"] = None
                token["start_price"] = price

        else:

            level = _next_level(last_down, change)

            if level is not None:

                messages.append(
                    f"{RED} {symbol} {change:.2f}%"
                )

                token["last_down_alert"] = level
                token["last_up_alert"] = None
                token["start_price"] = price

        if start_volume and volume:

            volume_change = (
                (volume - start_volume) / start_volume
            ) * 100

            if volume_change >= VOLUME_ALERT_PERCENT:

                messages.append(
                    f"{BLUE} {symbol} Wolumen +{volume_change:.0f}%"
                )

                token["start_volume"] = volume

        storage[symbol] = token

    save_storage(storage)

    if not messages:
        return None

    return "\n".join(messages)
