from flask import Flask, render_template, request, redirect
from translations import translations

app = Flask(__name__)

def get_lang():
    lang = request.args.get("lang", "EN")
    return lang if lang in translations else "EN"

ALLOWED_LANGS = ["EN", "TH", "JP", "ZH"]
def validate_lang(lang):
    return lang.upper() if lang and lang.upper() in ALLOWED_LANGS else "EN"

# Home page
@app.route('/<lang>/')
def home(lang):
    lang = validate_lang(lang)
    return render_template("index.html", lang=lang, text=translations[lang])

# Start page
@app.route('/<lang>/start')
def start(lang):
    lang = validate_lang(lang)
    return render_template('start.html', lang=lang, text=translations[lang])

# Result page
@app.route('/<lang>/result')
def result(lang):
    lang = validate_lang(lang)
    return render_template('result.html', lang=lang, text=translations[lang])

# About page
@app.route('/<lang>/about')
def about(lang):
    lang = validate_lang(lang)
    return render_template('about.html', lang=lang, text=translations[lang])

# Organizer page
@app.route('/<lang>/organizer')
def organizer(lang):
    lang = validate_lang(lang)
    return render_template('organizer.html', lang=lang, text=translations[lang])

# Contact page
@app.route('/<lang>/contact')
def contact(lang):
    lang = validate_lang(lang)
    return render_template('contact.html', lang=lang, text=translations[lang])

@app.route('/')
def redirect_home():
    # Use query parameter if present, otherwise default to EN
    lang = request.args.get('lang', 'EN').upper()
    if lang not in ALLOWED_LANGS:
        lang = 'EN'
    return redirect(f'/{lang}/')

if __name__ == '__main__':
    app.run(debug=True)
