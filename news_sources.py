import feedparser

RSS_FEEDS = [
    "https://www.coindesk.com/arc/outboundfeeds/rss/",
    "https://cointelegraph.com/rss",
]

def get_news():
    news = []

    for feed in RSS_FEEDS:
        try:
            data = feedparser.parse(feed)
            for entry in data.entries[:10]:
                news.append({
                    "title": entry.title,
                    "link": entry.link,
                    "published": getattr(entry, "published", "")
                })
        except Exception as e:
            print(e)

    return news
