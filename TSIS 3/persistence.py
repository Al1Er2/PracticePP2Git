import json
import os

LEADERBOARD_FILE = "leaderboard.json"
SETTINGS_FILE = "settings.json"

DEFAULT_SETTINGS = {
    "sound": True,
    "car_color": "blue",
    "difficulty": "normal"
}

def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS.copy()

    try:
        with open(SETTINGS_FILE, "r") as file:
            return json.load(file)
    except:
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS.copy()

def save_settings(settings):
    with open(SETTINGS_FILE, "w") as file:
        json.dump(settings, file, indent=4)

def load_leaderboard():
    if not os.path.exists(LEADERBOARD_FILE):
        save_leaderboard([])
        return []

    try:
        with open(LEADERBOARD_FILE, "r") as file:
            return json.load(file)
    except:
        save_leaderboard([])
        return []

def save_leaderboard(data):
    with open(LEADERBOARD_FILE, "w") as file:
        json.dump(data, file, indent=4)

def add_score(name, score, distance, coins):
    data = load_leaderboard()

    data.append({
        "name": name,
        "score": score,
        "distance": int(distance),
        "coins": coins
    })

    data = sorted(data, key=lambda x: x["score"], reverse=True)[:10]
    save_leaderboard(data)