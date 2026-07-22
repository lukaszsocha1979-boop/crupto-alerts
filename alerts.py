PRICE_ALERT_15M = 10
PRICE_ALERT_1H = 10
PRICE_ALERT_4H = 15

VOLUME_ALERT = 100
LIQUIDITY_ALERT = 15


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

    alerts = []

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

        if change is not None and abs(change) >= threshold:

            icon = "🚀" if change > 0 else "📉"

            alerts.append(
                f"{icon} {symbol}\n"
                f"{label}: {change:+.2f}%\n"
                f"${previous['price']:.8f} → ${current['price']:.8f}"
            )

    previous = history[-2]

    volume_change = percent_change(
        previous.get("volume24h"),
        current.get("volume24h"),
    )

    if volume_change is not None and volume_change >= VOLUME_ALERT:

        alerts.append(
            f"📊 {symbol}\n"
            f"Wolumen +{volume_change:.2f}%"
        )

    liquidity_change = percent_change(
        previous.get("liquidity"),
        current.get("liquidity"),
    )

    if (
        liquidity_change is not None
        and abs(liquidity_change) >= LIQUIDITY_ALERT
    ):

        alerts.append(
            f"💧 {symbol}\n"
            f"Płynność: {liquidity_change:+.2f}%"
        )

    if not alerts:
        return None

    return "\n\n".join(alerts)
