# Clean symptom rules — English keywords only, no Telugu

FARMER_SYMPTOM_RULES = [
    {
        "keywords": ["white spot", "white spots", "white patch", "spots on", "white dots", "white on shrimp", "white on fish", "white colour", "white color"],
        "disease": "White Spot Syndrome (WSSV)",
        "severity": "critical",
        "action": "Stop feeding immediately. Increase aeration. Apply probiotics. Consult aqua doctor for WSSV test.",
    },
    {
        "keywords": ["white feces", "white faeces", "white poop", "white stool", "white gut", "white waste", "white fecal"],
        "disease": "White Feces Syndrome / EHP",
        "severity": "high",
        "action": "Reduce feed 30%. Add gut probiotics and lime. Check for EHP with lab test.",
    },
    {
        "keywords": ["dying", "dead", "mortality", "sudden death", "dying fast", "mass death", "lots of dead", "found dead", "ems"],
        "disease": "Early Mortality Syndrome (EMS / AHPND)",
        "severity": "critical",
        "action": "Stop feeding 48 hours. Emergency aeration. Partial water exchange. Isolate affected pond.",
    },
    {
        "keywords": ["floating", "surface", "top of water", "gasping", "piping", "mouth open", "swimming top", "float", "gills open"],
        "disease": "Hypoxia — Low Oxygen Stress",
        "severity": "critical",
        "action": "Run all aerators immediately. Stop feeding. Emergency water exchange if possible.",
    },
    {
        "keywords": ["not eating", "no feed", "feed not taken", "stopped eating", "refuse feed", "feed waste", "uneaten feed"],
        "disease": "Feed Refusal / Internal Bacterial Infection",
        "severity": "high",
        "action": "Reduce feed 50%. Check water quality. Add vitamin C and probiotics to feed.",
    },
    {
        "keywords": ["red body", "red color", "red colour", "red shrimp", "reddish", "red gill", "turned red"],
        "disease": "Red Body Syndrome / Toxicity Stress",
        "severity": "high",
        "action": "Check for ammonia and nitrite. Stop chemicals. Water exchange 20%. Add activated carbon.",
    },
    {
        "keywords": ["soft shell", "molting problem", "molt", "shell problem", "weak shell", "shell soft", "molting", "soft body"],
        "disease": "Soft Shell / Molting Disorder",
        "severity": "medium",
        "action": "Add mineral supplements and calcium. Check alkalinity. Reduce stress and handling.",
    },
    {
        "keywords": ["black gill", "gill rot", "gill problem", "gills black", "gill damage", "gill fungus", "gills brown", "gill"],
        "disease": "Black Gill Disease / Gill Rot",
        "severity": "high",
        "action": "Improve aeration. Reduce organic load. Apply formalin bath under expert guidance.",
    },
    {
        "keywords": ["green water", "algae", "algae bloom", "water green", "dirty water", "green colour", "bloom"],
        "disease": "Algal Bloom — Oxygen Crash Risk",
        "severity": "medium",
        "action": "Reduce sunlight. Use zeolite. Increase aeration at night. Avoid overfeeding.",
    },
    {
        "keywords": ["slow growth", "not growing", "small size", "stunted", "growth slow", "growth"],
        "disease": "Slow Growth — EHP / Nutritional Deficiency",
        "severity": "medium",
        "action": "Check feed quality. Test for EHP. Add vitamins and improve water exchange.",
    },
    {
        "keywords": ["fin rot", "tail rot", "rotting", "fungus", "cotton like", "white fungus", "fin damage", "tail damage"],
        "disease": "Fin Rot / Fungal Infection",
        "severity": "medium",
        "action": "Salt bath 5 ppt for 1 hour. Improve water quality. Reduce stocking density.",
    },
    {
        "keywords": ["swollen", "bloated", "big belly", "dropsy", "swelling", "belly big"],
        "disease": "Dropsy / Internal Organ Infection",
        "severity": "high",
        "action": "Isolate affected stock. Stop feeding. Antibiotic feed under vet guidance only.",
    },
    {
        "keywords": ["jumping", "jump out", "crawling out", "leaving water", "trying to escape"],
        "disease": "Environmental Stress — Toxicity or pH Shock",
        "severity": "high",
        "action": "Test pH and ammonia urgently. Partial water exchange. Stop all chemicals.",
    },
    {
        "keywords": ["healthy", "no problem", "all fine", "good", "normal"],
        "disease": "No visible disease — pond appears healthy",
        "severity": "ok",
        "action": "Continue routine monitoring. Keep aerators running and maintain feed schedule.",
    },
]
