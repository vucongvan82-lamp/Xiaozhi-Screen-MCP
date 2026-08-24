import json
import os
import threading

BASE_DIR = os.path.dirname(os.path.abspath(https://github.com/vucongvan82-lamp/Xiaozhi-Screen-MCP/blob/main/data/locations.json))
DATA_DIR = os.path.join(BASE_DIR, "data")
DATA_FILE = os.path.join(DATA_DIR, "locations.json")

_lock = threading.Lock()


def _load_locations():
    os.makedirs(DATA_DIR, exist_ok=True)

    if not os.path.exists(DATA_FILE):
        return {}

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    except Exception as e:
        print("LOCATION LOAD ERROR =", repr(e))
        return {}


def _save_locations(data):
    os.makedirs(DATA_DIR, exist_ok=True)

    temp_file = DATA_FILE + ".tmp"

    with open(temp_file, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=2
        )

    os.replace(temp_file, DATA_FILE)


def save_location(esp_id, province):
    with _lock:

        locations = _load_locations()

        locations[esp_id] = {
            "province": province
        }

        _save_locations(locations)

        print("========== LOCATION STORE ==========")
        print("DEVICE   =", esp_id)
        print("PROVINCE =", province)

        return True


def get_location(esp_id):

    with _lock:

        locations = _load_locations()

        item = locations.get(esp_id)

        if item is None:
            return None

        return item.get("province")


def delete_location(esp_id):

    with _lock:

        locations = _load_locations()

        if esp_id in locations:
            del locations[esp_id]
            _save_locations(locations)

        return True
