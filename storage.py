"""
Crypto Alerts
Storage v1.1
"""

import json
import os

from config import STORAGE_FILE


def load_storage():
    """
    Wczytuje dane z storage.json.
    """

    if not os.path.exists(STORAGE_FILE):
        return {}

    try:
        with open(STORAGE_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    except Exception as e:
        print(f"[STORAGE] Błąd odczytu: {e}")
        return {}


def save_storage(data):
    """
    Zapisuje dane do storage.json.
    """

    try:
        with open(STORAGE_FILE, "w", encoding="utf-8") as file:
            json.dump(
                data,
                file,
                indent=4,
                ensure_ascii=False
            )

    except Exception as e:
        print(f"[STORAGE] Błąd zapisu: {e}")


def get_token(symbol):
    """
    Zwraca dane zapisane dla tokena.
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


def remove_token(symbol):
    """
    Usuwa token ze storage.
    """

    data = load_storage()

    if symbol in data:
        del data[symbol]
        save_storage(data)


def clear_storage():
    """
    Czyści cały storage.
    """

    save_storage({})
