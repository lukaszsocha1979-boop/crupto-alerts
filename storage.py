
"""
Crypto Alerts
Storage v1.2
Bezpieczny odczyt i zapis historii alertów.
"""

import json
import os

from config import STORAGE_FILE


def load_storage():
    """Wczytuje dane z storage.json."""

    if not os.path.exists(STORAGE_FILE):
        return {}

    try:
        with open(STORAGE_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, dict):
            raise ValueError("Storage nie zawiera słownika JSON")

        return data

    except Exception as e:
        print(f"[STORAGE] Błąd odczytu: {e}")
        raise RuntimeError(
            "Nie można odczytać storage.json. "
            "Przerywam działanie, aby nie utracić historii."
        ) from e


def save_storage(data):
    """Zapisuje dane bezpiecznie przez plik tymczasowy."""

    if not isinstance(data, dict):
        raise ValueError("Dane storage muszą być słownikiem")

    temp_file = STORAGE_FILE + ".tmp"

    try:
        with open(temp_file, "w", encoding="utf-8") as file:
            json.dump(
                data,
                file,
                indent=4,
                ensure_ascii=False
            )
            file.flush()
            os.fsync(file.fileno())

        os.replace(temp_file, STORAGE_FILE)

    except Exception as e:
        print(f"[STORAGE] Błąd zapisu: {e}")

        if os.path.exists(temp_file):
            try:
                os.remove(temp_file)
            except OSError:
                pass

        raise


def get_token(symbol):
    """Zwraca dane zapisane dla tokena."""

    data = load_storage()
    return data.get(symbol, {})


def update_token(symbol, values):
    """Aktualizuje dane tokena."""

    data = load_storage()
    data[symbol] = values
    save_storage(data)


def remove_token(symbol):
    """Usuwa token ze storage."""

    data = load_storage()

    if symbol in data:
        del data[symbol]
        save_storage(data)


def clear_storage():
    """Czyści cały storage."""

    save_storage({})
