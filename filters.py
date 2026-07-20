from config import KEYWORDS, HIGH_PRIORITY


def analyze(news):
    alerts = []

    for item in news:
        title = item["title"].lower()

        project = None

        for token, words in KEYWORDS.items():
            if any(w in title for w in words):
                project = token
                break

        if not project:
            continue

        level = "🔴 NISKA"

        if any(w in title for w in HIGH_PRIORITY):
            level = "🟢 WYSOKA"
        elif "update" in title or "launch" in title:
            level = "🟡 ŚREDNIA"

        alerts.append({
            "project": project,
            "level": level,
            "title": item["title"],
            "link": item["link"]
        })

    return alerts
