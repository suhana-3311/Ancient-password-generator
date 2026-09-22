
from flask import Flask, render_template, request, jsonify
import secrets
import string
import re

app = Flask(__name__)

# Simplified Roman-transliteration Katapayadi mapping used for this educational demo.
# Traditional Katapayadi assigns consonants to digits 0-9 and numbers are commonly
# interpreted right-to-left. The application documents this convention in the UI.
KATAPAYADI = {
    "kh": 2, "gh": 4, "ng": 5, "ch": 7, "jh": 9, "ny": 0,
    "th": 7, "dh": 9, "ph": 2, "bh": 4,
    "k": 1, "g": 3, "c": 6, "j": 8,
    "t": 6, "d": 8, "n": 0,
    "p": 1, "b": 3, "m": 5,
    "y": 1, "r": 2, "l": 3, "v": 4,
    "sh": 5, "s": 7, "h": 8,
}

SANSKRIT_WORDS = {
    "AGNI": "Fire",
    "SURYA": "Sun",
    "VAYU": "Air / Wind",
    "JAL": "Water",
    "PRITHVI": "Earth",
    "VIDYA": "Knowledge",
    "SHAKTI": "Power / Energy",
    "MANTRA": "Sacred utterance",
}

BHUTA_SANKHYA = {
    "Eyes": 2,
    "Hands": 2,
    "Vedas": 4,
    "Seasons": 6,
    "Rasas": 6,
    "Navagraha": 9,
    "Planets": 9,
}

def katapayadi_value(word: str) -> str:
    """
    Educational transliteration parser.
    Multi-letter consonants are matched before single letters.
    Vowels are ignored for the consonant-to-number step.
    """
    s = re.sub(r"[^a-z]", "", word.lower())
    values = []
    i = 0
    while i < len(s):
        pair = s[i:i+2]
        if pair in KATAPAYADI:
            values.append(str(KATAPAYADI[pair]))
            i += 2
        elif s[i] in KATAPAYADI:
            values.append(str(KATAPAYADI[s[i]]))
            i += 1
        else:
            i += 1

    # Katapayadi numerals are conventionally read from right to left.
    return "".join(reversed(values)) if values else "0"

def secure_random_chars(length: int, use_upper=True, use_lower=True,
                        use_digits=True, use_symbols=True) -> str:
    pools = []
    if use_upper:
        pools.append(string.ascii_uppercase)
    if use_lower:
        pools.append(string.ascii_lowercase)
    if use_digits:
        pools.append(string.digits)
    if use_symbols:
        pools.append("!@#$%^&*()-_=+[]{}?")

    if not pools:
        pools = [string.ascii_letters + string.digits]

    chars = [secrets.choice(pool) for pool in pools]
    all_chars = "".join(pools)
    while len(chars) < length:
        chars.append(secrets.choice(all_chars))
    secrets.SystemRandom().shuffle(chars)
    return "".join(chars[:length])

def strength(password: str):
    score = 0
    if len(password) >= 8: score += 1
    if len(password) >= 12: score += 1
    if len(password) >= 16: score += 1
    if re.search(r"[A-Z]", password): score += 1
    if re.search(r"[a-z]", password): score += 1
    if re.search(r"\d", password): score += 1
    if re.search(r"[^A-Za-z0-9]", password): score += 1

    if score <= 3:
        label = "Weak"
    elif score <= 5:
        label = "Medium"
    else:
        label = "Strong"

    checks = {
        "Length ≥ 12": len(password) >= 12,
        "Uppercase": bool(re.search(r"[A-Z]", password)),
        "Lowercase": bool(re.search(r"[a-z]", password)),
        "Number": bool(re.search(r"\d", password)),
        "Special character": bool(re.search(r"[^A-Za-z0-9]", password)),
    }
    return label, score, checks

@app.route("/")
def index():
    return render_template(
        "index.html",
        sanskrit_words=SANSKRIT_WORDS,
        bhuta_sankhya=BHUTA_SANKHYA
    )

@app.post("/generate")
def generate():
    data = request.get_json(silent=True) or {}
    word = str(data.get("word", "AGNI")).upper().strip()
    bhuta_name = str(data.get("bhuta", "Vedas"))
    length = max(8, min(int(data.get("length", 16)), 32))

    kat = katapayadi_value(word)
    bhuta = BHUTA_SANKHYA.get(bhuta_name, 4)

    # Ancient-system outputs are used as a thematic seed/component.
    # The unpredictable part comes from secrets.SystemRandom / secrets.choice.
    prefix = word[:2].capitalize() if word else "Ak"
    thematic = f"{prefix}{kat}{bhuta}"
    remaining = max(4, length - len(thematic))
    random_part = secure_random_chars(
        remaining, use_upper=True, use_lower=True,
        use_digits=True, use_symbols=True
    )

    password = thematic + random_part
    # Shuffle the complete result so the thematic part isn't always at the front.
    chars = list(password)
    secrets.SystemRandom().shuffle(chars)
    password = "".join(chars)[:length]

    label, score, checks = strength(password)

    return jsonify({
        "password": password,
        "word": word,
        "meaning": SANSKRIT_WORDS.get(word, "Custom Sanskrit-inspired input"),
        "katapayadi": kat,
        "bhuta_name": bhuta_name,
        "bhuta_value": bhuta,
        "strength": label,
        "score": score,
        "checks": checks,
    })

if __name__ == "__main__":
    app.run(debug=True)
