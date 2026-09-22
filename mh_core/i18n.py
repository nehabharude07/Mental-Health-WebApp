"""
mh_core.i18n
------------
4 languages: English, Hindi (Devanagari), Marathi (Devanagari), Hinglish.

Saare user-facing strings yahan hain. Naya language add karna ho to bas
LANGUAGES me entry daalein aur UI + ITEM_TEXT me uska block likh dein.
"""

from __future__ import annotations
from typing import Dict, Any

DEFAULT_LANG = "hinglish"

LANGUAGES: Dict[str, Dict[str, str]] = {
    "en":       {"name": "English",  "native": "English",   "flag": "EN"},
    "hi":       {"name": "Hindi",    "native": "हिन्दी",     "flag": "हि"},
    "mr":       {"name": "Marathi",  "native": "मराठी",      "flag": "मर"},
    "hinglish": {"name": "Hinglish", "native": "Hinglish",  "flag": "HI"},
}


def normalise_lang(value: str | None) -> str:
    if not value:
        return DEFAULT_LANG
    value = str(value).strip().lower()
    return value if value in LANGUAGES else DEFAULT_LANG


# ---------------------------------------------------------------------------
# Questionnaire item text, keyed by item.key
# ---------------------------------------------------------------------------

ITEM_TEXT: Dict[str, Dict[str, str]] = {
    "sleep": {
        "en": "Trouble falling asleep, staying asleep, or sleeping too much",
        "hi": "नींद आने में परेशानी, बार-बार नींद खुलना, या बहुत ज़्यादा सोना",
        "mr": "झोप न लागणे, वारंवार जाग येणे, किंवा खूप जास्त झोपणे",
        "hinglish": "Neend aane me dikkat, baar baar neend khulna, ya zyada sona",
    },
    "appetite": {
        "en": "Poor appetite or overeating",
        "hi": "भूख कम लगना या ज़रूरत से ज़्यादा खाना",
        "mr": "भूक कमी लागणे किंवा गरजेपेक्षा जास्त खाणे",
        "hinglish": "Bhookh kam lagna ya zarurat se zyada khaana",
    },
    "interest": {
        "en": "Little interest or pleasure in doing things",
        "hi": "किसी काम में मन न लगना, पहले जैसी खुशी न मिलना",
        "mr": "कोणत्याही कामात मन न लागणे, पूर्वीसारखा आनंद न मिळणे",
        "hinglish": "Kisi kaam me mann na lagna, pehle jaisi khushi na milna",
    },
    "fatigue": {
        "en": "Feeling tired or having little energy",
        "hi": "थकान महसूस होना, ऊर्जा की कमी",
        "mr": "थकवा जाणवणे, ऊर्जा कमी वाटणे",
        "hinglish": "Thakaan mehsoos hona, energy ki kami",
    },
    "worthlessness": {
        "en": "Feeling bad about yourself, or that you are a failure",
        "hi": "खुद को बेकार या नाकाम समझना",
        "mr": "स्वतःला निरुपयोगी किंवा अपयशी समजणे",
        "hinglish": "Khud ko bekaar ya failure samajhna",
    },
    "concentration": {
        "en": "Trouble concentrating on things like reading or work",
        "hi": "पढ़ाई या काम पर ध्यान न लगा पाना",
        "mr": "अभ्यास किंवा कामावर लक्ष केंद्रित न होणे",
        "hinglish": "Padhai ya kaam par dhyaan na laga paana",
    },
    "agitation": {
        "en": "Moving or speaking slowly, or being unusually fidgety",
        "hi": "धीमा पड़ जाना, या बहुत बेचैन होकर हिलते रहना",
        "mr": "हालचाल मंदावणे, किंवा खूप अस्वस्थ होऊन हलत राहणे",
        "hinglish": "Dheema pad jaana, ya bahut bechain hokar hilte rehna",
    },
    "suicidal_ideation": {
        "en": "Thoughts that you would be better off gone, or of hurting yourself",
        "hi": "ऐसे विचार कि आप न होते तो बेहतर होता, या खुद को नुकसान पहुँचाने के विचार",
        "mr": "आपण नसतो तर बरे झाले असते असे विचार, किंवा स्वतःला इजा करण्याचे विचार",
        "hinglish": "Aise vichaar ki aap na hote to behtar hota, ya khud ko nuksaan pahunchana",
    },
    "sleep_disturbance": {
        "en": "Disturbed, broken or non-restful sleep",
        "hi": "टूटी-टूटी, बेचैन, आराम न देने वाली नींद",
        "mr": "अस्वस्थ, तुटक, आराम न देणारी झोप",
        "hinglish": "Neend tooti-tooti, bechain, aaram na dene wali",
    },
    "aggression": {
        "en": "Irritability, short temper or angry outbursts",
        "hi": "चिड़चिड़ापन, छोटी बात पर गुस्सा आना",
        "mr": "चिडचिड, लहान गोष्टीवर राग येणे",
        "hinglish": "Chidchidapan, chhoti baat par gussa aana",
    },
    "panic_attacks": {
        "en": "Sudden episodes of intense fear, racing heart or breathlessness",
        "hi": "अचानक तेज़ डर, दिल तेज़ धड़कना, साँस फूलना",
        "mr": "अचानक तीव्र भीती, हृदय जोरात धडधडणे, श्वास लागणे",
        "hinglish": "Achanak tez dar, dil tez dhadakna, saans phoolna",
    },
    "hopelessness": {
        "en": "Feeling down, hopeless, or that nothing will get better",
        "hi": "उदासी, उम्मीद खत्म लगना, कुछ ठीक नहीं होगा ऐसा लगना",
        "mr": "उदासी, आशा संपल्यासारखी वाटणे, काहीच ठीक होणार नाही असे वाटणे",
        "hinglish": "Udaasi, ummeed khatam lagna, kuch theek nahi hoga aisa lagna",
    },
    "restlessness": {
        "en": "Feeling restless, keyed up or unable to sit still",
        "hi": "बेचैनी, एक जगह टिक कर न बैठ पाना",
        "mr": "अस्वस्थता, एका जागी स्थिर बसता न येणे",
        "hinglish": "Bechaini, ek jagah tik kar na baith paana",
    },
    "low_energy": {
        "en": "Persistent low energy or motivation through the day",
        "hi": "दिन भर ऊर्जा और प्रेरणा का कम रहना",
        "mr": "दिवसभर ऊर्जा आणि उत्साह कमी राहणे",
        "hinglish": "Din bhar energy aur motivation ka kam rehna",
    },
}

# ---------------------------------------------------------------------------
# Response options (0-3)
# ---------------------------------------------------------------------------

OPTION_TEXT: Dict[int, Dict[str, str]] = {
    0: {"en": "Not at all",              "hi": "बिल्कुल नहीं",        "mr": "अजिबात नाही",       "hinglish": "Bilkul nahi"},
    1: {"en": "Several days",            "hi": "कुछ दिन",             "mr": "काही दिवस",          "hinglish": "Kuch din"},
    2: {"en": "More than half the days", "hi": "आधे से ज़्यादा दिन",   "mr": "अर्ध्याहून जास्त दिवस", "hinglish": "Aadhe se zyada din"},
    3: {"en": "Nearly every day",        "hi": "लगभग रोज़",           "mr": "जवळजवळ रोज",         "hinglish": "Lagbhag roz"},
}

# ---------------------------------------------------------------------------
# Severity states
# ---------------------------------------------------------------------------

STATE_TEXT: Dict[str, Dict[str, str]] = {
    "No depression": {"en": "No depression", "hi": "कोई अवसाद नहीं", "mr": "नैराश्य नाही",  "hinglish": "No depression"},
    "Mild":          {"en": "Mild",          "hi": "हल्का",          "mr": "सौम्य",          "hinglish": "Mild"},
    "Moderate":      {"en": "Moderate",      "hi": "मध्यम",          "mr": "मध्यम",          "hinglish": "Moderate"},
    "Severe":        {"en": "Severe",        "hi": "गंभीर",          "mr": "गंभीर",          "hinglish": "Severe"},
}

DOMAIN_TEXT: Dict[str, Dict[str, str]] = {
    "core":      {"en": "Core mood",   "hi": "मुख्य मनोदशा", "mr": "मुख्य मनःस्थिती", "hinglish": "Core mood"},
    "cognitive": {"en": "Cognitive",   "hi": "संज्ञानात्मक",  "mr": "बोधात्मक",       "hinglish": "Cognitive"},
    "somatic":   {"en": "Physical",    "hi": "शारीरिक",      "mr": "शारीरिक",        "hinglish": "Physical"},
    "anxiety":   {"en": "Anxiety",     "hi": "चिंता",         "mr": "चिंता",           "hinglish": "Anxiety"},
    "affective": {"en": "Mood/temper", "hi": "मिज़ाज",        "mr": "मनःस्थिती/राग",   "hinglish": "Mood/temper"},
    "risk":      {"en": "Risk",        "hi": "जोखिम",         "mr": "धोका",            "hinglish": "Risk"},
}

# ---------------------------------------------------------------------------
# Advice per severity band
# ---------------------------------------------------------------------------

ADVICE_TEXT: Dict[str, Dict[str, Dict[str, str]]] = {
    "No depression": {
        "en": {
            "headline": "Your answers do not point to a significant depressive pattern.",
            "detail": "Things look steady. Keep up regular sleep, some physical activity and "
                      "connection with people. If how you feel changes later, you can check again.",
        },
        "hi": {
            "headline": "आपके जवाब किसी बड़े अवसाद के पैटर्न की ओर इशारा नहीं करते।",
            "detail": "स्थिति ठीक लग रही है। नियमित नींद, थोड़ी शारीरिक गतिविधि और लोगों से जुड़ाव "
                      "बनाए रखें। आगे कभी भावनाएँ बदलने लगें तो दोबारा जाँच सकते हैं।",
        },
        "mr": {
            "headline": "तुमची उत्तरे कोणत्याही मोठ्या नैराश्याच्या नमुन्याकडे निर्देश करत नाहीत.",
            "detail": "परिस्थिती ठीक दिसते आहे. नियमित झोप, थोडी शारीरिक हालचाल आणि लोकांशी संपर्क "
                      "टिकवून ठेवा. पुढे कधी भावना बदलल्या तर पुन्हा तपासू शकता.",
        },
        "hinglish": {
            "headline": "Aapke jawab kisi significant depressive pattern ki taraf ishaara nahi karte.",
            "detail": "Routine theek lag raha hai. Neend, exercise aur logon se connection maintain "
                      "rakhein. Agar aage kabhi feelings badalne lagein to dobara check kar sakte hain.",
        },
    },
    "Mild": {
        "en": {
            "headline": "Mild-level symptoms are showing up.",
            "detail": "At this stage lifestyle changes help a lot — a fixed sleep schedule, daily "
                      "physical activity, less screen time, and talking to someone you trust. "
                      "If this continues beyond two weeks, speaking to a counsellor is a good idea.",
        },
        "hi": {
            "headline": "हल्के स्तर के लक्षण दिख रहे हैं।",
            "detail": "इस चरण पर जीवनशैली में बदलाव काफ़ी मदद करते हैं — तय समय पर नींद, रोज़ थोड़ी "
                      "शारीरिक गतिविधि, कम स्क्रीन टाइम, और किसी भरोसेमंद व्यक्ति से बात करना। "
                      "अगर दो हफ़्ते से ज़्यादा ऐसा ही चले तो काउंसलर से बात करना ठीक रहेगा।",
        },
        "mr": {
            "headline": "सौम्य पातळीची लक्षणे दिसत आहेत.",
            "detail": "या टप्प्यावर जीवनशैलीतील बदल खूप मदत करतात — ठराविक वेळी झोप, रोज थोडी "
                      "शारीरिक हालचाल, कमी स्क्रीन टाइम, आणि विश्वासू व्यक्तीशी बोलणे. "
                      "दोन आठवड्यांपेक्षा जास्त असेच राहिले तर समुपदेशकाशी बोलणे योग्य ठरेल.",
        },
        "hinglish": {
            "headline": "Halke (mild) level ke symptoms dikh rahe hain.",
            "detail": "Is stage par lifestyle changes kaafi madad karte hain - fixed sleep schedule, "
                      "rozana thodi physical activity, screen time kam, aur kisi bharose ke insaan se "
                      "baat karna. Agar 2 hafte se zyada aisa hi chale to counsellor se baat karna theek rahega.",
        },
    },
    "Moderate": {
        "en": {
            "headline": "Moderate-level symptoms are showing up.",
            "detail": "This level usually starts affecting day-to-day functioning. Consulting a "
                      "qualified mental health professional (psychologist or psychiatrist) is "
                      "recommended. Therapy is very effective at this stage.",
        },
        "hi": {
            "headline": "मध्यम स्तर के लक्षण दिख रहे हैं।",
            "detail": "यह स्तर आमतौर पर रोज़मर्रा के कामों पर असर डालता है। किसी योग्य मानसिक स्वास्थ्य "
                      "पेशेवर (मनोवैज्ञानिक या मनोचिकित्सक) से परामर्श लेना सुझाया जाता है। "
                      "इस चरण पर थेरेपी बहुत प्रभावी होती है।",
        },
        "mr": {
            "headline": "मध्यम पातळीची लक्षणे दिसत आहेत.",
            "detail": "ही पातळी सहसा रोजच्या कामकाजावर परिणाम करते. पात्र मानसिक आरोग्य तज्ज्ञाचा "
                      "(मानसशास्त्रज्ञ किंवा मनोविकारतज्ज्ञ) सल्ला घेणे शिफारसीय आहे. "
                      "या टप्प्यावर थेरपी खूप प्रभावी ठरते.",
        },
        "hinglish": {
            "headline": "Moderate level ke symptoms dikh rahe hain.",
            "detail": "Yeh level aam taur par rozmarra ke kaam par asar daalta hai. Kisi qualified "
                      "mental health professional (psychologist ya psychiatrist) se consultation lena "
                      "recommended hai. Therapy is stage par bahut effective hoti hai.",
        },
    },
    "Severe": {
        "en": {
            "headline": "Symptoms are in the severe range.",
            "detail": "Please consult a mental health professional soon. This is not weakness — "
                      "severe depression is a treatable medical condition, and professional support "
                      "leads to significant improvement. Tell someone close to you as well, so you "
                      "are not dealing with it alone.",
        },
        "hi": {
            "headline": "लक्षण गंभीर श्रेणी में आ रहे हैं।",
            "detail": "कृपया जल्द किसी मानसिक स्वास्थ्य पेशेवर से मिलें। यह कमज़ोरी नहीं है — गंभीर "
                      "अवसाद एक इलाज योग्य चिकित्सीय स्थिति है, और पेशेवर सहायता से काफ़ी सुधार होता है। "
                      "किसी अपने को भी बता दें ताकि आप अकेले न रहें।",
        },
        "mr": {
            "headline": "लक्षणे गंभीर श्रेणीत येत आहेत.",
            "detail": "कृपया लवकर मानसिक आरोग्य तज्ज्ञाचा सल्ला घ्या. ही कमजोरी नाही — गंभीर नैराश्य "
                      "हा उपचार करण्यायोग्य वैद्यकीय आजार आहे, आणि व्यावसायिक मदतीने लक्षणीय सुधारणा "
                      "होते. जवळच्या कोणालातरी सांगा, म्हणजे तुम्ही एकटे राहणार नाही.",
        },
        "hinglish": {
            "headline": "Symptoms severe range me aa rahe hain.",
            "detail": "Please kisi mental health professional se jaldi consult karein. Yeh kamzori nahi "
                      "hai - severe depression ek treatable medical condition hai, aur professional "
                      "support se significant improvement hota hai. Kisi apne ko bhi bata dein taaki "
                      "aap akele na rahein.",
        },
    },
}

# ---------------------------------------------------------------------------
# UI strings
# ---------------------------------------------------------------------------

UI: Dict[str, Dict[str, str]] = {
    "en": {
        "title": "Mental Health Screening System",
        "subtitle": "14-item symptom check based on validated screening instruments (PHQ-9 / GAD-7 style)",
        "notice_strong": "This is a screening tool, not a diagnosis.",
        "notice": "The result cannot replace the opinion of a doctor or mental health professional. "
                  "If you are struggling, please talk to a professional.",
        "tab_quiz": "Questionnaire",
        "tab_text": "Describe in your own words",
        "form_title": "Over the last 2 weeks, how often have you felt this?",
        "form_sub": "Pick one option for each. All 14 are required.",
        "form_title_again": "Fill it again",
        "submit": "See result",
        "clear": "Clear",
        "text_title": "Tell us what you are going through",
        "text_sub": "Write freely in English, Hindi, Marathi or Hinglish. The more detail you give, "
                    "the better the analysis. Minimum ~15 words.",
        "text_placeholder": "For example: For the last month I can't sleep properly, I don't feel "
                            "like doing anything, I get irritated at small things and I feel tired all day...",
        "text_submit": "Analyse my description",
        "text_note": "Note: this reads your text with a keyword-based analyser. It can miss things. "
                     "After the result you can open the questionnaire to refine it.",
        "result_eyebrow": "Screening result",
        "again": "Take the test again",
        "symptom_areas": "Symptom areas",
        "top_symptoms": "Most prominent symptoms",
        "no_symptoms": "No symptom was reported frequently.",
        "detected_title": "What we picked up from your text",
        "detected_none": "We couldn't clearly pick up specific symptoms from your text. "
                         "Please try the questionnaire for a reliable result.",
        "detected_hint": "If something is wrong or missing here, fill the questionnaire instead — it is more accurate.",
        "ml_opinion": "ML model's opinion",
        "low_conf": "low confidence",
        "model_info": "Model information",
        "crisis_title": "Support is available to you right now",
        "crisis_small": "If the danger is immediate, call 112 or go to someone you trust.",
        "disclaimer": "This is a screening tool, not a medical diagnosis. It cannot replace a "
                      "qualified doctor or mental health professional.",
        "footer": "If you ever have thoughts of harming yourself —",
        "footer_tail": "both 24x7, free",
        "lang_label": "Language",
        "err_short": "Please write a little more — at least 15 words — so the analysis is meaningful.",
    },
    "hi": {
        "title": "मानसिक स्वास्थ्य स्क्रीनिंग प्रणाली",
        "subtitle": "मान्य स्क्रीनिंग उपकरणों (PHQ-9 / GAD-7 शैली) पर आधारित 14-प्रश्न लक्षण जाँच",
        "notice_strong": "यह एक स्क्रीनिंग टूल है, निदान नहीं।",
        "notice": "इसका परिणाम किसी डॉक्टर या मानसिक स्वास्थ्य पेशेवर की राय की जगह नहीं ले सकता। "
                  "अगर आप परेशानी महसूस कर रहे हैं, कृपया किसी पेशेवर से बात करें।",
        "tab_quiz": "प्रश्नावली",
        "tab_text": "अपने शब्दों में बताएँ",
        "form_title": "पिछले 2 हफ़्तों में आपने यह कितनी बार महसूस किया?",
        "form_sub": "हर सवाल का एक विकल्प चुनें। सभी 14 ज़रूरी हैं।",
        "form_title_again": "दोबारा भरें",
        "submit": "परिणाम देखें",
        "clear": "साफ़ करें",
        "text_title": "बताइए आप किस दौर से गुज़र रहे हैं",
        "text_sub": "हिन्दी, मराठी, अंग्रेज़ी या हिंग्लिश — किसी में भी खुलकर लिखें। जितना विस्तार देंगे, "
                    "विश्लेषण उतना बेहतर होगा। कम से कम ~15 शब्द।",
        "text_placeholder": "जैसे: पिछले एक महीने से मुझे ठीक से नींद नहीं आती, किसी काम में मन नहीं लगता, "
                            "छोटी बात पर चिढ़ जाता हूँ और दिन भर थकान रहती है...",
        "text_submit": "मेरा विवरण विश्लेषित करें",
        "text_note": "ध्यान दें: यह आपके टेक्स्ट को कीवर्ड-आधारित विश्लेषक से पढ़ता है। कुछ चीज़ें छूट सकती हैं। "
                     "परिणाम के बाद आप प्रश्नावली खोलकर इसे बेहतर कर सकते हैं।",
        "result_eyebrow": "स्क्रीनिंग परिणाम",
        "again": "दोबारा जाँच करें",
        "symptom_areas": "लक्षण क्षेत्र",
        "top_symptoms": "सबसे प्रमुख लक्षण",
        "no_symptoms": "कोई लक्षण बार-बार दर्ज नहीं हुआ।",
        "detected_title": "आपके टेक्स्ट से जो समझ आया",
        "detected_none": "आपके टेक्स्ट से स्पष्ट लक्षण नहीं पकड़ पाए। भरोसेमंद परिणाम के लिए कृपया प्रश्नावली भरें।",
        "detected_hint": "अगर यहाँ कुछ ग़लत या छूटा हुआ है, तो प्रश्नावली भरें — वह ज़्यादा सटीक है।",
        "ml_opinion": "ML मॉडल की राय",
        "low_conf": "कम भरोसा",
        "model_info": "मॉडल जानकारी",
        "crisis_title": "अभी आपको सहायता मिल सकती है",
        "crisis_small": "अगर ख़तरा तुरंत है, तो 112 पर कॉल करें या किसी भरोसेमंद व्यक्ति के पास जाएँ।",
        "disclaimer": "यह एक स्क्रीनिंग टूल है, चिकित्सीय निदान नहीं। यह किसी योग्य डॉक्टर या मानसिक "
                      "स्वास्थ्य पेशेवर की जगह नहीं ले सकता।",
        "footer": "अगर कभी भी आपको ख़ुद को नुकसान पहुँचाने के विचार आएँ —",
        "footer_tail": "दोनों 24x7, निःशुल्क",
        "lang_label": "भाषा",
        "err_short": "कृपया थोड़ा और लिखें — कम से कम 15 शब्द — ताकि विश्लेषण सार्थक हो।",
    },
    "mr": {
        "title": "मानसिक आरोग्य तपासणी प्रणाली",
        "subtitle": "मान्यताप्राप्त तपासणी साधनांवर (PHQ-9 / GAD-7 शैली) आधारित 14-प्रश्न लक्षण तपासणी",
        "notice_strong": "हे एक तपासणी साधन आहे, निदान नव्हे.",
        "notice": "याचा निकाल डॉक्टर किंवा मानसिक आरोग्य तज्ज्ञाच्या मताची जागा घेऊ शकत नाही. "
                  "तुम्हाला त्रास होत असेल, तर कृपया तज्ज्ञाशी बोला.",
        "tab_quiz": "प्रश्नावली",
        "tab_text": "स्वतःच्या शब्दांत सांगा",
        "form_title": "गेल्या 2 आठवड्यांत तुम्हाला हे किती वेळा जाणवले?",
        "form_sub": "प्रत्येक प्रश्नासाठी एक पर्याय निवडा. सर्व 14 आवश्यक आहेत.",
        "form_title_again": "पुन्हा भरा",
        "submit": "निकाल पहा",
        "clear": "साफ करा",
        "text_title": "तुम्ही कोणत्या परिस्थितीतून जात आहात ते सांगा",
        "text_sub": "मराठी, हिंदी, इंग्रजी किंवा हिंग्लिश — कोणत्याही भाषेत मोकळेपणाने लिहा. जितका तपशील "
                    "द्याल, तितके विश्लेषण चांगले होईल. किमान ~15 शब्द.",
        "text_placeholder": "उदा.: गेल्या महिनाभरापासून मला नीट झोप येत नाही, कोणत्याही कामात मन लागत नाही, "
                            "लहान गोष्टीवर चिडचिड होते आणि दिवसभर थकवा जाणवतो...",
        "text_submit": "माझे वर्णन तपासा",
        "text_note": "टीप: हे तुमचा मजकूर कीवर्ड-आधारित विश्लेषकाने वाचते. काही गोष्टी सुटू शकतात. "
                     "निकालानंतर तुम्ही प्रश्नावली उघडून ते अधिक अचूक करू शकता.",
        "result_eyebrow": "तपासणी निकाल",
        "again": "पुन्हा तपासणी करा",
        "symptom_areas": "लक्षण क्षेत्रे",
        "top_symptoms": "सर्वात ठळक लक्षणे",
        "no_symptoms": "कोणतेही लक्षण वारंवार नोंदवले गेले नाही.",
        "detected_title": "तुमच्या मजकुरातून जे समजले",
        "detected_none": "तुमच्या मजकुरातून स्पष्ट लक्षणे ओळखता आली नाहीत. विश्वसनीय निकालासाठी कृपया प्रश्नावली भरा.",
        "detected_hint": "इथे काही चुकीचे किंवा सुटलेले असेल, तर प्रश्नावली भरा — ती अधिक अचूक आहे.",
        "ml_opinion": "ML मॉडेलचे मत",
        "low_conf": "कमी विश्वास",
        "model_info": "मॉडेल माहिती",
        "crisis_title": "तुम्हाला आत्ताच मदत मिळू शकते",
        "crisis_small": "धोका तात्काळ असेल, तर 112 वर कॉल करा किंवा विश्वासू व्यक्तीकडे जा.",
        "disclaimer": "हे एक तपासणी साधन आहे, वैद्यकीय निदान नव्हे. हे पात्र डॉक्टर किंवा मानसिक आरोग्य "
                      "तज्ज्ञाची जागा घेऊ शकत नाही.",
        "footer": "कधीही स्वतःला इजा करण्याचे विचार आले तर —",
        "footer_tail": "दोन्ही 24x7, विनामूल्य",
        "lang_label": "भाषा",
        "err_short": "कृपया थोडे अधिक लिहा — किमान 15 शब्द — जेणेकरून विश्लेषण अर्थपूर्ण होईल.",
    },
    "hinglish": {
        "title": "Mental Health Screening System",
        "subtitle": "14-item symptom check based on validated screening instruments (PHQ-9 / GAD-7 style)",
        "notice_strong": "Yeh ek screening tool hai, diagnosis nahi.",
        "notice": "Iska result kisi doctor ya mental health professional ki raay ki jagah nahi le sakta. "
                  "Agar aap pareshaani mehsoos kar rahe hain, please kisi professional se baat karein.",
        "tab_quiz": "Questionnaire",
        "tab_text": "Apne shabdon me batayein",
        "form_title": "Pichhle 2 hafton me aapne ye kitni baar mehsoos kiya?",
        "form_sub": "Har sawaal ka ek option chunein. Saare 14 zaroori hain.",
        "form_title_again": "Phir se bharein",
        "submit": "Result dekhein",
        "clear": "Clear",
        "text_title": "Bataiye aap kis daur se guzar rahe hain",
        "text_sub": "Hindi, Marathi, English ya Hinglish - kisi me bhi khul kar likhein. Jitna detail "
                    "denge, analysis utna behtar hoga. Kam se kam ~15 words.",
        "text_placeholder": "Jaise: pichhle ek mahine se mujhe theek se neend nahi aati, kisi kaam me "
                            "mann nahi lagta, chhoti baat par chid jaata hoon aur din bhar thakaan rehti hai...",
        "text_submit": "Mera description analyse karein",
        "text_note": "Note: yeh aapke text ko keyword-based analyser se padhta hai. Kuch cheezein chhoot "
                     "sakti hain. Result ke baad aap questionnaire khol kar ise behtar kar sakte hain.",
        "result_eyebrow": "Screening result",
        "again": "Dobara test karein",
        "symptom_areas": "Symptom areas",
        "top_symptoms": "Sabse prominent symptoms",
        "no_symptoms": "Koi symptom frequently report nahi hua.",
        "detected_title": "Aapke text se jo samajh aaya",
        "detected_none": "Aapke text se specific symptoms clearly pakad nahi paaye. Bharosemand result "
                         "ke liye please questionnaire bharein.",
        "detected_hint": "Agar yahan kuch galat ya chhoot gaya hai, to questionnaire bharein - woh zyada accurate hai.",
        "ml_opinion": "ML model ki raay",
        "low_conf": "low confidence",
        "model_info": "Model information",
        "crisis_title": "Aapko abhi support mil sakta hai",
        "crisis_small": "Agar khatra turant hai, to 112 par call karein ya kisi bharose ke insaan ke paas jaayein.",
        "disclaimer": "Yeh ek screening tool hai, medical diagnosis nahi. Yeh kisi qualified doctor ya "
                      "mental health professional ki jagah nahi le sakta.",
        "footer": "Agar kabhi bhi aapko khud ko nuksaan pahunchane ke vichaar aayein —",
        "footer_tail": "dono 24x7, free",
        "lang_label": "Language",
        "err_short": "Please thoda aur likhein - kam se kam 15 words - taaki analysis meaningful ho.",
    },
}

# ---------------------------------------------------------------------------
# Crisis resources (contact numbers same, descriptions translated)
# ---------------------------------------------------------------------------

CRISIS_TEXT: Dict[str, list] = {
    "en": [
        ("Tele-MANAS (Govt. of India, 24x7, multi-language)", "14416 / 1-800-891-4416"),
        ("KIRAN Mental Health Helpline (24x7)", "1800-599-0019"),
        ("AASRA (24x7)", "+91-9820466726"),
        ("Vandrevala Foundation (24x7)", "+91-9999666555"),
        ("Emergency services", "112"),
    ],
    "hi": [
        ("टेली-मानस (भारत सरकार, 24x7, कई भाषाएँ)", "14416 / 1-800-891-4416"),
        ("किरण मानसिक स्वास्थ्य हेल्पलाइन (24x7)", "1800-599-0019"),
        ("आसरा (24x7)", "+91-9820466726"),
        ("वंद्रेवाला फाउंडेशन (24x7)", "+91-9999666555"),
        ("आपातकालीन सेवाएँ", "112"),
    ],
    "mr": [
        ("टेली-मानस (भारत सरकार, 24x7, अनेक भाषा)", "14416 / 1-800-891-4416"),
        ("किरण मानसिक आरोग्य हेल्पलाइन (24x7)", "1800-599-0019"),
        ("आसरा (24x7)", "+91-9820466726"),
        ("वंद्रेवाला फाउंडेशन (24x7)", "+91-9999666555"),
        ("आपत्कालीन सेवा", "112"),
    ],
    "hinglish": [
        ("Tele-MANAS (Govt. of India, 24x7, multi-language)", "14416 / 1-800-891-4416"),
        ("KIRAN Mental Health Helpline (24x7)", "1800-599-0019"),
        ("AASRA (24x7)", "+91-9820466726"),
        ("Vandrevala Foundation (24x7)", "+91-9999666555"),
        ("Emergency services", "112"),
    ],
}

CRISIS_REASON: Dict[str, str] = {
    "en": "You mentioned thoughts of not being here or of hurting yourself. Whatever the score "
          "says, it is important to get support for this right away.",
    "hi": "आपने ऐसे विचारों का ज़िक्र किया है जिनमें खुद को नुकसान पहुँचाना या न होना शामिल है। "
          "स्कोर चाहे जो भी हो, इस पर तुरंत सहायता लेना ज़रूरी है।",
    "mr": "तुम्ही स्वतःला इजा करण्याचे किंवा नसण्याचे विचार सांगितले आहेत. गुण काहीही असोत, "
          "यावर लगेच मदत घेणे महत्त्वाचे आहे.",
    "hinglish": "Aapne khud ko nuksaan pahunchane ya na hone wale vichaaron ka zikr kiya hai. "
                "Score chahe jo bhi ho, is par turant support lena zaroori hai.",
}


# ---------------------------------------------------------------------------
# Lookup helpers
# ---------------------------------------------------------------------------

def t(lang: str, key: str) -> str:
    lang = normalise_lang(lang)
    return UI.get(lang, UI[DEFAULT_LANG]).get(key, UI["en"].get(key, key))


def item_text(key: str, lang: str) -> str:
    lang = normalise_lang(lang)
    return ITEM_TEXT.get(key, {}).get(lang) or ITEM_TEXT.get(key, {}).get("en", key)


def option_text(value: int, lang: str) -> str:
    lang = normalise_lang(lang)
    return OPTION_TEXT[value].get(lang, OPTION_TEXT[value]["en"])


def state_text(state: str, lang: str) -> str:
    lang = normalise_lang(lang)
    return STATE_TEXT.get(state, {}).get(lang, state)


def domain_text(domain: str, lang: str) -> str:
    lang = normalise_lang(lang)
    return DOMAIN_TEXT.get(domain, {}).get(lang, domain.capitalize())


def advice_text(state: str, lang: str) -> Dict[str, str]:
    lang = normalise_lang(lang)
    block = ADVICE_TEXT.get(state, ADVICE_TEXT["No depression"])
    return block.get(lang, block["en"])


def crisis_resources(lang: str) -> list:
    lang = normalise_lang(lang)
    rows = CRISIS_TEXT.get(lang, CRISIS_TEXT["en"])
    return [{"name": n, "contact": c} for n, c in rows]


def crisis_reason(lang: str) -> str:
    lang = normalise_lang(lang)
    return CRISIS_REASON.get(lang, CRISIS_REASON["en"])
