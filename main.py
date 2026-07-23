# Alerts module placeholder
market = get_market()

alerts = check_alerts(market)

if alerts:
    send_message(build_message(alerts))

if should_check_news():
    news = check_news()

    if news:
        send_message(build_news_message(news))
