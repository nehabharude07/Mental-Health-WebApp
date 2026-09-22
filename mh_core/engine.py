"""
mh_core.engine
--------------
Hybrid prediction engine.

Primary   : rule-based clinical scoring (scoring.py) - har naye input par kaam karta hai
Secondary : trained ML model (train_model.py) - sirf reference, agar woh
            cross-validation me reliable nikla ho

Do input modes:
  * questionnaire - user 14 sawaalon ke jawab deta hai
  * free text     - user apni bhasha me likhta hai, text_analysis symptoms nikaalta hai

Design reason: Deepression.csv me identical symptom profiles ke alag-alag labels
hain, isliye ML accuracy ceiling ~50% hai. Aise model ko headline result banana
users ko galat jaankari dega. Isliye rule engine primary hai.
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, Any, Optional

from . import i18n
from .scoring import score_answers, answers_to_csv_scale, STATES
from .text_analysis import analyse, word_count, MIN_WORDS

MODEL_PATH = Path(__file__).resolve().parent.parent / "model" / "model_bundle.joblib"

_bundle: Optional[dict] = None
_load_error: str = ""


def load_model() -> Optional[dict]:
    """Model bundle ek hi baar load hota hai (lazy, cached)."""
    global _bundle, _load_error
    if _bundle is not None or _load_error:
        return _bundle
    try:
        import joblib
        if not MODEL_PATH.exists():
            _load_error = "model_bundle.joblib not found - run `python train_model.py` first."
            return None
        _bundle = joblib.load(MODEL_PATH)
        return _bundle
    except Exception as exc:  # noqa: BLE001
        _load_error = f"Model load failed: {exc}"
        return None


def model_status() -> Dict[str, Any]:
    bundle = load_model()
    if bundle is None:
        return {"available": False, "error": _load_error}
    return {
        "available": True,
        "reliable": bundle.get("reliable", False),
        "model_name": bundle.get("model_name"),
        "cv_accuracy": bundle.get("cv_accuracy"),
        "holdout_accuracy": bundle.get("holdout_accuracy"),
        "baseline_accuracy": bundle.get("baseline_accuracy"),
        "accuracy_ceiling": bundle.get("accuracy_ceiling"),
        "n_training_rows": bundle.get("n_training_rows"),
    }


def _ml_opinion(answers: Dict[str, int], lang: str) -> Optional[Dict[str, Any]]:
    bundle = load_model()
    if bundle is None:
        return None
    try:
        mapped = answers_to_csv_scale(answers)
        row = [[mapped[col] for col in bundle["feature_columns"]]]
        pipe = bundle["pipeline"]
        pred = str(pipe.predict(row)[0])

        probabilities = []
        if hasattr(pipe, "predict_proba"):
            proba = pipe.predict_proba(row)[0]
            by_class = {str(c): float(p) * 100 for c, p in zip(pipe.classes_, proba)}
            probabilities = [
                {"state": s, "label": i18n.state_text(s, lang),
                 "value": round(by_class.get(s, 0.0), 1)}
                for s in STATES
            ]
        return {
            "prediction": pred,
            "prediction_label": i18n.state_text(pred, lang),
            "probabilities": probabilities,
            "reliable": bool(bundle.get("reliable", False)),
            "cv_accuracy": round(float(bundle.get("cv_accuracy", 0)) * 100, 1),
            "model_name": bundle.get("model_name"),
        }
    except Exception:  # noqa: BLE001
        return None


def predict(answers: Dict[str, int], lang: str = i18n.DEFAULT_LANG,
            partial: bool = False) -> Dict[str, Any]:
    """Validated answers (0-3 per item) -> poora result dict."""
    lang = i18n.normalise_lang(lang)
    result = score_answers(answers, lang, partial=partial).to_dict()

    ml = _ml_opinion(answers, lang)
    result["ml"] = ml
    result["source"] = "questionnaire"
    result["engine"] = "clinical_scoring"

    if ml and ml["reliable"]:
        result["engine"] = "clinical_scoring + ml"
        result["agreement"] = (ml["prediction"] == result["state"])
    else:
        result["agreement"] = None

    result["disclaimer"] = i18n.t(lang, "disclaimer")
    result["answers"] = answers
    return result


class TextTooShort(ValueError):
    pass


def predict_from_text(text: str, lang: str = i18n.DEFAULT_LANG) -> Dict[str, Any]:
    """
    Free text -> symptom extraction -> same scoring engine.

    User kisi bhi bhasha (en / hi / mr / hinglish) me, ya mila-jula, likh sakta hai -
    analyser saari languages ke patterns ek saath dekhta hai.
    """
    lang = i18n.normalise_lang(lang)

    if word_count(text) < MIN_WORDS:
        raise TextTooShort(i18n.t(lang, "err_short"))

    extraction = analyse(text)
    result = predict(extraction["answers"], lang, partial=True)
    result["source"] = "free_text"

    # detected symptoms ko user ki bhasha me label karo
    result["detected"] = [
        {
            "key": d["key"],
            "label": i18n.item_text(d["key"], lang),
            "value": d["value"],
            "value_label": i18n.option_text(d["value"], lang),
            "evidence": d["evidence"],
            "critical": d["critical"],
        }
        for d in extraction["detected"]
    ]
    result["text_meta"] = extraction["meta"]
    result["user_text"] = text
    return result
