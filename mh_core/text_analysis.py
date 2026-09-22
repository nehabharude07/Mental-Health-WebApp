"""
mh_core.text_analysis
---------------------
Free-text se symptom scores nikalta hai.

User English / Hindi / Marathi / Hinglish me — ya sab mila kar — likh sakta hai.
Yeh module code-mixed text handle karta hai: saari languages ke patterns ek saath
search hote hain, isliye "mujhe neend nahi aati and I feel very tired" bhi chalta hai.

Kaise kaam karta hai
--------------------
1. Text normalise (lowercase, punctuation clean)
2. Har symptom ke liye multilingual keyword patterns match
3. Negation check - "neend theek aati hai", "no anxiety" jaise cases skip
4. Intensity modifiers - "bahut", "खूप", "every day" -> score badhta hai
5. Duration cues - "1 month se", "हमेशा" -> score badhta hai
6. Result: 14 symptoms ka 0-3 score + kaunse detect hue uski list

Limitations (user ko UI me bataye jaate hain)
---------------------------------------------
Yeh keyword-based hai, koi language model nahi. Sarcasm, metaphor aur
indirect phrasing miss ho sakte hain. Isliye result ke saath user ko
questionnaire bharne ka option diya jaata hai.
"""

from __future__ import annotations

import re
import unicodedata
from typing import Dict, List, Tuple, Any

# --------------------------------------------------------------------------
# Lexicon: symptom_key -> list of regex patterns (all languages together)
# --------------------------------------------------------------------------

LEXICON: Dict[str, List[str]] = {
    "sleep": [
        r"\b(can'?t|cannot|unable to|trouble|difficulty|hard to)\s+(fall\s+)?sleep",
        r"\b(insomnia|sleepless|oversleep|sleeping too much|no sleep)\b",
        r"\bneend\s*(\w+\s+)?(nahi|nai|na|kam)\b",
        r"\bneend\s*(nahi aati|nahi aa rahi|nahi aa rhi|udd gayi)\b",
        r"\b(so nahi|soya nahi|so paata nahi|so pati nahi)\b",
        r"\b(zyada|jyada|bahut)\s*(sona|so raha|so rahi|sota|soti)\b",
        r"नींद\s*(नहीं|कम|पूरी नहीं|ठीक से नहीं)",
        r"(अनिद्रा|सो नहीं पाता|सो नहीं पाती|बहुत सोता|बहुत सोती)",
        r"झोप\s*(येत नाही|लागत नाही|कमी|नीट येत नाही)",
        r"(निद्रानाश|खूप झोपतो|खूप झोपते)",
    ],
    "appetite": [
        r"\b(no|poor|low|loss of|lost my)\s+appetite\b",
        r"\b(not eating|can'?t eat|don'?t feel like eating|overeating|binge eat)\b",
        r"\bbhookh\s*(\w+\s+)?(nahi|nai|kam|na)\b",
        r"\b(khaane ka mann nahi|khana nahi khaya|khana chhoot)\b",
        r"\b(zyada|jyada|bahut)\s*khaa",
        r"भूख\s*(नहीं|कम|मर)",
        r"(खाने का मन नहीं|ज़्यादा खा|बहुत खा)",
        r"भूक\s*(लागत नाही|कमी|नाही)",
        r"(खाण्याची इच्छा नाही|खूप खातो|खूप खाते)",
    ],
    "interest": [
        r"\b(no|lost|little|lack of)\s+(interest|pleasure|motivation|joy)\b",
        r"\b(nothing (feels|seems) (fun|good|interesting))\b",
        r"\b(don'?t enjoy|can'?t enjoy|not enjoying|anhedonia)\b",
        r"\b(don'?t feel like doing|no desire to do)\b",
        r"\bmann\s*(\w+\s+)?(nahi|nai|na)\s*lag",
        r"\b(kisi kaam me mann nahi|kuch achha nahi lagta|kuch accha nahi lagta)\b",
        r"\b(pehle jaisi khushi nahi|maza nahi aata|mazaa nahi)\b",
        r"(मन नहीं लगता|मन नहीं लग|किसी काम में मन नहीं)",
        r"(कुछ अच्छा नहीं लगता|पहले जैसी खुशी नहीं|मज़ा नहीं आता)",
        r"(मन लागत नाही|कशातच मन लागत नाही)",
        r"(काहीच आवडत नाही|पूर्वीसारखा आनंद नाही|मजा येत नाही)",
    ],
    "fatigue": [
        r"\b(tired|exhausted|fatigue|worn out|drained|no strength)\b",
        r"\bthak\w*\b",
        r"\b(thakaan|thaka hua|thaki hui|kamzori)\b",
        r"(थकान|थका हुआ|थकी हुई|कमज़ोरी|थक जाता|थक जाती)",
        r"(थकवा|दमछाक|अशक्तपणा|थकून जातो|थकून जाते)",
    ],
    "worthlessness": [
        r"\b(worthless|useless|failure|good for nothing|hate myself|burden)\b",
        r"\b(i'?m a (failure|loser)|not good enough|blame myself|guilty)\b",
        r"\b(bekaar|bekar|nakaam|nakaara|kisi kaam ka nahi)\b",
        r"\b(khud se nafrat|apne aap se nafrat|main failure|mai failure)\b",
        r"\bkhud ko (bura|bekaar|kosna|dosh)\b",
        r"(बेकार|नाकाम|निकम्मा|खुद से नफ़रत|अपराधबोध)",
        r"(खुद को दोष|मैं किसी काम का नहीं|मैं फेल)",
        r"(निरुपयोगी|अपयशी|स्वतःचा राग|स्वतःला दोष)",
        r"(मी कामाचा नाही|मी कामाची नाही)",
    ],
    "concentration": [
        r"\b(can'?t (focus|concentrate)|trouble (focusing|concentrating))\b",
        r"\b(poor concentration|mind wanders|forgetful|memory problem)\b",
        r"\bconcentration\s+(is\s+)?(very\s+)?(poor|bad|gone|terrible|low)\b",
        r"\b(focus|attention)\s+(is\s+)?(very\s+)?(poor|bad|gone|terrible|low)\b",
        r"\b(distracted|zoning out|blank mind|can'?t think (straight|clearly))\b",
        r"\b(dhyaan nahi|dhyan nahi|focus nahi|concentrate nahi)\b",
        r"\b(padhai me mann nahi|bhool jaata|bhool jati|yaad nahi rehta)\b",
        r"(ध्यान नहीं लग|ध्यान नहीं दे|एकाग्रता|भूल जाता|भूल जाती)",
        r"(पढ़ाई में ध्यान नहीं|याद नहीं रहता)",
        r"(लक्ष लागत नाही|एकाग्रता होत नाही|विसरतो|विसरते)",
    ],
    "agitation": [
        r"\b(slowed down|moving slowly|speaking slowly|sluggish)\b",
        r"\b(fidget|pacing|can'?t sit still because)\b",
        r"\b(dheema|dheere|sust|susti|slow ho gaya|slow ho gayi)\b",
        r"(धीमा पड़|सुस्त|सुस्ती|धीरे धीरे बोल)",
        r"(मंदावले|सुस्त|संथ|हळू बोल)",
    ],
    "suicidal_ideation": [
        r"\b(suicid\w*|kill myself|end my life|end it all|take my life)\b",
        r"\b(want to die|wish i (was|were) dead|better off dead|better off gone)\b",
        r"\b(self[- ]?harm|hurt myself|cutting myself|no reason to live)\b",
        r"\b(don'?t want to live|not want to live|life is not worth)\b",
        r"\b(marna chahta|marna chahti|mar jaun|mar jaaun|marne ka mann)\b",
        r"\b(jeena nahi chahta|jeena nahi chahti|jeene ka mann nahi)\b",
        r"\b(khud ko khatam|khudkushi|atmahatya|zindagi khatam)\b",
        r"\b(main na hota|mai na hoti|duniya me na hota)\b",
        r"(आत्महत्या|मरना चाहता|मरना चाहती|मर जाऊँ|मरने का मन)",
        r"(जीना नहीं चाहता|जीना नहीं चाहती|जीने का मन नहीं|ज़िंदगी खत्म)",
        r"(खुद को खत्म|खुद को नुकसान|मैं न होता|मैं न होती)",
        r"(आत्महत्या|मरावंसं वाटतं|मरून जावं|जगावंसं वाटत नाही)",
        r"(स्वतःला इजा|स्वतःला संपव|जीवन संपव)",
    ],
    "sleep_disturbance": [
        r"\b(wake up (at night|repeatedly|many times)|broken sleep|restless sleep)\b",
        r"\b(nightmares?|bad dreams|not restful|wake up tired)\b",
        r"\b(neend (tooti|khulti|bar bar khul)|raat ko uth|raat bhar jaagta|raat bhar jaagti)\b",
        r"\b(bure sapne|buri neend|so kar bhi thaka)\b",
        r"(नींद टूट|रात को उठ|रात भर जाग|बुरे सपने)",
        r"(बेचैन नींद|सोकर भी थका)",
        r"(झोप तुटते|रात्री जाग|रात्रभर जागा|वाईट स्वप्न)",
    ],
    "aggression": [
        r"\b(irritab\w*|short temper|angry|anger|rage|snapping at|lose my temper)\b",
        r"\b(frustrated at small things|annoyed easily)\b",
        r"\b(gussa|gusse|chidchid|chid jaata|chid jati|chidhta|jhunjhla)\b",
        r"\b(chhoti baat par gussa|control nahi hota gussa)\b",
        r"(गुस्सा|चिड़चिड़|चिढ़ जाता|चिढ़ जाती|झुँझला|क्रोध)",
        r"(छोटी बात पर गुस्सा)",
        r"(राग येतो|राग येते|चिडचिड|संताप|रागावतो|रागावते)",
    ],
    "panic_attacks": [
        r"\b(panic attack|anxiety attack|heart racing|palpitation)\b",
        r"\b(can'?t breathe|short(ness)? of breath|breathless|choking feeling)\b",
        r"\b(sudden fear|intense fear|trembling|sweating suddenly)\b",
        r"\b(panic|ghabrahat|ghabra|dil tez dhadak|saans phool|saans nahi)\b",
        r"\b(achanak dar|bahut dar lagta|haath paon thande)\b",
        r"(घबराहट|घबरा|दिल तेज़ धड़क|साँस फूल|साँस नहीं)",
        r"(अचानक डर|बहुत डर लगता|पैनिक)",
        r"(घबराट|छातीत धडधड|श्वास लागतो|अचानक भीती|खूप भीती वाटते)",
    ],
    "hopelessness": [
        r"\b(hopeless|no hope|nothing will get better|no future|pointless|meaningless)\b",
        r"\b(depress\w*|sad|down|low|empty|crying|cry a lot|feel like crying)\b",
        r"\b(give up|gave up|what'?s the point)\b",
        r"\b(ummeed (nahi|khatam)|umeed nahi|koi ummeed nahi)\b",
        r"\b(udaas|udasi|nirash|nirasha|dukhi|rona aata|rone ka mann)\b",
        r"\b(kuch theek nahi hoga|sab khatam|koi faayda nahi|bekaar lagta)\b",
        r"(उम्मीद नहीं|उम्मीद खत्म|निराश|निराशा|उदास|उदासी)",
        r"(रोना आता|रोने का मन|कुछ ठीक नहीं होगा|कोई फ़ायदा नहीं|खालीपन)",
        r"(आशा नाही|निराश|निराशा|उदास|उदासी|रडू येते)",
        r"(काहीच ठीक होणार नाही|काही अर्थ नाही|रिकामेपणा)",
    ],
    "restlessness": [
        r"\b(restless|can'?t sit still|keyed up|on edge|uneasy|agitated)\b",
        r"\b(overthinking|racing thoughts|mind won'?t stop)\b",
        r"\b(bechain|bechaini|tik kar nahi|ek jagah nahi|bekarari)\b",
        r"\b(dimaag chalta rehta|sochta rehta|sochti rehti|overthink)\b",
        r"(बेचैन|बेचैनी|टिक कर नहीं|एक जगह नहीं|दिमाग चलता रहता)",
        r"(सोचता रहता|सोचती रहती|ज़्यादा सोच)",
        r"(अस्वस्थ|अस्वस्थता|एका जागी बसवत नाही|सतत विचार)",
    ],
    "low_energy": [
        r"\b(no energy|low energy|no motivation|can'?t get out of bed|lethargic)\b",
        r"\b(everything feels heavy|dragging myself|no will to do anything)\b",
        r"\b(energy nahi|energy kam|motivation nahi|himmat nahi|utsah nahi)\b",
        r"\b(bistar se uthne ka mann nahi|kuch karne ka mann nahi|sust)\b",
        r"(ऊर्जा नहीं|एनर्जी नहीं|मोटिवेशन नहीं|हिम्मत नहीं|उत्साह नहीं)",
        r"(बिस्तर से उठने का मन नहीं|कुछ करने का मन नहीं)",
        r"(ऊर्जा नाही|उत्साह नाही|काही करावंसं वाटत नाही|अंथरुणातून उठवत नाही)",
    ],
}

# --------------------------------------------------------------------------
# Modifiers
# --------------------------------------------------------------------------

HIGH_INTENSITY = [
    r"\b(very|extremely|really|so|constantly|always|every ?day|daily|all the time)\b",
    r"\b(severe|terrible|unbearable|can'?t take it|worst)\b",
    r"\b(bahut|bohot|bohut|hamesha|har roz|roz|har waqt|har samay|zyada|bilkul)\b",
    r"(बहुत|हमेशा|हर रोज़|रोज़|हर वक़्त|बेहद|अत्यधिक|ज़्यादा)",
    r"(खूप|नेहमी|रोज|सतत|अतिशय|फार)",
]

LOW_INTENSITY = [
    r"\b(sometimes|occasionally|a bit|slightly|a little|once in a while|rarely)\b",
    r"\b(kabhi kabhi|kabhi-kabhi|thoda|thodi|halka|halki|kam)\b",
    r"(कभी कभी|कभी-कभी|थोड़ा|थोड़ी|हल्का|हल्की|कम)",
    r"(कधी कधी|थोडं|थोडी|जरा|कमी)",
]

_NUM_WORDS_EN = r"(a|one|two|three|four|five|six|several|many|few|couple of)"
_NUM_WORDS_HG = r"(ek|do|teen|char|paanch|panch|kai|kuch|do-teen)"
_NUM_WORDS_DEV = r"(एक|दो|तीन|चार|पाँच|पांच|कई|कुछ|दोन|तीन|चार|पाच)"

DURATION_LONG = [
    r"\b(\d+\s*(month|months|year|years|week|weeks))\b",
    r"\b" + _NUM_WORDS_EN + r"\s*(month|months|year|years|week|weeks)\b",
    r"\b" + _NUM_WORDS_HG + r"\s*(mahine|mahino|maheene|saal|hafte|hafto)\b",
    _NUM_WORDS_DEV + r"\s*(महीने|महीनों|महिन्यां|महिने|साल|वर्ष|हफ़्ते|हफ्ते|आठवडे|आठवड्यां)",
    r"\b(for (a|the) (long time|while)|since (long|months|years))\b",
    r"\b(\d+\s*(mahine|mahino|saal|hafte|hafto))\b",
    r"(\d+\s*(महीने|महीनों|साल|हफ़्ते|हफ्तों))",
    r"(\d+\s*(महिने|महिन्यां|वर्ष|आठवडे))",
    r"(लंबे समय से|काफ़ी समय से|बहुत दिनों से)",
    r"(बऱ्याच दिवसांपासून|खूप दिवसांपासून)",
]

NEGATIONS = [
    r"\bno\b", r"\bnot\b", r"\bnever\b", r"\bdon'?t\b", r"\bdoesn'?t\b",
    r"\bisn'?t\b", r"\bwithout\b", r"\bfine\b", r"\bokay\b", r"\bnormal\b",
    r"\bnahi\b", r"\bnahin\b", r"\bnai\b", r"\bna\b", r"\btheek\b", r"\bachha\b",
    r"नहीं", r"ठीक", r"अच्छा", r"सामान्य",
    r"नाही", r"ठीक", r"चांगल", r"बरं",
]

# Negation tab hi lagti hai jab woh keyword se pehle 3 words ke andar ho
# AUR keyword khud negative na ho (e.g. "neend nahi aati" me nahi symptom ka hissa hai)
_NEG_WINDOW = 3

# Ye patterns already negative hain - inke aage negation check skip karo
_SELF_NEGATIVE = re.compile(
    r"(nahi|nahin|nai|नहीं|नाही|can'?t|cannot|no |not |don'?t|lack|loss|poor|low)",
    re.IGNORECASE,
)

MIN_WORDS = 15


def _normalise(text: str) -> str:
    text = unicodedata.normalize("NFC", text or "")
    text = text.lower()
    text = re.sub(r"[^\w\s'\u0900-\u097F]+", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _count(patterns: List[str], text: str) -> int:
    return sum(len(re.findall(p, text, flags=re.IGNORECASE)) for p in patterns)


def _is_negated(text: str, match_start: int, pattern: str) -> bool:
    """Keyword ke pehle ke 3 shabd dekh kar negation decide karta hai."""
    if _SELF_NEGATIVE.search(pattern):
        return False  # pattern khud negative hai
    before = text[:match_start].split()[-_NEG_WINDOW:]
    window = " ".join(before)
    return any(re.search(n, window, flags=re.IGNORECASE) for n in NEGATIONS)


def word_count(text: str) -> int:
    return len(_normalise(text).split())


def analyse(text: str) -> Dict[str, Any]:
    """
    Free text -> {answers: {key: 0-3}, detected: [...], meta: {...}}

    answers directly scoring.score_answers() me daala ja sakta hai.
    """
    norm = _normalise(text)
    words = norm.split()

    high = _count(HIGH_INTENSITY, norm)
    low = _count(LOW_INTENSITY, norm)
    long_duration = _count(DURATION_LONG, norm) > 0

    answers: Dict[str, int] = {}
    detected: List[Dict[str, Any]] = []

    for key, patterns in LEXICON.items():
        hits = 0
        evidence: List[str] = []
        for pattern in patterns:
            for m in re.finditer(pattern, norm, flags=re.IGNORECASE):
                if _is_negated(norm, m.start(), pattern):
                    continue
                hits += 1
                snippet = m.group(0).strip()
                if snippet and snippet not in evidence:
                    evidence.append(snippet)

        if hits == 0:
            answers[key] = 0
            continue

        # base score by hit count
        score = 1 if hits == 1 else 2

        # modifiers
        if high and (high >= 2 or hits >= 2):
            score += 1
        if long_duration:
            score += 1
        if low and not high:
            score -= 1

        # suicidal ideation par hamesha kam se kam 2 - safety first
        if key == "suicidal_ideation":
            score = max(score, 2)

        score = max(1, min(3, score))   # detected = at least 1
        answers[key] = score
        if score > 0:
            detected.append({
                "key": key,
                "value": score,
                "evidence": evidence[:3],
                "critical": key == "suicidal_ideation",
            })

    # Agar ek hi description me kaafi alag-alag symptoms mention hue hain,
    # to woh apne aap ek zyada serious picture banata hai - halke scores ko ek
    # step upar le jaate hain (max 3 tak).
    if len(detected) >= 5 and (high or long_duration):
        for d in detected:
            if d["value"] < 3:
                d["value"] += 1
                answers[d["key"]] = d["value"]

    detected.sort(key=lambda d: d["value"], reverse=True)

    return {
        "answers": answers,
        "detected": detected,
        "meta": {
            "word_count": len(words),
            "symptoms_found": len(detected),
            "intensity_markers": high,
            "hedge_markers": low,
            "long_duration": long_duration,
            "confidence": _confidence(len(words), len(detected)),
        },
    }


def _confidence(words: int, found: int) -> str:
    if words < MIN_WORDS or found == 0:
        return "low"
    if words >= 60 and found >= 4:
        return "moderate"
    if found >= 2:
        return "limited"
    return "low"
