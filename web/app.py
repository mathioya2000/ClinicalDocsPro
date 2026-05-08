# app.py
# Flask web dashboard for ClinicalDocsPro

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))

from flask import Flask, render_template, request, redirect, url_for, send_file, flash, jsonify
from patient_manager import (
    load_db, add_patient, get_patient, delete_patient,
    list_patients, search_patients, generate_patient_report,
    export_patient, db_stats
)
from pdf_generator import generate_pdf, list_conditions
from icd10_lookup import lookup, get_all_categories, get_codes_by_category
from report_builder import Patient

BASE_DIR   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORTS_DIR= os.path.join(BASE_DIR, "reports")
TEMPLATES  = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
STATIC     = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")

app = Flask(__name__, template_folder=TEMPLATES, static_folder=STATIC)
app.secret_key = "clinicaldocspro-secret-2026"


# ── Home / Dashboard ──────────────────────────────────────────────────────────
@app.route("/")
def index():
    db   = load_db()
    stats = {
        "total_patients":  len(db),
        "total_conditions": len(list_conditions()),
        "total_reports":   len([f for f in os.listdir(REPORTS_DIR)
                                if f.endswith(".pdf")]) if os.path.exists(REPORTS_DIR) else 0,
    }
    recent = list(db.values())[-5:][::-1]
    return render_template("index.html", stats=stats, recent=recent)


# ── Patients list ─────────────────────────────────────────────────────────────
@app.route("/patients")
def patients():
    db     = load_db()
    query  = request.args.get("q", "").strip()
    if query:
        mrns = search_patients(query)
        data = {mrn: db[mrn] for mrn in mrns if mrn in db}
    else:
        data = db
    return render_template("patients.html", patients=data, query=query)


# ── View single patient ───────────────────────────────────────────────────────
@app.route("/patients/<mrn>")
def patient_detail(mrn):
    patient = get_patient(mrn)
    if not patient:
        flash(f"Patient MRN '{mrn}' not found.", "error")
        return redirect(url_for("patients"))
    return render_template("patient_detail.html", patient=patient,
                           lookup=lookup)


# ── Add new patient ───────────────────────────────────────────────────────────
@app.route("/patients/new", methods=["GET", "POST"])
def new_patient():
    categories = get_all_categories()
    all_codes  = {}
    for cat in categories:
        all_codes[cat] = get_codes_by_category(cat)

    if request.method == "POST":
        try:
            # Parse secondary diagnoses
            sec_codes = request.form.getlist("secondary_codes")
            secondary = [{"code": c} for c in sec_codes if c.strip()]

            # Parse medications
            med_names  = request.form.getlist("med_name")
            med_doses  = request.form.getlist("med_dose")
            med_routes = request.form.getlist("med_route")
            med_freqs  = request.form.getlist("med_frequency")
            med_purps  = request.form.getlist("med_purpose")
            medications = [
                {"name": n, "dose": d, "route": r,
                 "frequency": f, "purpose": p}
                for n, d, r, f, p in zip(
                    med_names, med_doses, med_routes,
                    med_freqs, med_purps)
                if n.strip()
            ]

            # Parse allergies
            all_names     = request.form.getlist("allergy_name")
            all_reactions = request.form.getlist("allergy_reaction")
            allergies = [
                {"name": n, "reaction": r}
                for n, r in zip(all_names, all_reactions)
                if n.strip()
            ]

            # Parse instructions
            instructions = [
                i.strip() for i in
                request.form.get("discharge_instructions", "").splitlines()
                if i.strip()
            ]

            # Parse follow-up
            fu_providers  = request.form.getlist("fu_provider")
            fu_specialties= request.form.getlist("fu_specialty")
            fu_dates      = request.form.getlist("fu_date")
            fu_contacts   = request.form.getlist("fu_contact")
            follow_up = [
                {"provider": p, "specialty": s,
                 "date": d, "contact": c}
                for p, s, d, c in zip(
                    fu_providers, fu_specialties,
                    fu_dates, fu_contacts)
                if p.strip()
            ]

            patient = Patient(
                name                  = request.form["name"],
                dob                   = request.form["dob"],
                mrn                   = request.form["mrn"],
                sex                   = request.form["sex"],
                admitting_physician   = request.form["admitting_physician"],
                admission_date        = request.form["admission_date"],
                discharge_date        = request.form["discharge_date"],
                primary_diagnosis     = {"code": request.form["primary_code"]},
                secondary_diagnoses   = secondary,
                medications           = medications,
                allergies             = allergies,
                discharge_instructions= instructions,
                follow_up             = follow_up,
                notes                 = request.form.get("notes", ""),
            )

            add_patient(patient)
            flash(f"Patient {patient.name} added successfully!", "success")
            return redirect(url_for("patient_detail", mrn=patient.mrn))

        except Exception as e:
            flash(f"Error adding patient: {str(e)}", "error")

    return render_template("new_patient.html",
                           categories=categories, all_codes=all_codes)


# ── Generate patient report ───────────────────────────────────────────────────
@app.route("/patients/<mrn>/report")
def patient_report(mrn):
    result = generate_patient_report(mrn, include_guidelines=True)
    if result and os.path.exists(result):
        flash(f"Report generated successfully!", "success")
        return send_file(result, as_attachment=True,
                         download_name=os.path.basename(result))
    flash("Failed to generate report.", "error")
    return redirect(url_for("patient_detail", mrn=mrn))


# ── Delete patient ────────────────────────────────────────────────────────────
@app.route("/patients/<mrn>/delete", methods=["POST"])
def patient_delete(mrn):
    db   = load_db()
    name = db.get(mrn, {}).get("name", mrn)
    delete_patient(mrn)
    flash(f"Patient {name} deleted.", "info")
    return redirect(url_for("patients"))


# ── Guidelines page ───────────────────────────────────────────────────────────
@app.route("/guidelines")
def guidelines():
    conditions = list_conditions()
    return render_template("guidelines.html", conditions=conditions)


# ── Generate full guidelines PDF ──────────────────────────────────────────────
@app.route("/guidelines/generate")
def generate_guidelines():
    result = generate_pdf(output_filename="clinical_guidelines.pdf")
    if result and os.path.exists(result):
        return send_file(result, as_attachment=True,
                         download_name="clinical_guidelines.pdf")
    flash("Failed to generate guidelines PDF.", "error")
    return redirect(url_for("guidelines"))


# ── ICD-10 search API ─────────────────────────────────────────────────────────
@app.route("/api/icd10")
def api_icd10():
    code = request.args.get("code", "").strip()
    if code:
        return jsonify(lookup(code))
    return jsonify({"error": "No code provided"})


# ── Reports list ──────────────────────────────────────────────────────────────
@app.route("/reports")
def reports():
    files = []
    if os.path.exists(REPORTS_DIR):
        for f in sorted(os.listdir(REPORTS_DIR)):
            if f.endswith(".pdf"):
                path = os.path.join(REPORTS_DIR, f)
                files.append({
                    "name": f,
                    "size": f"{os.path.getsize(path) // 1024} KB",
                    "path": path,
                })
    return render_template("reports.html", files=files)


# ── Download a report ─────────────────────────────────────────────────────────
@app.route("/reports/<filename>")
def download_report(filename):
    filepath = os.path.join(REPORTS_DIR, filename)
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True, download_name=filename)
    flash("Report not found.", "error")
    return redirect(url_for("reports"))


if __name__ == "__main__":
    print("=== ClinicalDocsPro Web Dashboard ===")
    print("  Open your browser at: http://127.0.0.1:5000")
    print("  Press Ctrl+C to stop\n")
    app.run(debug=True, port=5000)