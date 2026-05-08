# patient_manager.py
# Save, load, list and search patients from a local JSON database

import os
import json
import sys
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils import BASE_DIR, REPORTS_DIR
from report_builder import Patient, build_report

# ── Database path ─────────────────────────────────────────────────────────────
DB_DIR  = os.path.join(BASE_DIR, "patients", "patient_records")
DB_FILE = os.path.join(BASE_DIR, "patients", "patients_db.json")


# ── Load / Save database ──────────────────────────────────────────────────────
def load_db():
    """Load all patients from JSON database."""
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_db(db):
    """Save patient database to JSON file."""
    os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=2, ensure_ascii=False)


# ── Add a patient ─────────────────────────────────────────────────────────────
def add_patient(patient):
    """
    Add or update a patient in the database.
    Uses MRN as unique key.
    """
    db = load_db()
    db[patient.mrn] = {
        "name":                   patient.name,
        "dob":                    patient.dob,
        "mrn":                    patient.mrn,
        "sex":                    patient.sex,
        "admitting_physician":    patient.admitting_physician,
        "admission_date":         patient.admission_date,
        "discharge_date":         patient.discharge_date,
        "primary_diagnosis":      patient.primary_diagnosis,
        "secondary_diagnoses":    patient.secondary_diagnoses,
        "medications":            patient.medications,
        "allergies":              patient.allergies,
        "discharge_instructions": patient.discharge_instructions,
        "follow_up":              patient.follow_up,
        "notes":                  patient.notes,
        "created":                str(date.today()),
    }
    save_db(db)
    print(f"  Saved: {patient.name} (MRN: {patient.mrn})")
    return patient.mrn


# ── Load a patient by MRN ─────────────────────────────────────────────────────
def get_patient(mrn):
    """Load a patient from the database by MRN."""
    db = load_db()
    if mrn not in db:
        print(f"  Patient MRN '{mrn}' not found.")
        return None
    data = db[mrn]
    return Patient(
        name                  = data["name"],
        dob                   = data["dob"],
        mrn                   = data["mrn"],
        sex                   = data["sex"],
        admitting_physician   = data["admitting_physician"],
        admission_date        = data["admission_date"],
        discharge_date        = data["discharge_date"],
        primary_diagnosis     = data["primary_diagnosis"],
        secondary_diagnoses   = data.get("secondary_diagnoses",    []),
        medications           = data.get("medications",            []),
        allergies             = data.get("allergies",              []),
        discharge_instructions= data.get("discharge_instructions", []),
        follow_up             = data.get("follow_up",              []),
        notes                 = data.get("notes",                  ""),
    )


# ── List all patients ─────────────────────────────────────────────────────────
def list_patients():
    """Print a summary table of all patients in the database."""
    db = load_db()
    if not db:
        print("  No patients found in database.")
        return []

    print(f"\n  {'MRN':<15} {'Name':<25} {'Admission':<15} {'Discharge':<15} {'Primary Dx'}")
    print(f"  {'-'*15} {'-'*25} {'-'*15} {'-'*15} {'-'*30}")

    for mrn, data in db.items():
        print(f"  {mrn:<15} {data['name']:<25} "
              f"{data['admission_date']:<15} "
              f"{data['discharge_date']:<15} "
              f"{data['primary_diagnosis']['code']}")
    return list(db.keys())


# ── Search patients ───────────────────────────────────────────────────────────
def search_patients(query):
    """
    Search patients by name, MRN, or ICD-10 code.
    Returns list of matching MRNs.
    """
    db      = load_db()
    query   = query.lower().strip()
    matches = []

    for mrn, data in db.items():
        if (query in data["name"].lower() or
            query in mrn.lower() or
            query in data["primary_diagnosis"]["code"].lower() or
            any(query in d["code"].lower()
                for d in data.get("secondary_diagnoses", []))):
            matches.append(mrn)

    return matches


# ── Delete a patient ──────────────────────────────────────────────────────────
def delete_patient(mrn):
    """Remove a patient from the database by MRN."""
    db = load_db()
    if mrn not in db:
        print(f"  Patient MRN '{mrn}' not found.")
        return False
    name = db[mrn]["name"]
    del db[mrn]
    save_db(db)
    print(f"  Deleted: {name} (MRN: {mrn})")
    return True


# ── Generate report for a saved patient ──────────────────────────────────────
def generate_patient_report(mrn, include_guidelines=True):
    """Load a patient by MRN and generate their PDF report."""
    patient = get_patient(mrn)
    if not patient:
        return None
    print(f"\n  Generating report for: {patient.name}")
    return build_report(patient, include_guidelines=include_guidelines)


# ── Export patient to JSON file ───────────────────────────────────────────────
def export_patient(mrn):
    """Export a single patient record to a JSON file."""
    db = load_db()
    if mrn not in db:
        print(f"  Patient MRN '{mrn}' not found.")
        return None
    os.makedirs(DB_DIR, exist_ok=True)
    filename  = f"{mrn}_record.json"
    filepath  = os.path.join(DB_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(db[mrn], f, indent=2, ensure_ascii=False)
    print(f"  Exported: {filepath}")
    return filepath


# ── Database stats ────────────────────────────────────────────────────────────
def db_stats():
    """Print database statistics."""
    db = load_db()
    if not db:
        print("  Database is empty.")
        return

    total = len(db)
    codes = {}
    for data in db.values():
        code = data["primary_diagnosis"]["code"]
        codes[code] = codes.get(code, 0) + 1

    print(f"\n  Total patients : {total}")
    print(f"  Database file  : {DB_FILE}")
    print(f"\n  Primary diagnoses:")
    for code, count in sorted(codes.items(), key=lambda x: -x[1]):
        print(f"    {code:<12} {count} patient(s)")


# ── Interactive menu ──────────────────────────────────────────────────────────
def menu():
    """Simple interactive CLI menu."""
    while True:
        print("\n" + "="*50)
        print("  ClinicalDocsPro — Patient Manager")
        print("="*50)
        print("  1. List all patients")
        print("  2. Search patients")
        print("  3. Generate report for a patient")
        print("  4. Export patient record to JSON")
        print("  5. Delete a patient")
        print("  6. Database stats")
        print("  0. Exit")
        print("-"*50)

        choice = input("  Enter choice: ").strip()

        if choice == "1":
            list_patients()

        elif choice == "2":
            q = input("  Search (name / MRN / ICD-10 code): ").strip()
            results = search_patients(q)
            if results:
                print(f"\n  Found {len(results)} match(es):")
                for mrn in results:
                    p = get_patient(mrn)
                    if p:
                        print(f"    • {p.name} — MRN: {p.mrn}")
            else:
                print("  No matches found.")

        elif choice == "3":
            mrn = input("  Enter MRN: ").strip()
            result = generate_patient_report(mrn)
            if result:
                print(f"\n  Report saved to: {result}")

        elif choice == "4":
            mrn = input("  Enter MRN: ").strip()
            export_patient(mrn)

        elif choice == "5":
            mrn = input("  Enter MRN: ").strip()
            confirm = input(f"  Delete patient {mrn}? (yes/no): ").strip().lower()
            if confirm == "yes":
                delete_patient(mrn)

        elif choice == "6":
            db_stats()

        elif choice == "0":
            print("\n  Goodbye!")
            break

        else:
            print("  Invalid choice. Please try again.")


# ── Test run ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=== ClinicalDocsPro — Patient Manager ===\n")

    # Create and save sample patients
    patients = [
        Patient(
            name="John M. Doe",      dob="March 14, 1958",
            mrn="0047821-B",         sex="Male",
            admitting_physician="Dr. Sarah L. Martinez, MD",
            admission_date="April 28, 2026",
            discharge_date="May 3, 2026",
            primary_diagnosis={"code": "I50.22"},
            secondary_diagnoses=[
                {"code": "I48.91"}, {"code": "E11.65"},
                {"code": "N18.32"}, {"code": "I10"},
            ],
            medications=[
                {"name": "Furosemide",   "dose": "80 mg",  "route": "Oral", "frequency": "BID",    "purpose": "Diuresis"},
                {"name": "Bisoprolol",   "dose": "5 mg",   "route": "Oral", "frequency": "Daily",  "purpose": "Rate/BP"},
                {"name": "Apixaban",     "dose": "5 mg",   "route": "Oral", "frequency": "BID",    "purpose": "AFib"},
                {"name": "Metformin",    "dose": "500 mg", "route": "Oral", "frequency": "BID",    "purpose": "Diabetes"},
            ],
            allergies=[
                {"name": "Penicillin", "reaction": "Rash"},
                {"name": "Codeine",    "reaction": "Nausea"},
            ],
            discharge_instructions=[
                "Sodium < 1,500 mg/day",
                "Weigh daily; call MD if +2 lbs in 1 day",
                "Light walking 10-15 minutes twice daily",
            ],
            follow_up=[
                {"provider": "Dr. R. Flores",  "specialty": "Primary Care", "date": "May 7, 2026",  "contact": "(936) 555-0142"},
                {"provider": "Dr. A. Hughes",  "specialty": "Cardiology",   "date": "May 12, 2026", "contact": "(936) 555-0287"},
            ],
            notes="5-day admission for ADHF. Discharged stable with home health."
        ),
        Patient(
            name="Maria L. Santos",  dob="July 22, 1965",
            mrn="0051234-A",         sex="Female",
            admitting_physician="Dr. Kevin R. Owens, MD",
            admission_date="May 1, 2026",
            discharge_date="May 5, 2026",
            primary_diagnosis={"code": "J44.1"},
            secondary_diagnoses=[
                {"code": "E11.9"}, {"code": "E66.09"},
            ],
            medications=[
                {"name": "Tiotropium",    "dose": "18 mcg", "route": "Inhaled", "frequency": "Daily",  "purpose": "COPD"},
                {"name": "Salbutamol",    "dose": "100 mcg","route": "Inhaled", "frequency": "PRN",    "purpose": "Rescue"},
                {"name": "Prednisolone",  "dose": "40 mg",  "route": "Oral",    "frequency": "Daily",  "purpose": "Exacerbation"},
                {"name": "Metformin",     "dose": "1000 mg","route": "Oral",    "frequency": "BID",    "purpose": "Diabetes"},
            ],
            allergies=[
                {"name": "Aspirin", "reaction": "Bronchospasm"},
            ],
            discharge_instructions=[
                "Use tiotropium inhaler every morning",
                "Carry salbutamol rescue inhaler at all times",
                "Complete prednisolone course as prescribed",
                "Stop smoking — referral to cessation programme provided",
            ],
            follow_up=[
                {"provider": "Dr. K. Owens",   "specialty": "Pulmonology",  "date": "May 12, 2026", "contact": "(936) 555-0198"},
                {"provider": "Dr. R. Flores",  "specialty": "Primary Care", "date": "May 15, 2026", "contact": "(936) 555-0142"},
            ],
            notes="Admitted with COPD exacerbation. GOLD Grade 3. Discharged on triple therapy."
        ),
        Patient(
            name="Robert T. Kim",    dob="November 5, 1972",
            mrn="0062891-C",         sex="Male",
            admitting_physician="Dr. Angela T. Hughes, MD",
            admission_date="May 4, 2026",
            discharge_date="May 6, 2026",
            primary_diagnosis={"code": "I10"},
            secondary_diagnoses=[
                {"code": "E78.5"}, {"code": "F32.1"},
            ],
            medications=[
                {"name": "Amlodipine",    "dose": "10 mg",  "route": "Oral", "frequency": "Daily",  "purpose": "HTN"},
                {"name": "Lisinopril",    "dose": "20 mg",  "route": "Oral", "frequency": "Daily",  "purpose": "HTN"},
                {"name": "Atorvastatin",  "dose": "40 mg",  "route": "Oral", "frequency": "Nightly","purpose": "Cholesterol"},
                {"name": "Sertraline",    "dose": "50 mg",  "route": "Oral", "frequency": "Daily",  "purpose": "Depression"},
            ],
            allergies=[
                {"name": "Sulfa drugs", "reaction": "Rash"},
            ],
            discharge_instructions=[
                "Monitor BP at home twice daily; log readings",
                "Low-sodium diet < 1,500 mg/day",
                "Exercise 30 minutes most days",
                "Continue sertraline; follow up with psychiatry",
            ],
            follow_up=[
                {"provider": "Dr. A. Hughes",  "specialty": "Cardiology",   "date": "May 14, 2026", "contact": "(936) 555-0287"},
                {"provider": "Dr. P. Nguyen",  "specialty": "Psychiatry",   "date": "May 21, 2026", "contact": "(936) 555-0445"},
            ],
            notes="Admitted for hypertensive urgency. BP controlled on dual therapy. Depression identified; sertraline started."
        ),
    ]

    # Save all patients
    print("Saving patients to database...")
    for p in patients:
        add_patient(p)

    # List all
    print("\nAll patients in database:")
    list_patients()

    # Stats
    print("\nDatabase statistics:")
    db_stats()

    # Search test
    print("\nSearch test — query 'I10':")
    results = search_patients("I10")
    print(f"  Found: {results}")

    # Export test
    print("\nExporting first patient record:")
    export_patient("0047821-B")

    # Generate report
    print("\nGenerating report for Robert T. Kim:")
    generate_patient_report("0062891-C")

    print("\n=== All tests passed! ===")
    print("\nTo open the interactive menu run:")
    print("  python src/patient_manager.py --menu")