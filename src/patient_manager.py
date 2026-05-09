# patient_manager.py
# SQLite-backed patient storage (replaces JSON file)

import os
import sqlite3
import json
import sys
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils import BASE_DIR
from report_builder import Patient, build_report

# ── Database path ─────────────────────────────────────────────────────────────
DB_FILE = os.path.join(BASE_DIR, "patients", "patients.db")

# ── Database helpers ──────────────────────────────────────────────────────────
def get_connection():
    """Open a connection to the SQLite database (auto-commits)."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")   # better concurrency
    conn.execute("PRAGMA foreign_keys=ON")
    return conn

def init_db():
    """Create tables if they don't exist."""
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            mrn TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            dob TEXT,
            sex TEXT,
            admitting_physician TEXT,
            admission_date TEXT,
            discharge_date TEXT,
            primary_diagnosis_code TEXT,
            primary_diagnosis_name TEXT,
            secondary_diagnoses TEXT,  -- JSON array
            medications TEXT,          -- JSON array
            allergies TEXT,            -- JSON array
            discharge_instructions TEXT,-- JSON array
            follow_up TEXT,            -- JSON array
            notes TEXT,
            created TEXT
        )
    """)
    conn.commit()
    conn.close()

# ── Convert row ↔ Patient object ──────────────────────────────────────────────
def row_to_patient(row):
    """Turn a database row into a Patient object."""
    return Patient(
        name               = row['name'],
        dob                = row['dob'],
        mrn                = row['mrn'],
        sex                = row['sex'],
        admitting_physician= row['admitting_physician'],
        admission_date     = row['admission_date'],
        discharge_date     = row['discharge_date'],
        primary_diagnosis  = json.loads(row['primary_diagnosis_code']),
        secondary_diagnoses= json.loads(row['secondary_diagnoses']),
        medications        = json.loads(row['medications']),
        allergies          = json.loads(row['allergies']),
        discharge_instructions= json.loads(row['discharge_instructions']),
        follow_up          = json.loads(row['follow_up']),
        notes              = row['notes']
    )

# ── Public API (same as before) ───────────────────────────────────────────────
def load_db():
    """Return a dict {mrn: patient_dict} for compatibility with web routes."""
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM patients ORDER BY mrn")
    rows = c.fetchall()
    db = {}
    for row in rows:
        db[row['mrn']] = {
            "name": row['name'],
            "dob": row['dob'],
            "mrn": row['mrn'],
            "sex": row['sex'],
            "admitting_physician": row['admitting_physician'],
            "admission_date": row['admission_date'],
            "discharge_date": row['discharge_date'],
            "primary_diagnosis": json.loads(row['primary_diagnosis_code']),
            "secondary_diagnoses": json.loads(row['secondary_diagnoses']),
            "medications": json.loads(row['medications']),
            "allergies": json.loads(row['allergies']),
            "discharge_instructions": json.loads(row['discharge_instructions']),
            "follow_up": json.loads(row['follow_up']),
            "notes": row['notes'],
            "created": row['created']
        }
    conn.close()
    return db

def add_patient(patient):
    """Insert or replace a patient (upsert on MRN)."""
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        INSERT OR REPLACE INTO patients (
            mrn, name, dob, sex, admitting_physician,
            admission_date, discharge_date,
            primary_diagnosis_code, primary_diagnosis_name,
            secondary_diagnoses, medications, allergies,
            discharge_instructions, follow_up, notes, created
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        patient.mrn,
        patient.name,
        patient.dob,
        patient.sex,
        patient.admitting_physician,
        patient.admission_date,
        patient.discharge_date,
        json.dumps(patient.primary_diagnosis),
        patient.primary_diagnosis.get('code', '') + ' - ' + patient.primary_diagnosis.get('name', ''),
        json.dumps(patient.secondary_diagnoses),
        json.dumps(patient.medications),
        json.dumps(patient.allergies),
        json.dumps(patient.discharge_instructions),
        json.dumps(patient.follow_up),
        patient.notes,
        str(date.today())
    ))
    conn.commit()
    conn.close()
    print(f"  Saved: {patient.name} (MRN: {patient.mrn})")
    return patient.mrn

def get_patient(mrn):
    """Retrieve a single patient by MRN."""
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM patients WHERE mrn = ?", (mrn,))
    row = c.fetchone()
    conn.close()
    if row is None:
        print(f"  Patient MRN '{mrn}' not found.")
        return None
    return row_to_patient(row)

def list_patients():
    """Print a summary table of all patients."""
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT mrn, name, admission_date, discharge_date, primary_diagnosis_code FROM patients ORDER BY mrn")
    rows = c.fetchall()
    if not rows:
        print("  No patients found in database.")
        return []

    print(f"\n  {'MRN':<15} {'Name':<25} {'Admission':<15} {'Discharge':<15} {'Primary Dx'}")
    print(f"  {'-'*15} {'-'*25} {'-'*15} {'-'*15} {'-'*30}")
    for row in rows:
        dx = json.loads(row['primary_diagnosis_code']) if row['primary_diagnosis_code'] else {}
        print(f"  {row['mrn']:<15} {row['name']:<25} "
              f"{row['admission_date']:<15} "
              f"{row['discharge_date']:<15} "
              f"{dx.get('code', '')}")
    conn.close()
    return list(load_db().keys())

def search_patients(query):
    """Search patients by name, MRN, or ICD-10 code."""
    conn = get_connection()
    c = conn.cursor()
    q = f"%{query}%"
    c.execute("""
        SELECT mrn FROM patients
        WHERE name LIKE ?
           OR mrn LIKE ?
           OR primary_diagnosis_code LIKE ?
           OR secondary_diagnoses LIKE ?
    """, (q, q, q, q))
    rows = c.fetchall()
    conn.close()
    return [row['mrn'] for row in rows]

def search_patients_paginated(query, sort_by='mrn', order='asc', page=1, per_page=10):
    """
    Search + sort + paginate. Returns a dict with keys:
        patients: list of patient_dicts
        total: total matching rows
        pages: total number of pages
        current_page: current page number
    """
    conn = get_connection()
    c = conn.cursor()
    
    # Build WHERE clause
    where = ""
    params = []
    if query:
        q = f"%{query}%"
        where = "WHERE name LIKE ? OR mrn LIKE ? OR primary_diagnosis_code LIKE ? OR secondary_diagnoses LIKE ?"
        params = [q, q, q, q]
    
    # Count total matches
    count_sql = f"SELECT COUNT(*) FROM patients {where}"
    c.execute(count_sql, params)
    total = c.fetchone()[0]
    
    # Determine total pages
    pages = max(1, -(-total // per_page))  # ceil division
    current_page = max(1, min(page, pages))
    offset = (current_page - 1) * per_page
    
    # Validate sort column (only allow safe columns to prevent injection)
    allowed_sort = ['mrn', 'name', 'admission_date', 'discharge_date', 'primary_diagnosis_code']
    if sort_by not in allowed_sort:
        sort_by = 'mrn'
    order = 'ASC' if order.lower() == 'asc' else 'DESC'
    
    # Fetch the page of patients
    sql = f"""
        SELECT mrn, name, admission_date, discharge_date, primary_diagnosis_code
        FROM patients {where}
        ORDER BY {sort_by} {order}
        LIMIT ? OFFSET ?
    """
    c.execute(sql, params + [per_page, offset])
    rows = c.fetchall()
    
    patients = []
    for row in rows:
        dx = json.loads(row['primary_diagnosis_code']) if row['primary_diagnosis_code'] else {}
        patients.append({
            'mrn': row['mrn'],
            'name': row['name'],
            'admission_date': row['admission_date'],
            'discharge_date': row['discharge_date'],
            'primary_code': dx.get('code', ''),
            'primary_name': dx.get('name', '')
        })
    
    conn.close()
    return {
        'patients': patients,
        'total': total,
        'pages': pages,
        'current_page': current_page
    }

def delete_patient(mrn):
    """Delete a patient from the database."""
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT name FROM patients WHERE mrn = ?", (mrn,))
    row = c.fetchone()
    if row is None:
        print(f"  Patient MRN '{mrn}' not found.")
        conn.close()
        return False
    name = row['name']
    c.execute("DELETE FROM patients WHERE mrn = ?", (mrn,))
    conn.commit()
    conn.close()
    print(f"  Deleted: {name} (MRN: {mrn})")
    return True

def generate_patient_report(mrn, include_guidelines=True):
    """Load a patient by MRN and generate PDF report."""
    patient = get_patient(mrn)
    if not patient:
        return None
    print(f"\n  Generating report for: {patient.name}")
    return build_report(patient, include_guidelines=include_guidelines)

def export_patient(mrn):
    """Export a single patient record to JSON file."""
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM patients WHERE mrn = ?", (mrn,))
    row = c.fetchone()
    if row is None:
        print(f"  Patient MRN '{mrn}' not found.")
        conn.close()
        return None
    os.makedirs(os.path.join(BASE_DIR, "patients", "patient_records"), exist_ok=True)
    filename = f"{mrn}_record.json"
    filepath = os.path.join(BASE_DIR, "patients", "patient_records", filename)
    record = {
        "name": row['name'],
        "dob": row['dob'],
        "mrn": row['mrn'],
        "sex": row['sex'],
        "admitting_physician": row['admitting_physician'],
        "admission_date": row['admission_date'],
        "discharge_date": row['discharge_date'],
        "primary_diagnosis": json.loads(row['primary_diagnosis_code']),
        "secondary_diagnoses": json.loads(row['secondary_diagnoses']),
        "medications": json.loads(row['medications']),
        "allergies": json.loads(row['allergies']),
        "discharge_instructions": json.loads(row['discharge_instructions']),
        "follow_up": json.loads(row['follow_up']),
        "notes": row['notes'],
        "created": row['created']
    }
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(record, f, indent=2, ensure_ascii=False)
    conn.close()
    print(f"  Exported: {filepath}")
    return filepath

def db_stats():
    """Print database statistics."""
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM patients")
    total = c.fetchone()[0]
    if total == 0:
        print("  Database is empty.")
        conn.close()
        return
    c.execute("SELECT primary_diagnosis_code, COUNT(*) FROM patients GROUP BY primary_diagnosis_code ORDER BY COUNT(*) DESC")
    print(f"\n  Total patients : {total}")
    print(f"  Database file  : {DB_FILE}")
    print(f"\n  Primary diagnoses:")
    for row in c.fetchall():
        dx = json.loads(row[0]) if row[0] else {}
        code = dx.get('code', 'Unknown')
        print(f"    {code:<12} {row[1]} patient(s)")
    conn.close()

# ── Interactive menu ──────────────────────────────────────────────────────────
def menu():
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

# ── If run directly, initialize DB and run menu ───────────────────────────────
if __name__ == "__main__":
    print("=== ClinicalDocsPro — Patient Manager ===\n")
    init_db()
    menu()