# src/migrate_json_to_db.py
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from patient_manager import init_db, add_patient, Patient

# Load JSON data
json_path = os.path.join(os.path.dirname(__file__), '..', 'patients', 'patients_db.json')
with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Initialize new SQLite DB (creates patients.db)
init_db()

# Import each patient
for mrn, pdata in data.items():
    p = Patient(
        name               = pdata['name'],
        dob                = pdata['dob'],
        mrn                = pdata['mrn'],
        sex                = pdata['sex'],
        admitting_physician= pdata['admitting_physician'],
        admission_date     = pdata['admission_date'],
        discharge_date     = pdata['discharge_date'],
        primary_diagnosis  = pdata['primary_diagnosis'],
        secondary_diagnoses= pdata.get('secondary_diagnoses', []),
        medications        = pdata.get('medications', []),
        allergies          = pdata.get('allergies', []),
        discharge_instructions= pdata.get('discharge_instructions', []),
        follow_up          = pdata.get('follow_up', []),
        notes              = pdata.get('notes', '')
    )
    add_patient(p)

print(f"Migrated {len(data)} patients to SQLite.")