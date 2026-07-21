import json
import os

FILE = "sent.json"


def load():
    if os.path.exists(FILE):
        with open(FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save(data):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f)


def already_sent(link):
    return link in load()


def save_sent(link):
    data = load()

    if link not in data:
        data.append(link)
        save(data)
