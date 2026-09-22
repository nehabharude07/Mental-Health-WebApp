"""
mh_core.scoring
---------------
Rule-based symptom severity engine.

Yeh module PHQ-9 / GAD-7 jaise validated screening instruments ke structure par
based hai. Har symptom item 0-3 scale par hai:

    0 = Not at all        1 = Several days
    2 = More than half    3 = Nearly every day

Ye engine deterministic hai - isliye ye KISI BHI naye input par sahi tarah
kaam karta hai, chahe woh training data me kabhi aaya ho ya nahi.
Yahi cheez purane model.pkl me missing thi.

Saara user-facing text mh_core/i18n.py me hai (English / Hindi / Marathi /
Hinglish). Yeh module sirf logic rakhta hai.

IMPORTANT: Yeh ek screening / self-awareness tool hai, medical diagnosis NAHI.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Dict, List, Any

from . import i18n


# --------------------------------------------------------------------------
# 1. Questionnaire definition
# --------------------------------------------------------------------------

@dataclass(frozen=True)
class Item:
    key: str            # form field name
    csv_column: str     # matching column in Deepression.csv
    domain: str         # symptom cluster
    weight: float = 1.0
    critical: bool = False  # triggers safety pathway


ITEMS: List[Item] = [
    Item("sleep",             "Sleep",             "somatic",   1.0),
    Item("appetite",          "Appetite",          "somatic",   1.0),
    Item("interest",          "Interest",          "core",      1.6),
    Item("fatigue",           "Fatigue",           "somatic",   1.1),
    Item("worthlessness",     "Worthlessness",     "cognitive", 1.5),
    Item("concentration",     "Concentration",     "cognitive", 1.2),
    Item("agitation",         "Agitation",         "somatic",   1.0),
    Item("suicidal_ideation", "Suicidal Ideation", "risk",      2.2, critical=True),
    Item("sleep_disturbance", "Sleep Disturbance", "somatic",   1.0),
    Item("aggression",        "Aggression",        "affective", 1.0),
    Item("panic_attacks",     "Panic Attacks",     "anxiety",   1.3),
    Item("hopelessness",      "Hopelessness",      "core",      1.7),
    Item("restlessness",      "Restlessness",      "anxiety",   1.0),
    Item("low_energy",        "Low Energy",        "somatic",   1.1),
]

ITEM_BY_KEY: Dict[str, Item] = {i.key: i for i in ITEMS}

MIN_SCORE, MAX_SCORE = 0, 3
N_ITEMS = len(ITEMS)
RAW_MAX = N_ITEMS * MAX_SCORE          # 42
WEIGHTED_MAX = sum(i.weight for i in ITEMS) * MAX_SCORE

STATES = ["No depression", "Mild", "Moderate", "Severe"]

# Severity bands on the 0-100 normalised weighted score.
# Proportional to PHQ-9 cut-offs (5 / 10 / 20 on a 0-27 scale).
BANDS = [
    (0.0, 16.0, "No depression"),
    (16.0, 34.0, "Mild"),
    (34.0, 60.0, "Moderate"),
    (60.0, 100.1, "Severe"),
]


# --------------------------------------------------------------------------
# 2. Input validation
# --------------------------------------------------------------------------

class ValidationError(ValueError):
    """Raised when submitted answers are missing or out of range."""


_ERR = {
    "missing": {
        "en": "These questions are unanswered: ",
        "hi": "इन सवालों का जवाब नहीं दिया गया: ",
        "mr": "या प्रश्नांची उत्तरे दिलेली नाहीत: ",
        "hinglish": "In sawaalon ka jawab missing hai: ",
    },
    "range": {
        "en": "These answers must be between 0 and 3: ",
        "hi": "इन सवालों की वैल्यू 0-3 के बीच होनी चाहिए: ",
        "mr": "या प्रश्नांची मूल्ये 0-3 दरम्यान असावीत: ",
        "hinglish": "In sawaalon ki value 0-3 ke beech honi chahiye: ",
    },
}


def validate_answers(raw: Dict[str, Any], lang: str = i18n.DEFAULT_LANG) -> Dict[str, int]:
    """Har item ko 0-3 int me convert karta hai; error message user ki bhasha me."""
    lang = i18n.normalise_lang(lang)
    cleaned: Dict[str, int] = {}
    missing: List[str] = []
    bad: List[str] = []

    for item in ITEMS:
        label = i18n.item_text(item.key, lang)
        if item.key not in raw or raw[item.key] in (None, ""):
            missing.append(label)
            continue
        try:
            value = int(float(raw[item.key]))
        except (TypeError, ValueError):
            bad.append(label)
            continue
        if not (MIN_SCORE <= value <= MAX_SCORE):
            bad.append(label)
            continue
        cleaned[item.key] = value

    def _join(items: List[str]) -> str:
        return ", ".join(items[:3]) + (" ..." if len(items) > 3 else "")

    if missing:
        raise ValidationError(_ERR["missing"][lang] + _join(missing))
    if bad:
        raise ValidationError(_ERR["range"][lang] + _join(bad))
    return cleaned


# --------------------------------------------------------------------------
# 3. Scoring
# --------------------------------------------------------------------------

@dataclass
class ScoreResult:
    raw_score: int
    raw_max: int
    normalised: float                   # 0-100
    state: str                          # canonical English key
    state_label: str                    # translated for display
    band_index: int
    headline: str
    detail: str
    domain_scores: List[Dict[str, Any]]
    top_symptoms: List[Dict[str, Any]]
    crisis: bool
    crisis_reason: str = ""
    crisis_resources: List[Dict[str, str]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def _band_for(normalised: float) -> tuple:
    for idx, (lo, hi, name) in enumerate(BANDS):
        if lo <= normalised < hi:
            return name, idx
    return BANDS[-1][2], len(BANDS) - 1


# Free-text mode me user sirf un symptoms ka zikr karta hai jo use pareshan kar
# rahe hain - baaki 14 me se jo mention nahi hue woh "0" nahi maane ja sakte.
# Isliye partial mode me denominator sirf mentioned symptoms par banta hai,
# par ek floor ke saath (warna 1 symptom = 100% ho jaata).
PARTIAL_FLOOR = 0.45


def score_answers(answers: Dict[str, int], lang: str = i18n.DEFAULT_LANG,
                  partial: bool = False) -> ScoreResult:
    """
    Validated answers -> severity band + breakdown.
    Deterministic: har naya combination sahi handle hota hai.

    partial=True  -> free-text mode ke liye calibration (upar dekhein)
    """
    lang = i18n.normalise_lang(lang)

    raw = sum(answers[i.key] for i in ITEMS)
    weighted = sum(answers[i.key] * i.weight for i in ITEMS)

    if partial:
        mentioned = sum(i.weight for i in ITEMS if answers.get(i.key, 0) > 0)
        total_weight = sum(i.weight for i in ITEMS)
        denominator = MAX_SCORE * max(mentioned, PARTIAL_FLOOR * total_weight)
    else:
        denominator = WEIGHTED_MAX

    normalised = round(100.0 * weighted / denominator, 1) if denominator else 0.0
    normalised = min(normalised, 100.0)

    state, band_index = _band_for(normalised)

    # --- safety escalation -------------------------------------------------
    crisis = False
    crisis_reason = ""
    if answers.get("suicidal_ideation", 0) >= 1:
        crisis = True
        crisis_reason = i18n.crisis_reason(lang)
        if band_index < 2:  # a critical item pushes result to at least Moderate
            state, band_index = "Moderate", 2

    # --- per-domain breakdown ---------------------------------------------
    totals: Dict[str, List[float]] = {}
    for item in ITEMS:
        got, possible = totals.get(item.domain, (0.0, 0.0))
        totals[item.domain] = [
            got + answers[item.key] * item.weight,
            possible + MAX_SCORE * item.weight,
        ]
    domain_scores = [
        {
            "domain": d,
            "label": i18n.domain_text(d, lang),
            "value": round(100.0 * got / possible, 1) if possible else 0.0,
        }
        for d, (got, possible) in totals.items()
    ]
    domain_scores.sort(key=lambda x: x["value"], reverse=True)

    # --- most prominent symptoms ------------------------------------------
    ranked = sorted(
        ITEMS, key=lambda i: (answers[i.key] * i.weight, answers[i.key]), reverse=True
    )
    top_symptoms = [
        {
            "key": i.key,
            "label": i18n.item_text(i.key, lang),
            "value": answers[i.key],
            "domain": i18n.domain_text(i.domain, lang),
        }
        for i in ranked if answers[i.key] >= 2
    ][:5]

    advice = i18n.advice_text(state, lang)
    return ScoreResult(
        raw_score=raw,
        raw_max=RAW_MAX,
        normalised=normalised,
        state=state,
        state_label=i18n.state_text(state, lang),
        band_index=band_index,
        headline=advice["headline"],
        detail=advice["detail"],
        domain_scores=domain_scores,
        top_symptoms=top_symptoms,
        crisis=crisis,
        crisis_reason=crisis_reason,
        crisis_resources=i18n.crisis_resources(lang) if crisis else [],
    )


def answers_to_csv_scale(answers: Dict[str, int]) -> Dict[str, int]:
    """
    Form ke 0-3 scale ko Deepression.csv ke 1-5 scale me map karta hai,
    taaki ML model ko wahi feature space mile jis par woh train hua tha.
        0 -> 1,  1 -> 2,  2 -> 4,  3 -> 5
    """
    mapping = {0: 1, 1: 2, 2: 4, 3: 5}
    return {ITEM_BY_KEY[k].csv_column: mapping[v] for k, v in answers.items()}


def form_schema(lang: str = i18n.DEFAULT_LANG) -> List[Dict[str, Any]]:
    """Template ko form render karne ke liye item metadata (user ki bhasha me)."""
    lang = i18n.normalise_lang(lang)
    return [
        {
            "key": i.key,
            "label": i18n.item_text(i.key, lang),
            "domain": i.domain,
            "domain_label": i18n.domain_text(i.domain, lang),
            "critical": i.critical,
        }
        for i in ITEMS
    ]


def option_schema(lang: str = i18n.DEFAULT_LANG) -> List[Dict[str, Any]]:
    lang = i18n.normalise_lang(lang)
    return [{"value": v, "label": i18n.option_text(v, lang)} for v in range(4)]
