"""
Crypto Alerts
Storage v1.0
"""

import json
import os

from config import STORAGE_FILE


def load_storage():
    """
    Wczytuje storage.json.
    """

    if not os.path.exists(STORAGE_FILE):
        return {}

    try:
        with open(STORAGE_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    except Exception:
        return {}


def save_storage(data):
    """
    Zapisuje dane do storage.json.
    """

    with open(STORAGE_FILE, "w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False
        )


def get_token(symbol):
    """
    Pobiera dane tokena.
    """

    data = load_storage()

    return data.get(symbol, {})


def update_token(symbol, values):
    """
    Aktualizuje dane tokena.
    """

    data = load_storage()

    data[symbol] = values

    save_storage(data)


def clear_storage():
    """
    Czyści storage.
    """

    save_storage({})
