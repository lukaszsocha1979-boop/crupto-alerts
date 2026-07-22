PRICE_ALERT = 10       # %
VOLUME_ALERT = 100     # %
LIQUIDITY_ALERT = 15   # %


def percent_change(old, new):
    if old is None or new is None or old == 0:
        return None
    return ((new - old) / old) * 100


def check_alert(symbol, old_data, new_data):

    if old_data is None or new_data is None:
        return None

    alerts = []

    # CENA
    change = percent_change(
        old_data.get("price"),
        new_data.get("price"),
    )

    if change is not None and abs(change) >= PRICE_ALERT:
        alerts.append(
            f"{'🚀' if change > 0 else '📉'} {symbol}\n"
            f"Cena: {change:+.2f}%\n"
            f"${old_data['price']:.8f} → ${new_data['price']:.8f}"
        )

    # WOLUMEN
    volume_change = percent_change(
        old_data.get("volume24h"),
        new_data.get("volume24h"),
    )

    if volume_change is not None and volume_change >= VOLUME_ALERT:
        alerts.append(
            f"📊 {symbol}\n"
            f"Wolumen: +{volume_change:.2f}%"
        )

    # PŁYNNOŚĆ
    if "liquidity" in old_data and "liquidity" in new_data:

        liquidity_change = percent_change(
            old_data.get("liquidity"),
            new_data.get("liquidity"),
        )

        if liquidity_change is not None and abs(liquidity_change) >= LIQUIDITY_ALERT:
            alerts.append(
                f"💧 {symbol}\n"
                f"Płynność: {liquidity_change:+.2f}%"
            )

    if not alerts:
        return None

    return "\n\n".join(alerts)
