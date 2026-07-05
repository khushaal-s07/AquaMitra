#!/usr/bin/env python3
"""AquaMitra — voice-first aquaculture backend with dual-engine AI."""

import json
import os
import urllib.error
import urllib.request
from datetime import datetime

from flask import Flask, jsonify, request, send_from_directory

from treatments import enrich_alert
from i18n import (
    get_ui,
    normalize_lang,
    translate_alert,
    translate_text,
    localize_market_prices,
    build_localized_voice_diagnosis,
    get_languages_list,
)
from market_prices import (
    get_today_market_prices,
    is_price_query,
    build_price_voice_text,
    build_price_summary_short,
    get_states_list,
    normalize_state,
)

app = Flask(__name__, static_folder=".", static_url_path="")

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.0-flash")

# Andhra Pradesh coastal aquaculture belt (Nellore) — fallback when GPS unavailable
DEFAULT_LAT = 16.5142
DEFAULT_LON = 80.6325


def clamp(value, low, high):
    return max(low, min(high, value))


def fetch_climate(lat, lon):
    """Fetch live climate from Open-Meteo (free, no API key)."""
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        f"&current=temperature_2m,relative_humidity_2m,precipitation,cloud_cover,wind_speed_10m"
        f"&daily=precipitation_sum"
        f"&timezone=Asia%2FKolkata&forecast_days=1"
    )
    req = urllib.request.Request(url, headers={"User-Agent": "AquaMitra/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=12) as resp:
            data = json.loads(resp.read().decode())
        current = data.get("current", {})
        daily = data.get("daily", {})
        rain_today = 0.0
        if daily.get("precipitation_sum"):
            rain_today = daily["precipitation_sum"][0] or 0.0

        return {
            "air_temperature": current.get("temperature_2m", 30.0),
            "humidity": current.get("relative_humidity_2m", 70.0),
            "rain_now": current.get("precipitation", 0.0) or 0.0,
            "rain_today_mm": rain_today,
            "cloud_cover": current.get("cloud_cover", 50.0),
            "wind_speed_kmh": current.get("wind_speed_10m", 8.0),
            "latitude": lat,
            "longitude": lon,
            "source": "Open-Meteo live climate",
        }
    except (urllib.error.URLError, json.JSONDecodeError, KeyError):
        return fallback_climate(lat, lon)


def fallback_climate(lat, lon):
    """Seasonal climate model for AP coast when weather API is unreachable."""
    month = datetime.now().month
    hour = datetime.now().hour

    if month in (3, 4, 5):
        air_temp, humidity, rain, wind = 34.0, 55.0, 0.0, 12.0
        season = "pre-monsoon heat"
    elif month in (6, 7, 8, 9):
        air_temp, humidity, rain, wind = 29.0, 82.0, 8.0, 10.0
        season = "monsoon"
    elif month in (10, 11):
        air_temp, humidity, rain, wind = 31.0, 68.0, 2.0, 9.0
        season = "post-monsoon"
    else:
        air_temp, humidity, rain, wind = 27.0, 60.0, 0.0, 7.0
        season = "winter"

    if hour >= 18 or hour <= 6:
        air_temp -= 2.5

    return {
        "air_temperature": air_temp,
        "humidity": humidity,
        "rain_now": rain,
        "rain_today_mm": rain,
        "cloud_cover": 60.0 if rain > 0 else 25.0,
        "wind_speed_kmh": wind,
        "latitude": lat,
        "longitude": lon,
        "source": f"Seasonal edge model ({season})",
    }


def infer_pond_metrics_from_climate(climate):
    """
    Derive pond water parameters from climate conditions.

    Models used:
    - Water temp  : air temp + solar pond-heating offset
    - Salinity    : base coastal ppt, reduced by rain, increased by evaporation
    - pH          : photosynthesis (cloud/sun), rain acidity, salinity correlation
    - Dissolved O2: temperature saturation curve + wind aeration + daytime algae O2
    """
    air_temp = climate["air_temperature"]
    humidity = climate["humidity"]
    rain = climate["rain_now"] + climate["rain_today_mm"] * 0.3
    cloud = climate["cloud_cover"]
    wind = climate["wind_speed_kmh"]
    month = datetime.now().month
    hour = datetime.now().hour

    solar_factor = (100 - cloud) / 100

    # ── Water Temperature ──────────────────────────────────────────────
    # Pond surface absorbs solar radiation; lags air by ~1–3 °C depending on cloud
    water_temp = air_temp + 1.0 + solar_factor * 2.8
    if rain > 5:
        water_temp -= 1.5  # heavy rain cools pond surface
    water_temp = round(clamp(water_temp, 24.0, 36.0), 1)

    # ── Salinity (ppt) ───────────────────────────────────────────────────
    base_salinity = 22.0  # typical AP brackish vannamei pond
    if month in (6, 7, 8, 9):
        base_salinity -= 4.0   # monsoon freshwater inflow
    elif month in (4, 5):
        base_salinity += 2.0   # pre-monsoon evaporation peak

    salinity = base_salinity
    salinity -= rain * 0.18                          # rainfall dilution
    evap_boost = max(0, (air_temp - 28) * 0.12)     # heat evaporation
    evap_boost += max(0, (100 - humidity) * 0.025)   # dry air evaporation
    evap_boost += wind * 0.04                        # wind-driven evaporation
    salinity += evap_boost
    salinity = round(clamp(salinity, 5.0, 38.0), 1)

    # ── pH ─────────────────────────────────────────────────────────────
    base_ph = 7.75
    if 8 <= hour <= 17:
        base_ph += solar_factor * 0.45   # daytime algal photosynthesis raises pH
    else:
        base_ph -= 0.25                  # nighttime CO2 respiration lowers pH
    base_ph -= rain * 0.025              # acidic rain / runoff lowers pH
    base_ph += (salinity - 20) * 0.007   # higher ionic strength → slightly higher pH
    if humidity > 85 and rain > 3:
        base_ph -= 0.15                    # anaerobic conditions during heavy rain
    ph = round(clamp(base_ph, 6.8, 9.0), 1)

    # ── Dissolved Oxygen (mg/L) ─────────────────────────────────────────
    # Benson-Krause style saturation at given water temperature
    t = water_temp
    do_sat = 14.652 - 0.41022 * t + 0.007991 * t ** 2 - 0.000077774 * t ** 3

    aeration_factor = 0.58 + min(wind * 0.025, 0.25)   # wind-driven surface reaeration
    if 9 <= hour <= 16:
        aeration_factor += solar_factor * 0.22          # algal O2 production in daylight
    if rain > 8:
        aeration_factor -= 0.12                         # overcast + stratification after heavy rain
    if air_temp > 33:
        aeration_factor -= 0.08                         # thermal stratification in extreme heat

    dissolved_oxygen = do_sat * clamp(aeration_factor, 0.35, 1.05)
    dissolved_oxygen = round(clamp(dissolved_oxygen, 2.0, 9.0), 1)

    detection = {
        "ph": (
            f"Climate-detected from rain ({rain:.1f} mm), cloud cover ({cloud:.0f}%), "
            f"humidity ({humidity:.0f}%) & time of day"
        ),
        "salinity": (
            f"Climate-detected from rain dilution ({rain:.1f} mm), air temp ({air_temp}°C), "
            f"humidity ({humidity}%) & wind ({wind} km/h)"
        ),
        "water_temperature": (
            f"Climate-detected from air temp ({air_temp}°C), sun/cloud cover ({cloud:.0f}%) "
            f"& rain cooling"
        ),
        "dissolved_oxygen": (
            f"Climate-detected from water temp ({water_temp}°C), wind aeration ({wind} km/h) "
            f"& daylight algae oxygen"
        ),
        "air_temperature": air_temp,
    }

    return {
        "ph": ph,
        "salinity": salinity,
        "temperature": water_temp,
        "dissolved_oxygen": dissolved_oxygen,
        "detection": detection,
    }


def get_climate_and_metrics(lat=None, lon=None):
    lat = float(lat) if lat is not None else DEFAULT_LAT
    lon = float(lon) if lon is not None else DEFAULT_LON
    climate = fetch_climate(lat, lon)
    result = infer_pond_metrics_from_climate(climate)
    detection = result.pop("detection")
    metrics = result
    return climate, metrics, detection


def normalize_text(text):
    return (text or "").lower().strip()


from symptoms import FARMER_SYMPTOM_RULES

def diagnose_from_farmer_words(transcript):
    """Match farmer's own words to fish/shrimp diseases."""
    if not transcript or len(transcript.strip()) < 3:
        return []

    text = normalize_text(transcript)
    matched = []

    for rule in FARMER_SYMPTOM_RULES:
        for keyword in rule["keywords"]:
            if keyword.lower() in text:
                matched.append(enrich_alert({
                    "disease": rule["disease"],
                    "severity": rule["severity"],
                    "action": rule["action"],
                    "matched_symptom": keyword,
                    "source": "farmer_words",
                }))
                break

    # Deduplicate by disease name, keep highest severity
    seen = {}
    severity_rank = {"critical": 4, "high": 3, "medium": 2, "ok": 1}
    for alert in matched:
        name = alert["disease"]
        if name not in seen or severity_rank.get(alert["severity"], 0) > severity_rank.get(seen[name]["severity"], 0):
            seen[name] = alert

    results = list(seen.values())
    results.sort(key=lambda a: severity_rank.get(a["severity"], 0), reverse=True)
    return results


def merge_alerts(climate_alerts, word_alerts):
    """Combine climate-based and farmer-word disease alerts."""
    if word_alerts:
        # Farmer description takes priority; add climate alerts that aren't "ok"
        combined = word_alerts[:]
        for ca in climate_alerts:
            if ca["severity"] != "ok" and ca["disease"] not in {a["disease"] for a in combined}:
                combined.append(enrich_alert(dict(ca, source="climate")))
        return combined
    return climate_alerts


def build_voice_report(metrics, alerts, climate=None, detection=None, transcript=None, engine="edge", lang="en", state="AP"):
    """Plain-text script optimized for text-to-speech."""
    ui = get_ui(lang)
    primary = translate_alert(alerts[0], lang)
    extra = ""
    if len(alerts) > 1 and alerts[0]["severity"] != "ok":
        extra = " " + translate_text(f"Also possible: {alerts[1]['disease']}.", lang)

    if transcript:
        return build_localized_voice_diagnosis(transcript, primary, metrics, lang) + extra

    climate_note = ""
    if climate:
        climate_note = translate_text(
            f" Air temperature {climate['air_temperature']} degrees, humidity {climate['humidity']} percent. "
            f"pH {metrics['ph']}, water temperature {metrics['temperature']}, "
            f"oxygen {metrics['dissolved_oxygen']}, salinity {metrics['salinity']}. ",
            lang,
        )

    return ui["welcome_voice"] + climate_note + " " + translate_text(
        build_price_summary_short(get_today_market_prices(state)), lang
    )


def diagnose_diseases(metrics):
    """Rule-based disease & stress detection from climate-derived water metrics."""
    alerts = []

    if metrics["ph"] < 7.5:
        alerts.append({
            "disease": "Acidosis Stress / White Feces Syndrome risk",
            "severity": "high",
            "action": "Apply agricultural lime 20 kg per acre within 6 hours.",
            "source": "climate",
        })
    elif metrics["ph"] > 8.3:
        alerts.append({
            "disease": "Alkalosis — Gill damage risk",
            "severity": "medium",
            "action": "Stop lime. Increase partial water exchange.",
            "source": "climate",
        })

    if metrics["salinity"] > 32:
        alerts.append({
            "disease": "Salinity Stress — EHP vulnerability",
            "severity": "medium",
            "action": "Add fresh water. Reduce feed by 20 percent.",
            "source": "climate",
        })
    elif metrics["salinity"] < 12:
        alerts.append({
            "disease": "Low salinity osmotic shock",
            "severity": "high",
            "action": "Add brackish water immediately. Target 20 ppt.",
            "source": "climate",
        })

    if metrics["dissolved_oxygen"] < 4.0:
        alerts.append({
            "disease": "Hypoxia — Early Mortality Syndrome (EMS) risk",
            "severity": "critical",
            "action": "Run all aerators now. Stop feeding for 24 hours.",
            "source": "climate",
        })

    if metrics["temperature"] > 31:
        alerts.append({
            "disease": "Thermal stress — White Spot Syndrome (WSSV) trigger",
            "severity": "high",
            "action": "Increase aeration. Add pond shade. Reduce stocking density stress.",
            "source": "climate",
        })

    if not alerts:
        alerts.append(enrich_alert({
            "disease": "No active disease detected",
            "severity": "ok",
            "action": "Continue routine monitoring and probiotic feeding schedule.",
            "source": "climate",
        }))

    return [enrich_alert(a) for a in alerts]


def call_gemini(prompt):
    if not GEMINI_API_KEY:
        return None

    url = (
        f"https://generativelanguage.googleapis.com/v1beta/models/"
        f"{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"
    )
    payload = json.dumps({"contents": [{"parts": [{"text": prompt}]}]}).encode()
    req = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode())
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except (urllib.error.URLError, KeyError, IndexError, json.JSONDecodeError):
        return None


@app.route("/")
def home():
    return send_from_directory(".", "index.html")


@app.route("/<path:filename>")
def static_files(filename):
    allowed = {"manifest.json", "sw.js", "favicon.ico"}
    if filename in allowed:
        return send_from_directory(".", filename)
    return jsonify({"error": "Not found"}), 404


@app.route("/api/states", methods=["GET"])
def states():
    return jsonify({"states": get_states_list()})


@app.route("/api/languages", methods=["GET"])
def languages():
    return jsonify({"languages": get_languages_list()})


@app.route("/api/ui-strings", methods=["GET"])
def ui_strings():
    lang = request.args.get("lang", "en")
    return jsonify(get_ui(lang))


@app.route("/api/pond-status", methods=["GET"])
def pond_status():
    online = request.args.get("online", "true").lower() != "false"
    lat = request.args.get("lat", type=float)
    lon = request.args.get("lon", type=float)
    lang = normalize_lang(request.args.get("lang", "en"))
    state = normalize_state(request.args.get("state"))

    climate, metrics, detection = get_climate_and_metrics(lat, lon)
    climate_alerts = [translate_alert(a, lang) for a in diagnose_diseases(metrics)]
    alerts = climate_alerts
    raw_market = get_today_market_prices(state)
    market_prices = localize_market_prices(raw_market, lang)
    engine = "cloud" if online and GEMINI_API_KEY else "edge"
    ui = get_ui(lang)

    voice_text = build_voice_report(metrics, alerts, climate, detection, None, engine, lang, state)

    if engine == "cloud":
        gemini_voice = call_gemini(
            f"""You are AquaMitra aquaculture voice assistant. Reply in language '{lang}'.
Speak pond data clearly (max 110 words).
Climate: air {climate['air_temperature']}°C, humidity {climate['humidity']}%, rain {climate['rain_today_mm']}mm.
Pond: pH {metrics['ph']}, Salinity {metrics['salinity']} ppt, Temp {metrics['temperature']}°C, DO {metrics['dissolved_oxygen']} mg/L.
State market: {market_prices['state_name']}. Disease: {alerts[0]['disease']}. Action: {alerts[0]['action']}.
Plain spoken sentences only, no markdown."""
        )
        if gemini_voice:
            voice_text = gemini_voice.strip()

    return jsonify({
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "engine": engine,
        "lang": lang,
        "state": state,
        "ui": ui,
        "climate": climate,
        "detection": detection,
        "metrics": metrics,
        "alerts": alerts,
        "market_prices": market_prices,
        "voice_text": voice_text,
    })


@app.route("/api/voice-query", methods=["POST"])
def voice_query():
    body = request.get_json(silent=True) or {}
    transcript = (body.get("transcript") or "").strip()
    online = body.get("online", True)
    lat = body.get("lat")
    lon = body.get("lon")
    lang = normalize_lang(body.get("lang", "en"))
    state = normalize_state(body.get("state"))

    climate, metrics, detection = get_climate_and_metrics(lat, lon)
    climate_alerts = diagnose_diseases(metrics)
    word_alerts = diagnose_from_farmer_words(transcript)
    raw_market = get_today_market_prices(state)
    market_prices = localize_market_prices(raw_market, lang)
    engine = "cloud" if online and GEMINI_API_KEY else "edge"
    ui = get_ui(lang)

    if is_price_query(transcript):
        base_voice = build_price_voice_text(raw_market, transcript)
        voice_text = base_voice if lang == "en" else translate_text(base_voice, lang)
        alerts = [translate_alert(enrich_alert({
            "disease": "Market Price Query",
            "severity": "ok",
            "action": market_prices["note"],
            "source": "market",
            "solution": f"Best shrimp in {market_prices['state_name']}: {market_prices['shrimp'][2]['name']} at ₹{market_prices['shrimp'][2]['price']}/kg.",
            "medicine": "Contact local commission agent to lock harvest rate before selling.",
            "improvements": "Harvest when count matches highest price bracket. Monitor daily rates before selling.",
        }), lang)]
    elif word_alerts:
        alerts = [translate_alert(a, lang) for a in merge_alerts(climate_alerts, word_alerts)]
    elif transcript:
        alerts = [translate_alert(enrich_alert({
            "disease": "Symptoms unclear — need more description",
            "severity": "medium",
            "action": "Please describe: white spots, floating, not eating, red color, or dead fish.",
            "source": "farmer_words",
        }), lang)]
    else:
        alerts = [translate_alert(a, lang) for a in climate_alerts]

    if is_price_query(transcript):
        pass
    elif transcript and engine == "cloud":
        gemini_voice = call_gemini(
            f"""You are AquaMitra voice assistant. Reply ONLY in language code '{lang}' ({ui['language_name']}).
Farmer said: "{transcript}"
Diagnosis: {alerts[0]['disease']}. Solution: {alerts[0].get('solution','')}. Medicine: {alerts[0].get('medicine','')}.
Pond: pH {metrics['ph']}, Temp {metrics['temperature']}°C, DO {metrics['dissolved_oxygen']}, Salinity {metrics['salinity']}.
Spoken voice reply, max 90 words. No markdown."""
        )
        voice_text = gemini_voice.strip() if gemini_voice else build_voice_report(
            metrics, alerts, climate, detection, transcript, engine, lang, state
        )
    elif transcript:
        voice_text = build_voice_report(metrics, alerts, climate, detection, transcript, engine, lang, state)
    else:
        voice_text = build_voice_report(metrics, alerts, climate, detection, None, engine, lang, state)

    return jsonify({
        "engine": engine,
        "lang": lang,
        "state": state,
        "ui": ui,
        "climate": climate,
        "detection": detection,
        "transcript": transcript,
        "farmer_diagnosis": word_alerts,
        "metrics": metrics,
        "alerts": alerts,
        "market_prices": market_prices,
        "voice_text": voice_text,
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    print(f"\n🌊 AquaMitra Voice Copilot running at http://localhost:{port}\n")
    app.run(host="0.0.0.0", port=port, debug=False)
