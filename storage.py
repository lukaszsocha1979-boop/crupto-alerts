import json
import os

FILE = "sent.json"

def load():
    if not os.path.exists(FILE):
        return []

    with open(FILE, "r") as f:
        return json.load(f)


def save(data):
    with open(FILE, "w") as f:
        json.dump(data, f)


def already_sent(link):
    data = load()
    return link in data


def mark_sent(link):
    data = load()

    if link not in data:
        data.append(link)

    save(data)
