
# Ancient Knowledge System Inspired Secure Password Generator

## Stack
- Python
- Flask
- HTML
- CSS
- Bootstrap 5
- Bootstrap Icons
- JavaScript

## Run locally

1. Open terminal in this folder.
2. Create/activate a virtual environment if desired.
3. Install Flask:

```bash
pip install flask
```

4. Start the application:

```bash
python app.py
```

5. Open:

```text
http://127.0.0.1:5000
```

## Project logic

Sanskrit-inspired word
→ Katapayadi numerical component
→ Bhuta Sankhya numerical component
→ Python `secrets` randomization
→ shuffled password
→ strength evaluation

## Important academic/security note

This is an educational demonstration for the Ancient Knowledge System project. Katapayadi and Bhuta Sankhya are used as thematic/meaningful inputs; they are not cryptographic algorithms. The unpredictable part is generated with Python's `secrets` module.

The Roman-transliteration Katapayadi mapping is explicitly documented in the interface and should be described as a simplified educational implementation. Traditional sources can differ in transliteration, orthography and conventions.

## Main files

- `app.py` — Flask backend, mappings, generation and strength logic
- `templates/index.html` — complete website
- `static/css/style.css` — responsive styling and animations
- `static/js/app.js` — live generation, copy button and scroll animations
- `static/images/*.svg` — topic-specific original illustrations
