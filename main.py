PRICE_ALERT = 10      # %
VOLUME_ALERT = 100    # %


def check_alert(symbol, old_data, new_data):

    if old_data is None:
        return None

    alerts = []

    old_price = old_data["price"]
    new_price = new_data["price"]

    if old_price > 0:

        change = ((new_price - old_price) / old_price) * 100

        if abs(change) >= PRICE_ALERT:

            icon = "🚀" if change > 0 else "📉"

            alerts.append(
                f"{icon} {symbol}\n"
                f"Cena zmieniła się o {change:.2f}%\n"
                f"${old_price:.8f} → ${new_price:.8f}"
            )

    old_volume = old_data["volume24h"]
    new_volume = new_data["volume24h"]

    if old_volume > 0:

        volume_change = ((new_volume - old_volume) / old_volume) * 100

        if volume_change >= VOLUME_ALERT:

            alerts.append(
                f"📊 {symbol}\n"
                f"Wolumen wzrósł o {volume_change:.2f}%"
            )

    if len(alerts) == 0:
        return None

    return "\n\n".join(alerts)
