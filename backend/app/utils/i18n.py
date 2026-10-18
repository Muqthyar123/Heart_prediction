from flask import request

# Bilingual dictionary: English ('en') and Telugu ('te')
TRANSLATIONS = {
    "en": {
        "disclaimer": (
            "This system is intended for research and decision-support purposes. "
            "Predictions should not be considered a professional medical diagnosis."
        ),
        "lifestyle_disclaimer": (
            "This is an educational lifestyle assessment based on reported habits "
            "and does not replace a clinical cardiovascular risk calculation or doctor consultation."
        ),
        "higher_risk_label": "Higher Risk",
        "lower_risk_label": "Lower Risk",
        "moderate_risk_label": "Moderate Risk",
        "higher_risk_desc": "The model identified risk patterns associated with heart disease in the provided clinical features.",
        "lower_risk_desc": "The model did not identify strong clinical patterns associated with heart disease in the provided data.",
        "rec_activity": "Engage in at least 150 minutes of moderate aerobic exercise weekly.",
        "rec_diet": "Adopt a balanced diet rich in leafy vegetables, fruits, whole grains, and lean proteins.",
        "rec_smoking": "Avoid tobacco products and minimize exposure to secondhand smoke.",
        "rec_alcohol": "Limit alcohol consumption to moderate or zero intake.",
        "rec_sleep": "Aim for 7 to 9 hours of restorative sleep each night.",
        "rec_stress": "Practice evidence-based stress reduction techniques such as mindfulness or yoga.",
        "rec_weight": "Maintain a healthy body weight and monitor blood pressure periodically.",
        "profile_incomplete_reminder": "Your profile is incomplete. Adding emergency contact and medical history improves clinical reporting.",
        "hospital_share_notice": "Summary prepared for clinical discussion. Not a verified hospital registration.",
    },
    "te": {
        "disclaimer": (
            "ఈ వ్యవస్థ పరిశోధన మరియు నిర్ణయ మద్దతు ప్రయోజనాల కోసం మాత్రమే ఉద్దేశించబడింది. "
            "అంచనాలను అధికారిక వైద్య నిర్ధారణగా పరిగణించకూడదు."
        ),
        "lifestyle_disclaimer": (
            "ఇది జీవనశైలి ఆధారిత అవగాహన అంచనా మాత్రమే. "
            "ఇది వైద్యుల పరీక్ష లేదా క్లినికల్ గుండెజబ్బు పరీక్షను భర్తీ చేయదు."
        ),
        "higher_risk_label": "ఎక్కువ ప్రమాదం (Higher Risk)",
        "lower_risk_label": "తక్కువ ప్రమాదం (Lower Risk)",
        "moderate_risk_label": "మధ్యస్థ ప్రమాదం (Moderate Risk)",
        "higher_risk_desc": "క్లినికల్ వివరాల ఆధారంగా మోడల్ గుండెజబ్బు సంబంధిత రిస్క్ లక్షణాలను గుర్తించింది.",
        "lower_risk_desc": "అందించిన వివరాలలో మోడల్ గుండెజబ్బు రిస్క్ లక్షణాలను గుర్తించలేదు.",
        "rec_activity": "వారానికి కనీసం 150 నిమిషాల వ్యాయామం లేదా నడక అలవర్చుకోండి.",
        "rec_diet": "ఆకుకూరలు, పండ్లు మరియు సమతుల్య ఆహారాన్ని తీసుకోండి.",
        "rec_smoking": "ధూమపానం మరియు పొగాకు ఉత్పత్తులకు దూరంగా ఉండండి.",
        "rec_alcohol": "మద్యపానాన్ని నివారించండి లేదా నియంత్రించండి.",
        "rec_sleep": "రోజూ 7 నుండి 9 గంటల ప్రశాంత నిద్ర పొందండి.",
        "rec_stress": "యోగా, ప్రాణాయామం లేదా ధ్యానం ద్వారా ఒత్తిడిని తగ్గించుకోండి.",
        "rec_weight": "ఆరోగ్యకరమైన బరువును కాపాడుకోండి మరియు క్రమం తప్పకుండా బీపీని తనిఖీ చేయండి.",
        "profile_incomplete_reminder": "మీ ప్రొఫైల్ అసంపూర్తిగా ఉంది. అత్యవసర సంప్రదింపు వివరాలు మరియు వైద్య చరిత్రను జోడించండి.",
        "hospital_share_notice": "క్లినికల్ చర్చ కోసం తయారుచేసిన సారాంశం. ఇది ఆసుపత్రి రిజిస్ట్రేషన్ కాదు.",
    },
}


def get_current_language() -> str:
    """Extract preferred language from Accept-Language header or query param."""
    lang_header = request.headers.get("Accept-Language", "").lower()
    if "te" in lang_header:
        return "te"
    query_lang = request.args.get("lang", "").lower()
    if query_lang in ("te", "telugu"):
        return "te"
    return "en"


def get_text(key: str, lang: str = None) -> str:
    """Retrieve localized string for given key."""
    if not lang:
        lang = get_current_language()
    catalog = TRANSLATIONS.get(lang, TRANSLATIONS["en"])
    return catalog.get(key, TRANSLATIONS["en"].get(key, key))
