# Mental Health Screening System — Upgraded

## Kya problem thi

**1. Model sirf 8 hardcoded rows par train tha.**
Purana `train_model.py` me dataset ek Python dict tha jisme 8 rows thin.
`train_test_split(test_size=0.2)` ke baad training ke liye sirf **6 samples** bache.
LogisticRegression 6 samples se koi generalisable pattern nahi seekh sakta — isliye
app har naye input par lagbhag ek hi jawab de raha tha. **Yahi aapki main complaint thi.**

**2. Aapki asli dataset use hi nahi ho rahi thi.**
`Deepression.csv` (813 rows, 14 symptom features) project folder me padi thi
par koi code use nahi kar raha tha. App 5 alag features (age, gender, sleep,
exercise, stress) maang raha tha jinka dataset se koi rishta nahi tha.

**3. Dataset khud problematic hai.** `python train_model.py` chalane par yeh audit milta hai:

| Check | Value |
|---|---|
| Rows loaded | 813 |
| Rows dropped (blank/corrupt label) | 273 |
| Out-of-range cells clipped (scale 1–5 me 6 tha) | 168 |
| Usable rows | 540 |
| Unique symptom profiles | **30** |
| Profiles with contradictory labels | **18 / 30** |
| Maximum achievable accuracy (Bayes ceiling) | **50.6%** |

Matlab: CSV me ek hi symptom-combination par kahin "Mild", kahin "Severe"
likha hai. Aise data par koi bhi algorithm 50% se upar nahi ja sakta.
Feature–label correlation bhi ±0.17 (lagbhag zero) hai.

**4. Aur bhi issues:** input validation nahi thi (galat input → 500 error),
output sirf binary tha, `model.pkl` missing hone par app startup par crash hota,
`requirements.txt` me ek Windows installer path likha tha, aur `static/main.js`
me Electron ka code tha jo Flask ke browser me load hokar error deta tha.

---

## Solution: hybrid engine

Kyunki dataset bharosemand nahi hai, app **do engines** use karta hai:

### Primary — Clinical scoring (`mh_core/scoring.py`)
PHQ-9 / GAD-7 jaise validated screening instruments ke structure par bana
14-item questionnaire. Har item 0–3 scale par, weighted scoring se
0–100 severity index, phir 4 bands: No depression / Mild / Moderate / Severe.

Yeh **deterministic** hai — har naye input par sahi kaam karta hai, chahe woh
combination training data me kabhi aaya ho ya nahi. **Yahi cheez missing thi.**

### Secondary — ML model (`train_model.py`)
Cleaned data par 4 models compare hote hain (5-fold stratified CV):

```
baseline_majority        0.322
logistic_regression      0.337
random_forest            0.415
hist_gradient_boosting   0.446   <- best
```

Best model 44.6% par aata hai — ceiling 50.6% ke kaafi paas, yaani model
apna kaam theek kar raha hai, **data hi limit hai**. Isliye bundle me
`reliable: false` flag lagta hai aur app ise sirf "low confidence reference"
ke taur par, honest accuracy ke saath dikhata hai. Headline result rule
engine se aata hai.

Agar aapko kabhi better-labelled data mil jaye, to `train_model.py` dobara
chalayein — accuracy 60% cross karte hi model apne aap primary ban jayega.

---

## Naye features

- 14-item questionnaire, English + Hinglish dono me
- 4-level severity output with 0–100 score ring aur severity bar
- Per-domain breakdown (core / cognitive / somatic / anxiety / affective / risk)
- "Sabse prominent symptoms" list
- **Safety pathway**: suicidal ideation item par response aane par India ke
  24x7 helplines dikhte hain aur result kam se kam Moderate hota hai
- Poori input validation with saaf error messages (400, 500 ab crash nahi)
- JSON API: `POST /api/predict`, `GET /api/schema`, `GET /api/model`, `GET /health`
- Model transparency page — accuracy, baseline, ceiling sab visible
- Mobile-responsive dark UI
- Progress counter aur unanswered question highlight

---

## Files

```
app.py                    Flask app (rewritten)
train_model.py            training pipeline (rewritten)
mh_core/
  scoring.py              questionnaire + rule-based severity engine
  data_prep.py            CSV cleaning + data quality audit
  engine.py               hybrid predictor (rule + ML)
templates/index.html      UI (rewritten)
static/style.css          styles (rewritten)
static/app.js             frontend helpers (naya)
model/
  model_bundle.joblib     trained pipeline + metadata
  metrics.json            full metrics report
Deepression_clean.csv     cleaned dataset (auto-generated)
electron_main.js          purana Electron code (Flask se alag)
*_OLD.py.bak              aapki purani files, backup ke liye
```

---

## Kaise chalayein

Windows (aapka setup):
```cmd
env1\Scripts\activate
pip install -r requirements.txt
python train_model.py
python app.py
```
Ya seedha `run.bat` double-click karein.

Phir browser me: **http://127.0.0.1:5000**

API example:
```bash
curl -X POST http://127.0.0.1:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"sleep":2,"appetite":1,"interest":3,"fatigue":2,"worthlessness":3,
       "concentration":2,"agitation":1,"suicidal_ideation":0,
       "sleep_disturbance":2,"aggression":1,"panic_attacks":0,
       "hopelessness":3,"restlessness":1,"low_energy":2}'
```

---

## Agla step (agar accuracy badhani ho)

ML side ki accuracy **sirf better data se** badhegi, code se nahi:

1. **Labels theek karwayein** — abhi 18/30 profiles contradictory hain. Agar
   yeh dataset kisi survey se aaya hai to original labelling process check karein.
2. **Zyada unique profiles** — 540 rows me sirf 30 unique combinations hain.
   Asli variety chahiye, duplicate rows nahi.
3. **Severity-consistent labels** — agar labels actual PHQ-9 total score se
   derive kiye jayein, to model 85%+ easily cross karega.

Tab tak clinical scoring engine hi sahi aur defensible approach hai — aur
viva/presentation me yeh explain karna aapke project ke liye plus point hai:
aapne data quality audit kiya, problem identify ki, aur uska principled
solution diya.

---

## Zaroori disclaimer

Yeh ek **screening / self-awareness tool** hai, medical diagnosis nahi.
Iska result kisi qualified doctor ya mental health professional ki jagah
nahi le sakta.

Agar aap ya koi jaan-pehchaan wala mushkil daur se guzar raha hai:
**Tele-MANAS 14416** · **KIRAN 1800-599-0019** — dono 24x7, free, confidential.

---

# v2 Update — Language support + Free-text mode

## 1. Layout fix

Purana questionnaire har sawaal ko ek bade vertical block me dikhata tha —
isliye page bahut lamba ho jaata tha aur scroll karte rehna padta tha.

Ab har sawaal ek **compact row** hai: baayein taraf question, daayein taraf
chaaron options ek line me. 14 sawaal ab ek screen me aa jaate hain.
Mobile (820px se chhota) par ye automatically do lines me toot jaata hai.

## 2. 4 languages

| Code | Language |
|---|---|
| `en` | English |
| `hi` | हिन्दी (Devanagari) |
| `mr` | मराठी (Devanagari) |
| `hinglish` | Hinglish (Roman) |

Header me top-right switcher hai. Choice cookie me 1 saal ke liye save hoti hai.
URL se bhi set ho sakti hai: `/?lang=mr` ya `/lang/mr`.

Saara text `mh_core/i18n.py` me ek jagah hai — questions, options, severity
labels, advice, crisis resources, error messages, sab. **Naya language add karna:**
`LANGUAGES` me entry daalein, phir `ITEM_TEXT` / `OPTION_TEXT` / `STATE_TEXT` /
`DOMAIN_TEXT` / `ADVICE_TEXT` / `UI` / `CRISIS_TEXT` me uska block likh dein.
Code me kahin aur change nahi karna padega.

## 3. Free-text mode (naya)

Ab "Apne shabdon me batayein" tab me user apni pareshani khud likh sakta hai —
Hindi, Marathi, English, Hinglish, ya sab mila kar. Code-mixed text bhi chalta hai:

> "mujhe neend nahi aati and I feel very tired, कुछ अच्छा नहीं लगता and खूप चिडचिड होते"

`mh_core/text_analysis.py` ismein se 14 symptoms extract karta hai:

1. Text normalise (Unicode NFC, lowercase, punctuation clean)
2. Har symptom ke liye multilingual regex patterns match — saari languages
   ek saath, isliye code-mixing automatically handle hoti hai
3. **Negation handling** — keyword se pehle 3 shabd check hote hain.
   "neend achhi aati hai" aur "koi tension nahi hai" galti se symptom nahi bante
4. **Intensity modifiers** — "bahut" / "खूप" / "every day" / "extremely" → score upar
5. **Duration cues** — "do mahine se" / "तीन महीने" / "three months" → score upar
6. **Multi-symptom escalation** — ek hi description me 5+ alag symptoms +
   intensity/duration → sabhi ek step upar

Phir wahi rule-based scoring engine chalta hai, bas ek calibration ke saath:

**Partial-coverage normalisation.** Free text me user sirf wahi symptoms likhta
hai jo use pareshan kar rahe hain — baaki 14 me se jo mention nahi hue unhe "0"
maan lena galat hoga (warna har description "Mild" nikal aati). Isliye
denominator sirf mentioned symptoms par banta hai, par ek floor ke saath
(`PARTIAL_FLOOR = 0.45`) taaki 1 symptom likhne se 100% na ho jaye.

Result me **"Aapke text se jo samajh aaya"** panel dikhta hai — kaunsa symptom
kis level par detect hua, aur text ka woh hissa jisse woh detect hua.
User dekh sakta hai ki analysis sahi hai ya nahi.

### Iski limitations (UI me bhi bataye gaye hain)

Yeh **keyword-based** hai, koi language model nahi. Sarcasm, metaphor, aur
bahut indirect phrasing miss ho sakte hain. Isliye:
- result ke saath confidence level (`low` / `limited` / `moderate`) dikhta hai
- user ko questionnaire bharne ka option diya jaata hai, jo zyada accurate hai
- suicidal ideation detect hone par score kabhi 2 se kam nahi hota, aur
  crisis resources turant dikhte hain — safety par keyword-based system me
  false positive, false negative se behtar hai

Minimum ~15 words chahiye, warna app zyada likhne ko kehta hai.

## Naye API endpoints

```bash
# free text
curl -X POST http://127.0.0.1:5000/api/describe \
  -H "Content-Type: application/json" \
  -d '{"lang":"mr","text":"गेल्या दोन महिन्यांपासून मला झोप येत नाही, कोणत्याही कामात मन लागत नाही, खूप थकवा जाणवतो आणि चिडचिड होते"}'

# questionnaire (lang optional)
curl -X POST http://127.0.0.1:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"lang":"hi","sleep":2,"appetite":1,"interest":3,"fatigue":2,"worthlessness":3,
       "concentration":2,"agitation":1,"suicidal_ideation":0,"sleep_disturbance":2,
       "aggression":1,"panic_attacks":0,"hopelessness":3,"restlessness":1,"low_energy":2}'

# schema in a given language
curl "http://127.0.0.1:5000/api/schema?lang=mr"
```

## Naye files

```
mh_core/i18n.py            saare 4 languages ka text (single source of truth)
mh_core/text_analysis.py   multilingual free-text symptom extraction
```
