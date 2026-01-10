import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

def load_language(lang="en"):
    path = os.path.join(BASE_DIR, "translations", f"{lang}.json")
    fallback = os.path.join(BASE_DIR, "translations", "en.json")

    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        with open(fallback, encoding="utf-8") as f:
            return json.load(f)
