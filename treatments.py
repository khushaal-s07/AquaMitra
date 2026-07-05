# Solution, medicine & improvement advice per disease (AP aquaculture)

TREATMENT_DB = {
    "White Spot Syndrome (WSSV)": {
        "solution": "Stop feeding for 3 days. Run aerators 24 hours. Do 30% water exchange. Isolate this pond from others.",
        "medicine": "Probiotic powder 1 kg/acre after fasting. Immunostimulant (Beta-glucan) 5g/kg feed. Potassium permanganate 2 ppm dip under expert supervision.",
        "improvements": "Reduce stocking density 20%. Install shade nets. Disinfect nets and boots. WSSV lab test before next crop.",
    },
    "White Feces Syndrome / EHP": {
        "solution": "Cut feed 30% immediately. Increase water exchange 20%. Add lime to stabilize pH at 7.8.",
        "medicine": "Gut probiotic (Bacillus subtilis) 10g/kg feed for 10 days. Vitamin C 1g/kg feed. Organic iodine 0.3 ppm in water.",
        "improvements": "Use quality pellet feed only. Avoid overfeeding. Use feeding trays. EHP PCR test every 15 days.",
    },
    "Early Mortality Syndrome (EMS / AHPND)": {
        "solution": "Stop feeding 48 hours. Emergency aeration full power. Exchange 40% clean water. Do not move stock to other ponds.",
        "medicine": "Probiotics 2 kg/acre in water. Zeolite 25 kg/acre. Oxytetracycline only under registered aqua vet prescription.",
        "improvements": "Stock max 30/m². Use SPF disease-free seed. Keep DO above 5 mg/L. Record mortality daily.",
    },
    "Hypoxia — Low Oxygen Stress": {
        "solution": "Switch on all aerators immediately. Stop feeding today. Run paddle-wheels through the night.",
        "medicine": "Primary fix is aeration — no chemical needed. Emergency only: hydrogen peroxide 1 ppm under expert guidance.",
        "improvements": "Add one extra aerator per acre. Avoid overfeeding. Test DO at dawn. Plant shade to prevent night oxygen crash.",
    },
    "Feed Refusal / Internal Bacterial Infection": {
        "solution": "Reduce feed 50% for 3 days. Fix water quality first. Remove uneaten feed from pond bottom.",
        "medicine": "Vitamin C 2g/kg feed. Probiotic-coated feed 7 days. Garlic extract 1% in feed as natural antibacterial.",
        "improvements": "Feed during cool hours (7-8 AM, 5-6 PM). Use feeding trays. Maintain stable pH and DO.",
    },
    "Red Body Syndrome / Toxicity Stress": {
        "solution": "Stop chemicals near pond. Exchange 25% fresh water. Test ammonia and nitrite immediately.",
        "medicine": "Activated carbon 10 kg/acre. Zeolite 20 kg/acre. Vitamin E 500 mg/kg feed for 5 days.",
        "improvements": "No pesticides within 100m of pond. Plant buffer trees. Test water every 3 days in hot season.",
    },
    "Soft Shell / Molting Disorder": {
        "solution": "Maintain alkalinity above 120 ppm. Reduce handling. Keep water temperature stable.",
        "medicine": "Calcium-magnesium mineral supplement in feed. Dolomite lime 15 kg/acre. Vitamin D3 premix 10 days.",
        "improvements": "Add crushed oyster shell on pond bottom. Avoid sudden salinity changes during molting.",
    },
    "Black Gill Disease / Gill Rot": {
        "solution": "Increase aeration and 30% water exchange. Remove dead algae and sludge from bottom.",
        "medicine": "Formalin 25 ppm bath 30 min under expert supervision. Probiotics to reduce organic load.",
        "improvements": "Avoid overfeeding. Regular bottom cleaning. Keep ammonia below 0.1 ppm.",
    },
    "Algal Bloom — Oxygen Crash Risk": {
        "solution": "Shade cloth 30% to reduce sunlight. Stop excess feeding. Aerators on midnight to 6 AM.",
        "medicine": "Zeolite 20 kg/acre. Probiotics to compete with algae. Alum 25 kg/acre under expert guidance.",
        "improvements": "Maintain C:N ratio with probiotics. Weekly partial water exchange. Monitor night DO.",
    },
    "Slow Growth — EHP / Nutritional Deficiency": {
        "solution": "Upgrade to 35%+ protein feed. Increase water exchange 15%. Check stocking density.",
        "medicine": "Vitamin-mineral premix daily. Probiotics 5g/kg feed. Lecithin supplement for absorption.",
        "improvements": "SPF seed from certified hatchery. Target FCR below 1.4. Weekly growth sampling.",
    },
    "Fin Rot / Fungal Infection": {
        "solution": "Salt bath 5 ppt for 1 hour in treatment tank. Improve water quality. Reduce handling.",
        "medicine": "Potassium permanganate 2 ppm dip 30 min. Salt 5-10 ppt in pond for 24 hours under guidance.",
        "improvements": "Regular water exchange. Use soft nets. Probiotics to reduce fungal spores.",
    },
    "Dropsy / Internal Organ Infection": {
        "solution": "Isolate pond. Stop feeding 24 hours. Bury dead fish away from pond.",
        "medicine": "Florfenicol feed ONLY under registered aqua vet prescription. Probiotics 2 kg/acre.",
        "improvements": "Never use banned antibiotics. Keep pond bottom clean. Vet diagnosis before antibiotics.",
    },
    "Environmental Stress — Toxicity or pH Shock": {
        "solution": "Test pH, ammonia, nitrite now. Exchange 30% clean water. Stop all pond chemicals today.",
        "medicine": "Agricultural lime 20 kg/acre if pH below 7.5. Activated carbon if contamination suspected.",
        "improvements": "Buy pH and DO meter. Never mix chemicals without expert advice. Keep backup aerator.",
    },
    "No visible disease — pond appears healthy": {
        "solution": "Continue good practices. Daily water checks and proper feeding schedule.",
        "medicine": "Preventive probiotics 500g/acre weekly. Vitamin C 1g/kg feed as immunity booster.",
        "improvements": "Keep aerators running. Record feed and mortality daily. Lab water test every 10 days.",
    },
    "Symptoms unclear — need more description": {
        "solution": "Observe fish for 24 hours. Check DO, pH, and ammonia. Note any color, behavior, or feeding changes.",
        "medicine": "Preventive probiotics 500g/acre until diagnosis is clear. Vitamin C in feed as support.",
        "improvements": "Describe symptoms clearly: white spots, floating, not eating, red color, or dead fish.",
    },
    "Acidosis Stress / White Feces Syndrome risk": {
        "solution": "Apply agricultural lime 20-25 kg per acre within 6 hours. Increase aeration.",
        "medicine": "Sudda Chunam (agricultural lime) 20 kg/acre. Probiotics 1 kg/acre after lime settles.",
        "improvements": "Test pH daily until stable above 7.5. Avoid overfeeding during low pH periods.",
    },
    "Alkalosis — Gill damage risk": {
        "solution": "Stop lime application. Partial water exchange 20%. Monitor gill condition.",
        "medicine": "No chemical medicine. Probiotics 1 kg/acre. Vitamin C in feed 1g/kg.",
        "improvements": "Maintain pH between 7.5-8.3. Test alkalinity weekly.",
    },
    "Salinity Stress — EHP vulnerability": {
        "solution": "Add fresh water to reduce salinity. Reduce feed 20%. Monitor shrimp behavior.",
        "medicine": "Probiotics in feed 5g/kg. No antibiotics unless vet prescribes.",
        "improvements": "Target salinity 15-25 ppt for vannamei. Test salinity every 2 days.",
    },
    "Low salinity osmotic shock": {
        "solution": "Add brackish water immediately. Target 20 ppt salinity. Reduce stress and handling.",
        "medicine": "Mineral supplement in feed. Gradual salinity adjustment — never sudden changes.",
        "improvements": "Install salinity meter. Monitor during monsoon freshwater inflow.",
    },
    "Hypoxia — Early Mortality Syndrome (EMS) risk": {
        "solution": "Run all aerators now. Stop feeding 24 hours. Emergency water exchange if possible.",
        "medicine": "Probiotics 2 kg/acre. No chemical unless expert advises.",
        "improvements": "Test DO at dawn daily. Add night aeration. Reduce stocking if DO stays low.",
    },
    "Thermal stress — White Spot Syndrome (WSSV) trigger": {
        "solution": "Increase aeration. Add pond shade. Reduce feed 15% until temp drops below 30°C.",
        "medicine": "Vitamin C 2g/kg feed. Probiotics in water 1 kg/acre. Immunostimulant in feed.",
        "improvements": "Plant shade trees. Deeper water in center. Harvest before peak summer if possible.",
    },
    "No active disease detected": {
        "solution": "Continue routine monitoring and probiotic feeding schedule.",
        "medicine": "Preventive probiotics 500g/acre weekly. Vitamin C 1g/kg feed.",
        "improvements": "Maintain current good practices. Regular water testing every 10 days.",
    },
}


def enrich_alert(alert):
    """Add solution, medicine, improvements to any alert."""
    treatment = TREATMENT_DB.get(alert["disease"], {})
    alert["solution"] = treatment.get("solution", alert.get("action", "Consult local aqua expert."))
    alert["medicine"] = treatment.get("medicine", "Probiotics and vitamin supplements as preventive support.")
    alert["improvements"] = treatment.get("improvements", "Monitor water daily. Keep aerators running.")
    return alert
