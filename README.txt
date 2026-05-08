===========================================
 ClinicalDocsPro v1.0
 Medical Documentation System
===========================================

PHASE 1 — Condition Library (10 conditions)
  conditions/   : diabetes, hypertension, heart_failure,
                  ckd, copd, atrial_fibrillation,
                  hyperlipidaemia, asthma, obesity, depression

PHASE 2 — Report Engine (CLI)
  src/
    pdf_generator.py   : Reads condition .txt files, generates PDF
    report_builder.py  : Combines patient data + guidelines into PDF
    patient_manager.py : Save / load / search patients (JSON database)
    icd10_lookup.py    : ICD-10 code reference (70+ codes)
    utils.py           : Shared helpers and styling

PHASE 3 — Web Dashboard (Flask)
  web/app.py           : Flask server
  web/templates/       : HTML pages (index, patients, guidelines, reports)
  web/static/style.css : Dashboard styling

QUICK START
  1. Activate virtual environment:  .venv\Scripts\activate
  2. Generate all guidelines:       python src\pdf_generator.py
  3. Load sample patients:          python src\patient_manager.py
  4. Start web dashboard:           python web\app.py
  5. Open browser at:               http://127.0.0.1:5000

FOLDERS
  conditions/       : Plain-text clinical guidelines
  patients/         : Patient database (JSON) and individual records
  reports/          : Generated PDF reports (gitignored)
  src/              : Core engine code
  web/              : Flask web interface

DISCLAIMER
  For educational use only. Not for direct clinical use.