"""
app.py  (UPGRADED - v2)
=======================

Features:
  * 14-item validated-style questionnaire (compact layout)
  * 4 languages: English, Hindi, Marathi, Hinglish (?lang= ya switcher se)
  * Free-text mode: user apni bhasha me likhe, engine symptoms extract kare
  * 4-level severity output + per-domain breakdown + probability view
  * Safety pathway with India helplines
  * JSON API

Run:
    python app.py   ->  http://127.0.0.1:5000
"""

from __future__ import annotations

import os

from flask import Flask, render_template, request, jsonify, redirect, url_for, make_response

from mh_core import i18n
from mh_core.scoring import form_schema, option_schema, validate_answers, ValidationError, STATES
from mh_core.engine import predict, predict_from_text, model_status, TextTooShort

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False
LANG_COOKIE = "mh_lang"


def current_lang() -> str:
    """Priority: ?lang= query -> form field -> cookie -> default."""
    return i18n.normalise_lang(
        request.args.get("lang")
        or request.form.get("lang")
        or request.cookies.get(LANG_COOKIE)
    )


def page(lang: str, **extra):
    """Common template context."""
    ctx = {
        "lang": lang,
        "languages": i18n.LANGUAGES,
        "T": {k: i18n.t(lang, k) for k in i18n.UI["en"].keys()},
        "items": form_schema(lang),
        "options": option_schema(lang),
        "states": [{"key": s, "label": i18n.state_text(s, lang)} for s in STATES],
        "model": model_status(),
        "min_words": 15,
    }
    ctx.update(extra)
    response = make_response(render_template("index.html", **ctx))
    response.set_cookie(LANG_COOKIE, lang, max_age=60 * 60 * 24 * 365, samesite="Lax")
    return response


# ---------------------------------------------------------------- pages ---

@app.route("/")
def home():
    return page(current_lang(), tab="quiz")


@app.route("/lang/<code>")
def set_lang(code):
    resp = redirect(url_for("home"))
    resp.set_cookie(LANG_COOKIE, i18n.normalise_lang(code),
                    max_age=60 * 60 * 24 * 365, samesite="Lax")
    return resp


@app.route("/predict", methods=["POST"])
def predict_form():
    lang = current_lang()
    try:
        answers = validate_answers(request.form.to_dict(), lang)
    except ValidationError as exc:
        return page(lang, tab="quiz", error=str(exc),
                    submitted=request.form.to_dict()), 400

    return page(lang, tab="quiz", result=predict(answers, lang),
                submitted=request.form.to_dict())


@app.route("/describe", methods=["POST"])
def describe():
    lang = current_lang()
    text = (request.form.get("description") or "").strip()
    try:
        result = predict_from_text(text, lang)
    except TextTooShort as exc:
        return page(lang, tab="text", error=str(exc), user_text=text), 400

    return page(lang, tab="text", result=result, user_text=text)


# ------------------------------------------------------------------ api ---

@app.route("/api/predict", methods=["POST"])
def predict_api():
    """POST JSON: {"lang": "hi", "sleep": 2, "appetite": 1, ...} (saare 14 keys)"""
    payload = request.get_json(silent=True) or {}
    lang = i18n.normalise_lang(payload.get("lang"))
    try:
        answers = validate_answers(payload, lang)
    except ValidationError as exc:
        return jsonify({"ok": False, "error": str(exc)}), 400
    return jsonify({"ok": True, "result": predict(answers, lang)})


@app.route("/api/describe", methods=["POST"])
def describe_api():
    """POST JSON: {"text": "...", "lang": "mr"}"""
    payload = request.get_json(silent=True) or {}
    lang = i18n.normalise_lang(payload.get("lang"))
    try:
        result = predict_from_text(payload.get("text", ""), lang)
    except TextTooShort as exc:
        return jsonify({"ok": False, "error": str(exc)}), 400
    return jsonify({"ok": True, "result": result})


@app.route("/api/schema")
def schema_api():
    lang = current_lang()
    return jsonify({
        "lang": lang,
        "languages": i18n.LANGUAGES,
        "items": form_schema(lang),
        "options": option_schema(lang),
        "states": STATES,
    })


@app.route("/api/model")
def model_api():
    return jsonify(model_status())


@app.route("/health")
def health():
    return jsonify({"status": "ok",
                    "model_loaded": model_status().get("available", False)})


# --------------------------------------------------------------- errors ---

@app.errorhandler(404)
def not_found(_):
    lang = current_lang()
    msg = {"en": "Page not found. Back to home.",
           "hi": "पेज नहीं मिला। होम पर वापस आ गए हैं।",
           "mr": "पृष्ठ सापडले नाही. मुख्यपृष्ठावर परत आलो आहोत.",
           "hinglish": "Page nahi mila. Home par wapas aa gaye hain."}
    return page(lang, tab="quiz", error=msg[lang]), 404


@app.errorhandler(500)
def server_error(_):
    lang = current_lang()
    msg = {"en": "Something went wrong technically. Please try again.",
           "hi": "कुछ तकनीकी समस्या आ गई। कृपया दोबारा कोशिश करें।",
           "mr": "काहीतरी तांत्रिक अडचण आली. कृपया पुन्हा प्रयत्न करा.",
           "hinglish": "Kuch technical problem aa gayi. Dobara try karein."}
    return page(lang, tab="quiz", error=msg[lang]), 500


if __name__ == "__main__":
    print("\n  Mental Health Screening System")
    print("  http://127.0.0.1:5151")
    print("  Languages: English / हिन्दी / मराठी / Hinglish\n")
    status = model_status()
    if not status.get("available"):
        print(f"  [!] {status.get('error')}")
        print("      App will still run - the rule-based engine is independent.\n")
    app.run(host="127.0.0.1", port=5151,
            debug=os.environ.get("FLASK_DEBUG", "1") == "1")
