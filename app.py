from flask import Flask, render_template, redirect
import json
import os

app = Flask(__name__)

# ======================
# Language Configuration
# ======================
ALLOWED_LANGS = ["EN", "TH", "JP", "ZH"]
DEFAULT_LANG = "EN"
TRANSLATION_DIR = "translations"


def validate_lang(lang):
    """Validate language from URL"""
    if lang and lang.upper() in ALLOWED_LANGS:
        return lang.upper()
    return DEFAULT_LANG


def load_translation(lang):
    """Load JSON translation file with fallback"""
    lang = validate_lang(lang)
    path = os.path.join(TRANSLATION_DIR, f"{lang.lower()}.json")
    fallback = os.path.join(TRANSLATION_DIR, "en.json")

    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        with open(fallback, encoding="utf-8") as f:
            return json.load(f)


# ======================
# Routes
# ======================
@app.route("/")
def redirect_home():
    return redirect(f"/{DEFAULT_LANG}/")


@app.route("/<lang>/")
def home(lang):
    lang = validate_lang(lang)
    text = load_translation(lang)
    return render_template("index.html", lang=lang, text=text)


@app.route("/<lang>/start")
def start(lang):
    lang = validate_lang(lang)
    text = load_translation(lang)
    return render_template("start.html", lang=lang, text=text)


@app.route("/<lang>/result")
def result(lang):
    lang = validate_lang(lang)
    text = load_translation(lang)
    return render_template("result.html", lang=lang, text=text)


@app.route("/<lang>/about")
def about(lang):
    lang = validate_lang(lang)
    text = load_translation(lang)
    return render_template("about.html", lang=lang, text=text)


@app.route("/<lang>/organizer")
def organizer(lang):
    lang = validate_lang(lang)
    text = load_translation(lang)
    return render_template("organizer.html", lang=lang, text=text)


@app.route("/<lang>/contact")
def contact(lang):
    lang = validate_lang(lang)
    text = load_translation(lang)
    return render_template("contact.html", lang=lang, text=text)


# ======================
# Run
# ======================
if __name__ == "__main__":
    app.run(debug=True)
