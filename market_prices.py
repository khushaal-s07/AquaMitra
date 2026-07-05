"""State-wise fish & shrimp market prices for Indian aquaculture."""

from datetime import datetime


BASE_CATALOG = {
    "shrimp": [
        {"name": "Vannamei 30 count", "base": 400},
        {"name": "Vannamei 40 count", "base": 340},
        {"name": "Vannamei 50 count", "base": 300},
        {"name": "Vannamei 60 count", "base": 270},
        {"name": "Vannamei 80 count", "base": 240},
        {"name": "Vannamei 100 count", "base": 210},
        {"name": "Tiger Prawns", "base": 450},
    ],
    "fish": [
        {"name": "Rohu", "base": 200},
        {"name": "Catla", "base": 190},
        {"name": "Pangasius (Basa)", "base": 140},
        {"name": "Tilapia", "base": 160},
        {"name": "Milkfish", "base": 225},
        {"name": "Seabass (Barramundi)", "base": 350},
    ],
}

# State profiles: price multiplier + primary market hub + specialty fish adjustments
INDIAN_STATES = {
    "AP": {
        "name": "Andhra Pradesh",
        "hub": "Nellore",
        "multiplier": 1.00,
        "specialty": {"Tiger Prawns": 460, "Rohu": 195},
    },
    "TN": {
        "name": "Tamil Nadu",
        "hub": "Nagapattinam",
        "multiplier": 1.06,
        "specialty": {"Seabass (Barramundi)": 380, "Tiger Prawns": 470, "Vannamei 50 count": 310},
    },
    "KL": {
        "name": "Kerala",
        "hub": "Kochi",
        "multiplier": 1.10,
        "specialty": {"Seabass (Barramundi)": 400, "Milkfish": 250, "Tiger Prawns": 480},
    },
    "OR": {
        "name": "Odisha",
        "hub": "Paradeep",
        "multiplier": 0.95,
        "specialty": {"Vannamei 60 count": 255, "Rohu": 185, "Catla": 175},
    },
    "WB": {
        "name": "West Bengal",
        "hub": "Kolkata",
        "multiplier": 1.02,
        "specialty": {"Rohu": 230, "Catla": 220, "Pangasius (Basa)": 130},
        "extra_fish": [{"name": "Hilsa (Ilish)", "base": 1200}],
    },
    "GJ": {
        "name": "Gujarat",
        "hub": "Porbandar",
        "multiplier": 1.04,
        "specialty": {"Vannamei 40 count": 355, "Pangasius (Basa)": 150},
    },
    "MH": {
        "name": "Maharashtra",
        "hub": "Mumbai",
        "multiplier": 1.08,
        "specialty": {"Seabass (Barramundi)": 390, "Vannamei 30 count": 420},
    },
    "KA": {
        "name": "Karnataka",
        "hub": "Mangalore",
        "multiplier": 1.03,
        "specialty": {"Seabass (Barramundi)": 365, "Milkfish": 235},
    },
    "GA": {
        "name": "Goa",
        "hub": "Margao",
        "multiplier": 1.12,
        "specialty": {"Tiger Prawns": 500, "Seabass (Barramundi)": 410},
    },
    "PB": {
        "name": "Punjab",
        "hub": "Amritsar",
        "multiplier": 0.92,
        "specialty": {"Rohu": 210, "Catla": 200, "Tilapia": 170},
        "extra_fish": [{"name": "Singhi (Stinging Catfish)", "base": 280}],
    },
    "UP": {
        "name": "Uttar Pradesh",
        "hub": "Lucknow",
        "multiplier": 0.90,
        "specialty": {"Rohu": 205, "Catla": 195, "Pangasius (Basa)": 135},
    },
    "BR": {
        "name": "Bihar",
        "hub": "Patna",
        "multiplier": 0.88,
        "specialty": {"Rohu": 190, "Catla": 180},
    },
    "AS": {
        "name": "Assam",
        "hub": "Guwahati",
        "multiplier": 0.93,
        "specialty": {"Rohu": 200, "Catla": 185},
        "extra_fish": [{"name": "Magur (Walking Catfish)", "base": 320}],
    },
    "TR": {
        "name": "Tripura",
        "hub": "Agartala",
        "multiplier": 0.91,
        "specialty": {"Rohu": 188, "Tilapia": 155},
    },
    "CG": {
        "name": "Chhattisgarh",
        "hub": "Raipur",
        "multiplier": 0.89,
        "specialty": {"Rohu": 185, "Catla": 175},
    },
}

DEFAULT_STATE = "AP"

PRICE_KEYWORDS = [
    "price", "prices", "rate", "rates", "market", "sell", "selling", "cost",
    "bhav", "bhaav", "dam", "dar", "how much", "today", "mrp", "value", "worth",
    "buy", "purchase", "shrimp price", "fish price", "prawn price",
]


def normalize_state(state_code):
    code = (state_code or DEFAULT_STATE).upper()
    return code if code in INDIAN_STATES else DEFAULT_STATE


def get_states_list():
    return [
        {"code": code, "name": info["name"], "hub": info["hub"]}
        for code, info in INDIAN_STATES.items()
    ]


def _daily_drift(base, seed):
    day = datetime.now().timetuple().tm_yday
    drift = ((day * seed) % 11 - 5) / 100
    return round(base * (1 + drift))


def _item_base(state_info, item_name, default_base):
    specialty = state_info.get("specialty", {})
    if item_name in specialty:
        return specialty[item_name]
    return round(default_base * state_info["multiplier"])


def get_today_market_prices(state_code=None):
    state_code = normalize_state(state_code)
    state_info = INDIAN_STATES[state_code]
    today = datetime.now().strftime("%d %B %Y")

    shrimp = []
    for i, item in enumerate(BASE_CATALOG["shrimp"]):
        base = _item_base(state_info, item["name"], item["base"])
        price = _daily_drift(base, i + 3)
        shrimp.append({
            "name": item["name"],
            "price": price,
            "unit": "₹/kg",
            "trend": "up" if price > base else "down" if price < base else "stable",
        })

    fish = []
    all_fish = list(BASE_CATALOG["fish"]) + state_info.get("extra_fish", [])
    for i, item in enumerate(all_fish):
        base = _item_base(state_info, item["name"], item["base"])
        price = _daily_drift(base, i + 11)
        fish.append({
            "name": item["name"],
            "price": price,
            "unit": "₹/kg",
            "trend": "up" if price > base else "down" if price < base else "stable",
        })

    return {
        "date": today,
        "state": state_code,
        "state_name": state_info["name"],
        "market": f"{state_info['hub']} Fish Market, {state_info['name']}",
        "currency": "INR",
        "shrimp": shrimp,
        "fish": fish,
        "note": f"Indicative {state_info['name']} farm-gate prices. Confirm with local agent before selling.",
    }


def is_price_query(transcript):
    if not transcript:
        return False
    text = transcript.lower()
    return any(kw in text for kw in PRICE_KEYWORDS)


def find_price_for_query(transcript, market_prices):
    text = transcript.lower()
    matches = []
    for category in ("shrimp", "fish"):
        for item in market_prices[category]:
            names = [item["name"].lower()]
            for part in item["name"].lower().replace("(", " ").replace(")", " ").split():
                if len(part) > 3:
                    names.append(part)
            if any(n in text for n in names if n):
                matches.append(item)
    return matches


def build_price_voice_text(market_prices, transcript=None):
    mp = market_prices
    specific = find_price_for_query(transcript, mp) if transcript else []

    if specific:
        item = specific[0]
        return (
            f"Today's market price in {mp['state_name']} for {item['name']} is "
            f"{item['price']} rupees per kilogram at {mp['market']}. Date: {mp['date']}. {mp['note']}"
        )

    top_shrimp = mp["shrimp"][2]
    parts = [
        f"Today is {mp['date']}. Fish market prices for {mp['state_name']} from {mp['market']}. ",
        "Shrimp prices today: ",
    ]
    for s in mp["shrimp"][:4]:
        parts.append(f"{s['name']} {s['price']} rupees per kg. ")
    parts.append(
        f"Fish prices: Rohu {mp['fish'][0]['price']}, Catla {mp['fish'][1]['price']}, "
        f"Pangasius {mp['fish'][2]['price']}, Tilapia {mp['fish'][3]['price']} rupees per kg. "
        f"Best shrimp rate is {top_shrimp['name']} at {top_shrimp['price']} rupees. {mp['note']}"
    )
    return "".join(parts)


def build_price_summary_short(market_prices):
    mp = market_prices
    return (
        f"Today's {mp['state_name']} market at {mp['market']}: "
        f"Vannamei 50 count {mp['shrimp'][2]['price']} rupees per kg, "
        f"Rohu {mp['fish'][0]['price']}, Catla {mp['fish'][1]['price']}, "
        f"Pangasius {mp['fish'][2]['price']} rupees per kg."
    )
