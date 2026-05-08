# icd10_lookup.py
# ICD-10 code reference dictionary for ClinicalDocsPro

ICD10_CODES = {

    # Diabetes
    "E11.9":   {"name": "Type 2 Diabetes Mellitus",                     "category": "Diabetes"},
    "E11.65":  {"name": "T2DM with Hyperglycaemia (uncontrolled)",       "category": "Diabetes"},
    "E11.40":  {"name": "T2DM with Diabetic Neuropathy",                 "category": "Diabetes"},
    "E11.00":  {"name": "T2DM with Hyperosmolarity",                     "category": "Diabetes"},
    "E10.9":   {"name": "Type 1 Diabetes Mellitus",                      "category": "Diabetes"},
    "O24.419": {"name": "Gestational Diabetes Mellitus",                 "category": "Diabetes"},
    "R73.09":  {"name": "Pre-Diabetes / Impaired Glucose",               "category": "Diabetes"},

    # Hypertension
    "I10":     {"name": "Essential (Primary) Hypertension",              "category": "Hypertension"},
    "I11.9":   {"name": "Hypertensive Heart Disease without HF",         "category": "Hypertension"},
    "I12.9":   {"name": "Hypertensive Chronic Kidney Disease Stage 1-4", "category": "Hypertension"},
    "I13.10":  {"name": "Hypertensive Heart and CKD",                    "category": "Hypertension"},
    "I16.0":   {"name": "Hypertensive Urgency",                          "category": "Hypertension"},
    "I16.1":   {"name": "Hypertensive Emergency",                        "category": "Hypertension"},

    # Heart Failure
    "I50.20":  {"name": "Unspecified Systolic HF",                       "category": "Heart Failure"},
    "I50.22":  {"name": "Systolic HF Acute on Chronic (HFrEF)",          "category": "Heart Failure"},
    "I50.30":  {"name": "Unspecified Diastolic HF",                      "category": "Heart Failure"},
    "I50.32":  {"name": "Diastolic HF Acute on Chronic (HFpEF)",         "category": "Heart Failure"},
    "I50.9":   {"name": "Heart Failure Unspecified",                     "category": "Heart Failure"},

    # CKD
    "N18.1":   {"name": "Chronic Kidney Disease Stage 1",                "category": "CKD"},
    "N18.2":   {"name": "Chronic Kidney Disease Stage 2",                "category": "CKD"},
    "N18.31":  {"name": "Chronic Kidney Disease Stage 3a",               "category": "CKD"},
    "N18.32":  {"name": "Chronic Kidney Disease Stage 3b",               "category": "CKD"},
    "N18.4":   {"name": "Chronic Kidney Disease Stage 4",                "category": "CKD"},
    "N18.5":   {"name": "Chronic Kidney Disease Stage 5",                "category": "CKD"},
    "N18.6":   {"name": "End-Stage Renal Disease (ESRD)",                "category": "CKD"},
    "N18.9":   {"name": "Chronic Kidney Disease Unspecified",            "category": "CKD"},

    # COPD
    "J44.9":   {"name": "COPD Unspecified",                              "category": "COPD"},
    "J44.1":   {"name": "COPD with Acute Exacerbation",                  "category": "COPD"},
    "J44.0":   {"name": "COPD with Acute Lower Respiratory Infection",   "category": "COPD"},
    "J43.9":   {"name": "Emphysema Unspecified",                         "category": "COPD"},

    # Atrial Fibrillation
    "I48.0":   {"name": "Paroxysmal Atrial Fibrillation",                "category": "Atrial Fibrillation"},
    "I48.11":  {"name": "Longstanding Persistent Atrial Fibrillation",   "category": "Atrial Fibrillation"},
    "I48.19":  {"name": "Persistent Atrial Fibrillation",                "category": "Atrial Fibrillation"},
    "I48.20":  {"name": "Chronic Atrial Fibrillation",                   "category": "Atrial Fibrillation"},
    "I48.91":  {"name": "Atrial Fibrillation Unspecified",               "category": "Atrial Fibrillation"},
    "I48.3":   {"name": "Typical Atrial Flutter",                        "category": "Atrial Fibrillation"},

    # Hyperlipidaemia
    "E78.00":  {"name": "Pure Hypercholesterolaemia",                    "category": "Hyperlipidaemia"},
    "E78.01":  {"name": "Familial Hypercholesterolaemia",                "category": "Hyperlipidaemia"},
    "E78.1":   {"name": "Pure Hypertriglyceridaemia",                    "category": "Hyperlipidaemia"},
    "E78.5":   {"name": "Hyperlipidaemia Mixed",                         "category": "Hyperlipidaemia"},
    "E78.2":   {"name": "Mixed Hyperlipidaemia",                         "category": "Hyperlipidaemia"},

    # Asthma
    "J45.20":  {"name": "Mild Intermittent Asthma Uncomplicated",        "category": "Asthma"},
    "J45.30":  {"name": "Mild Persistent Asthma Uncomplicated",          "category": "Asthma"},
    "J45.40":  {"name": "Moderate Persistent Asthma Uncomplicated",      "category": "Asthma"},
    "J45.50":  {"name": "Severe Persistent Asthma Uncomplicated",        "category": "Asthma"},
    "J45.909": {"name": "Unspecified Asthma Uncomplicated",              "category": "Asthma"},
    "J45.901": {"name": "Unspecified Asthma with Acute Exacerbation",    "category": "Asthma"},

    # Obesity
    "E66.01":  {"name": "Morbid Obesity (Class III)",                    "category": "Obesity"},
    "E66.09":  {"name": "Other Obesity (Class I and II)",                "category": "Obesity"},
    "E66.9":   {"name": "Obesity Unspecified",                           "category": "Obesity"},
    "E66.1":   {"name": "Drug-Induced Obesity",                          "category": "Obesity"},

    # Depression
    "F32.0":   {"name": "Major Depressive Episode Mild",                 "category": "Depression"},
    "F32.1":   {"name": "Major Depressive Episode Moderate",             "category": "Depression"},
    "F32.2":   {"name": "Major Depressive Episode Severe",               "category": "Depression"},
    "F32.9":   {"name": "Major Depressive Episode Unspecified",          "category": "Depression"},
    "F33.0":   {"name": "Recurrent Depressive Disorder Mild",            "category": "Depression"},
    "F33.9":   {"name": "Recurrent Depressive Disorder Unspecified",     "category": "Depression"},
    "F41.1":   {"name": "Generalised Anxiety Disorder",                  "category": "Depression"},
}


# ── Lookup Functions ──────────────────────────────────────────────────────────

def lookup(code):
    """Return name and category for an ICD-10 code."""
    code = code.strip().upper()
    return ICD10_CODES.get(code, {
        "name": "Unknown Code",
        "category": "Unknown"
    })


def get_codes_by_category(category):
    """Return all ICD-10 codes for a given condition category."""
    return {
        code: info for code, info in ICD10_CODES.items()
        if info["category"].lower() == category.lower()
    }


def get_all_categories():
    """Return list of all unique condition categories."""
    return sorted(set(info["category"] for info in ICD10_CODES.values()))


def format_code(code):
    """Return a formatted string: CODE — Name (Category)"""
    info = lookup(code)
    return f"{code} — {info['name']} ({info['category']})"


# ── Quick test ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=== ICD-10 Lookup Test ===")
    test_codes = ["I10", "E11.65", "I50.22", "N18.32", "J44.1", "I48.91"]
    for c in test_codes:
        print(f"  {format_code(c)}")

    print("\n=== All Categories ===")
    for cat in get_all_categories():
        codes = get_codes_by_category(cat)
        print(f"  {cat}: {len(codes)} codes")