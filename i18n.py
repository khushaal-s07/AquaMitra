"""Multilingual support — Indian & world languages for AquaMitra."""

import json
import urllib.error
import urllib.parse
import urllib.request

# Language code → display name, BCP-47 speech code
LANGUAGES = {
    "en": {"name": "English", "speech": "en-IN", "native": "English"},
    "hi": {"name": "Hindi", "speech": "hi-IN", "native": "हिन्दी"},
    "ta": {"name": "Tamil", "speech": "ta-IN", "native": "தமிழ்"},
    "kn": {"name": "Kannada", "speech": "kn-IN", "native": "ಕನ್ನಡ"},
    "ml": {"name": "Malayalam", "speech": "ml-IN", "native": "മലയാളം"},
    "mr": {"name": "Marathi", "speech": "mr-IN", "native": "मराठी"},
    "bn": {"name": "Bengali", "speech": "bn-IN", "native": "বাংলা"},
    "gu": {"name": "Gujarati", "speech": "gu-IN", "native": "ગુજરાતી"},
    "pa": {"name": "Punjabi", "speech": "pa-IN", "native": "ਪੰਜਾਬੀ"},
    "or": {"name": "Odia", "speech": "or-IN", "native": "ଓଡ଼ିଆ"},
    "ur": {"name": "Urdu", "speech": "ur-IN", "native": "اردو"},
    "as": {"name": "Assamese", "speech": "as-IN", "native": "অসমীয়া"},
    "ar": {"name": "Arabic", "speech": "ar-SA", "native": "العربية"},
    "es": {"name": "Spanish", "speech": "es-ES", "native": "Español"},
    "fr": {"name": "French", "speech": "fr-FR", "native": "Français"},
    "de": {"name": "German", "speech": "de-DE", "native": "Deutsch"},
    "zh": {"name": "Chinese", "speech": "zh-CN", "native": "中文"},
    "ja": {"name": "Japanese", "speech": "ja-JP", "native": "日本語"},
    "pt": {"name": "Portuguese", "speech": "pt-BR", "native": "Português"},
    "ru": {"name": "Russian", "speech": "ru-RU", "native": "Русский"},
    "id": {"name": "Indonesian", "speech": "id-ID", "native": "Bahasa Indonesia"},
    "th": {"name": "Thai", "speech": "th-TH", "native": "ไทย"},
    "vi": {"name": "Vietnamese", "speech": "vi-VN", "native": "Tiếng Việt"},
    "ne": {"name": "Nepali", "speech": "ne-NP", "native": "नेपाली"},
    "si": {"name": "Sinhala", "speech": "si-LK", "native": "සිංහල"},
}

# UI & voice label strings per language
UI = {
    "en": {
        "app_subtitle": "Voice Pond Copilot",
        "hint": "Speak your fish problem in your own words. Get diagnosis, medicine, market prices.",
        "hint_examples": 'Tap mic — say "white spots", "not eating", or "shrimp price today"',
        "climate_title": "Climate Conditions Detected",
        "metrics_title": "Auto-Detected from Climate",
        "market_title": "Today's Market Prices",
        "fish_rates": "Fish Rates",
        "shrimp_prawn": "Shrimp / Prawn",
        "solution": "Solution",
        "medicine": "Medicine / Treatment",
        "improvements": "Improvements for Your Pond",
        "diagnosis_words": "Diagnosis from Your Words",
        "market_rates": "Today's Market Rates",
        "climate_health": "Climate Health Alert",
        "ph": "pH Level", "water_temp": "Water Temp (°C)", "do": "Dissolved O₂ (mg/L)", "salinity": "Salinity (ppt)",
        "air_temp": "Air Temp (°C)", "humidity": "Humidity (%)", "rain": "Rain Today (mm)", "wind": "Wind (km/h)",
        "welcome_voice": "Hello! AquaMitra here. Tap the microphone and describe your fish problem in your own words, or ask today's market price.",
        "you_said": "You said",
        "matched": "Matched",
        "per_kg": "/kg",
        "online": "Cloud AI", "offline": "Deep-Sea Edge",
        "choose_language": "Choose Your Language",
        "choose_state": "Select Your State",
        "choose_state_sub": "Market prices will show for your state",
        "change_language": "Change language",
        "change_state": "Change state",
    },
    "hi": {
        "app_subtitle": "आवाज़ Pond Copilot",
        "hint": "अपनी मछली की समस्या अपने शब्दों में बताएं। रोग, दवा, बाजार भाव पाएं।",
        "hint_examples": 'माइक दबाएं — "सफेद धब्बे", "खana नहीं", "झींगा की कीमत" कहें',
        "climate_title": "जलवायु स्थिति का पता चला",
        "metrics_title": "जलवायु से स्वतः पता",
        "market_title": "आज के बाजार भाव",
        "fish_rates": "मछली के भाव",
        "shrimp_prawn": "झींगा / Shrimp",
        "solution": "समाधान",
        "medicine": "दवा / इलाज",
        "improvements": "तालाब सुधार",
        "diagnosis_words": "आपके शब्दों से निदान",
        "market_rates": "आज के बाजार भाव",
        "climate_health": "जलवायु स्वास्थ्य चेतावनी",
        "ph": "pH", "water_temp": "पानी ताप (°C)", "do": "ऑक्सीजन", "salinity": "लवणता",
        "air_temp": "हवा ताप", "humidity": "नमी (%)", "rain": "बारिश (mm)", "wind": "हवा",
        "welcome_voice": "नमस्कार! AquaMitra. माइक दबाकर मछली की समस्या बताएं या आज का बाजार भाव पूछें।",
        "you_said": "आपने कहा", "matched": "मिलान", "per_kg": "/kg",
        "online": "Cloud AI", "offline": "Deep-Sea Edge",
    },
    "ta": {
        "app_subtitle": "குரல் Pond Copilot",
        "hint": "மீன் பிரச்சனையை உங்கள் வார்த்தையில் சொல்லுங்கள். நோய், மருந்து, market விலை.",
        "hint_examples": 'மைக் அழுத்துங்கள் — "வெள்ளை புள்ளி", "சாப்பிடவில்லை", "இறால் விலை"',
        "climate_title": "காலநிலை கண்டறியப்பட்டது",
        "metrics_title": "காலநிலையிலிருந்து கண்டறிதல்",
        "market_title": "இன்றைய market விலை",
        "fish_rates": "மீன் விலை", "shrimp_prawn": "இறால் / Shrimp",
        "solution": "தீர்வு", "medicine": "மருந்து / சிகிச்சை", "improvements": "குளம் மேம்பாடு",
        "diagnosis_words": "உங்கள் வார்த்தையிலிருந்து நோயறிதல்",
        "market_rates": "இன்றைய market விலை",
        "climate_health": "காலநிலை ஆரோக்கிய எச்சரிக்கை",
        "ph": "pH", "water_temp": "நீர் temp", "do": "ஆக்ஸிஜன்", "salinity": "உப்பு நிலை",
        "air_temp": "காற்று temp", "humidity": "ஈரப்பதம்", "rain": "மழை", "wind": "காற்று",
        "welcome_voice": "வணக்கம்! AquaMitra. மைக் அழுத்தி மீன் பிரச்சனை சொல்லுங்கள் அல்லது market விலை கேளுங்கள்.",
        "you_said": "நீங்கள் சொன்னது", "matched": "பொருத்தம்", "per_kg": "/kg",
        "online": "Cloud AI", "offline": "Deep-Sea Edge",
    },
}

# Fill remaining languages from English base + key translated fields via template
for code in LANGUAGES:
    if code not in UI:
        UI[code] = dict(UI["en"])
        UI[code]["native_name"] = LANGUAGES[code]["native"]

_translation_cache = {}


def normalize_lang(lang):
    if not lang:
        return "en"
    lang = lang.lower().split("-")[0]
    return lang if lang in LANGUAGES else "en"


def get_ui(lang):
    lang = normalize_lang(lang)
    base = UI.get(lang)
    if base:
        strings = dict(base)
    else:
        strings = dict(UI["en"])
        for key, val in strings.items():
            if isinstance(val, str) and key not in ("online", "offline", "per_kg"):
                strings[key] = translate_text(val, lang)
    strings["lang"] = lang
    strings["speech_code"] = LANGUAGES[lang]["speech"]
    strings["language_name"] = LANGUAGES[lang]["native"]
    return strings


def translate_text(text, target_lang, source_lang="en"):
    """Translate dynamic text (disease advice, etc.) to target language."""
    if not text or normalize_lang(target_lang) == normalize_lang(source_lang):
        return text

    target = normalize_lang(target_lang)
    cache_key = f"{source_lang}|{target}|{text[:120]}"
    if cache_key in _translation_cache:
        return _translation_cache[cache_key]

    # MyMemory free translation API
    try:
        q = urllib.parse.quote(text[:500])
        pair = f"{source_lang}|{target}"
        url = f"https://api.mymemory.translated.net/get?q={q}&langpair={pair}"
        req = urllib.request.Request(url, headers={"User-Agent": "AquaMitra/1.0"})
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode())
        translated = data.get("responseData", {}).get("translatedText", text)
        if translated and translated.lower() != text.lower():
            _translation_cache[cache_key] = translated
            return translated
    except (urllib.error.URLError, json.JSONDecodeError, KeyError):
        pass

    return text


def translate_alert(alert, lang):
    """Translate disease alert fields to target language."""
    lang = normalize_lang(lang)
    if lang == "en":
        return alert
    out = dict(alert)
    for field in ("disease", "action", "solution", "medicine", "improvements"):
        if out.get(field):
            out[field] = translate_text(out[field], lang)
    return out


def localize_market_prices(market_prices, lang):
    """Return market list in English or the user's chosen language only."""
    lang = normalize_lang(lang)
    mp = market_prices
    if lang == "en":
        return mp

    out = dict(mp)
    out["market"] = translate_text(mp["market"], lang)
    out["state_name"] = translate_text(mp["state_name"], lang)
    out["note"] = translate_text(mp["note"], lang)

    for category in ("shrimp", "fish"):
        out[category] = []
        for item in mp.get(category, []):
            entry = dict(item)
            entry["name"] = translate_text(item["name"], lang)
            out[category].append(entry)
    return out


def build_localized_voice_diagnosis(transcript, alert, metrics, lang):
    """Build voice text for disease diagnosis in farmer's language."""
    ui = get_ui(lang)
    t = lambda s: translate_text(s, lang)
    return (
        f"{t('You described')}: {transcript}. "
        f"{t('Diagnosis')}: {translate_text(alert['disease'], lang)}. "
        f"{ui['solution']}: {translate_text(alert.get('solution', alert.get('action', '')), lang)}. "
        f"{ui['medicine']}: {translate_text(alert.get('medicine', ''), lang)}. "
        f"{ui['improvements']}: {translate_text(alert.get('improvements', ''), lang)}. "
        f"pH {metrics['ph']}, {t('water temperature')} {metrics['temperature']}°C, "
        f"{t('oxygen')} {metrics['dissolved_oxygen']}, {t('salinity')} {metrics['salinity']}."
    )


def get_languages_list():
    return [{"code": k, "name": v["name"], "native": v["native"], "speech": v["speech"]}
            for k, v in LANGUAGES.items()]
