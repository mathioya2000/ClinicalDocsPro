# report_builder.py
# Combines patient data + condition guidelines into a personalised PDF report

import os
import sys
from datetime import date
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate,
    Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak
)
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import ParagraphStyle

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils import (
    BASE_DIR, CONDITIONS_DIR, REPORTS_DIR,
    NAVY, BLUE, LGREY, WHITE, STRIP, NOTE, WARN,
    get_styles, get_condition_colour, read_file
)
from pdf_generator import make_page, build_badge, build_condition_story, hr
from icd10_lookup import lookup, get_codes_by_category

PAGE_W, PAGE_H = letter
MARGIN = 0.85 * inch


# ── Map ICD-10 categories to condition filenames ──────────────────────────────
CATEGORY_TO_FILE = {
    "Diabetes":            "diabetes.txt",
    "Hypertension":        "hypertension.txt",
    "Heart Failure":       "heart_failure.txt",
    "CKD":                 "ckd.txt",
    "COPD":                "copd.txt",
    "Atrial Fibrillation": "atrial_fibrillation.txt",
    "Hyperlipidaemia":     "hyperlipidaemia.txt",
    "Asthma":              "asthma.txt",
    "Obesity":             "obesity.txt",
    "Depression":          "depression.txt",
}


# ── Patient data structure ────────────────────────────────────────────────────
class Patient:
    def __init__(
        self,
        name,
        dob,
        mrn,
        sex,
        admitting_physician,
        admission_date,
        discharge_date,
        primary_diagnosis,
        secondary_diagnoses=None,
        medications=None,
        allergies=None,
        discharge_instructions=None,
        follow_up=None,
        notes=None,
    ):
        self.name                 = name
        self.dob                  = dob
        self.mrn                  = mrn
        self.sex                  = sex
        self.admitting_physician  = admitting_physician
        self.admission_date       = admission_date
        self.discharge_date       = discharge_date
        self.primary_diagnosis    = primary_diagnosis
        self.secondary_diagnoses  = secondary_diagnoses  or []
        self.medications          = medications          or []
        self.allergies            = allergies            or []
        self.discharge_instructions = discharge_instructions or []
        self.follow_up            = follow_up            or []
        self.notes                = notes                or ""

    def all_icd10_codes(self):
        codes = [self.primary_diagnosis["code"]]
        codes += [d["code"] for d in self.secondary_diagnoses]
        return codes

    def all_categories(self):
        categories = set()
        for code in self.all_icd10_codes():
            info = lookup(code)
            if info["category"] != "Unknown":
                categories.add(info["category"])
        return sorted(categories)

    def condition_files(self):
        files = []
        for cat in self.all_categories():
            fname = CATEGORY_TO_FILE.get(cat)
            if fname:
                fpath = os.path.join(CONDITIONS_DIR, fname)
                if os.path.exists(fpath):
                    files.append(fname)
        return files


# ── Build patient cover page ──────────────────────────────────────────────────
def build_patient_cover(patient, styles):
    story = []

    story.append(Spacer(1, 0.3 * inch))
    story.append(Paragraph("PATIENT CLINICAL REPORT", styles["title"]))
    story.append(Paragraph("Discharge Summary & Condition Guidelines", styles["subtitle"]))
    story.append(Spacer(1, 0.04 * inch))
    story.append(Paragraph(
        f"Generated: {date.today().strftime('%B %d, %Y')}  |  ClinicalDocsPro  |  CONFIDENTIAL",
        styles["meta"]
    ))
    story.append(hr(NAVY, 2))
    story.append(Spacer(1, 0.12 * inch))

    # Patient info table
    patient_data = [
        ["Patient Name:",       patient.name],
        ["Date of Birth:",      patient.dob],
        ["MRN:",                patient.mrn],
        ["Sex:",                patient.sex],
        ["Admitting Physician:", patient.admitting_physician],
        ["Admission Date:",     patient.admission_date],
        ["Discharge Date:",     patient.discharge_date],
    ]
    pt = Table(patient_data, colWidths=[1.8 * inch, 5.05 * inch])
    pt.setStyle(TableStyle([
        ("FONTNAME",       (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTSIZE",       (0, 0), (-1, -1), 9.5),
        ("TEXTCOLOR",      (0, 0), (0, -1), NAVY),
        ("TOPPADDING",     (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING",  (0, 0), (-1, -1), 5),
        ("LEFTPADDING",    (0, 0), (-1, -1), 6),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [NOTE, WHITE]),
        ("GRID",           (0, 0), (-1, -1), 0.3, LGREY),
    ]))
    story.append(pt)
    story.append(Spacer(1, 0.15 * inch))

    # Diagnoses table
    story.append(Paragraph("Diagnoses", styles["h1"]))
    story.append(HRFlowable(width="100%", thickness=0.5, color=NAVY,
                            spaceBefore=2, spaceAfter=8))

    diag_data = [["Type", "ICD-10 Code", "Description"]]
    pri = patient.primary_diagnosis
    diag_data.append(["PRIMARY", pri["code"], lookup(pri["code"])["name"]])
    for d in patient.secondary_diagnoses:
        diag_data.append(["Secondary", d["code"], lookup(d["code"])["name"]])

    dt = Table(diag_data, colWidths=[1.2 * inch, 1.3 * inch, 4.35 * inch])
    dt.setStyle(TableStyle([
        ("BACKGROUND",     (0, 0), (-1, 0),  NAVY),
        ("TEXTCOLOR",      (0, 0), (-1, 0),  WHITE),
        ("FONTNAME",       (0, 0), (-1, 0),  "Helvetica-Bold"),
        ("FONTSIZE",       (0, 0), (-1, -1), 9),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, STRIP]),
        ("GRID",           (0, 0), (-1, -1), 0.35, LGREY),
        ("TOPPADDING",     (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING",  (0, 0), (-1, -1), 5),
        ("LEFTPADDING",    (0, 0), (-1, -1), 5),
        ("FONTNAME",       (0, 1), (0, 1),   "Helvetica-Bold"),
        ("TEXTCOLOR",      (0, 1), (0, 1),   colors.HexColor("#8a2020")),
    ]))
    story.append(dt)
    story.append(Spacer(1, 0.15 * inch))

    # Medications table
    if patient.medications:
        story.append(Paragraph("Discharge Medications", styles["h1"]))
        story.append(HRFlowable(width="100%", thickness=0.5, color=NAVY,
                                spaceBefore=2, spaceAfter=8))
        med_data = [["#", "Medication", "Dose", "Route", "Frequency", "Purpose"]]
        for i, med in enumerate(patient.medications, 1):
            med_data.append([
                str(i),
                med.get("name", ""),
                med.get("dose", ""),
                med.get("route", ""),
                med.get("frequency", ""),
                med.get("purpose", ""),
            ])
        mt = Table(med_data, colWidths=[
            0.3*inch, 1.6*inch, 0.8*inch, 0.6*inch, 1.1*inch, 2.45*inch
        ])
        mt.setStyle(TableStyle([
            ("BACKGROUND",     (0, 0), (-1, 0),  BLUE),
            ("TEXTCOLOR",      (0, 0), (-1, 0),  WHITE),
            ("FONTNAME",       (0, 0), (-1, 0),  "Helvetica-Bold"),
            ("FONTSIZE",       (0, 0), (-1, -1), 8.5),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, STRIP]),
            ("GRID",           (0, 0), (-1, -1), 0.35, LGREY),
            ("TOPPADDING",     (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING",  (0, 0), (-1, -1), 4),
            ("LEFTPADDING",    (0, 0), (-1, -1), 4),
            ("WORDWRAP",       (0, 0), (-1, -1), True),
        ]))
        story.append(mt)
        story.append(Spacer(1, 0.15 * inch))

    # Allergies
    if patient.allergies:
        story.append(Paragraph("Allergies", styles["h1"]))
        story.append(HRFlowable(width="100%", thickness=0.5, color=NAVY,
                                spaceBefore=2, spaceAfter=8))
        for allergy in patient.allergies:
            story.append(Paragraph(
                f"• <b>{allergy['name']}</b> — {allergy['reaction']}",
                styles["bullet"]
            ))
        story.append(Spacer(1, 0.1 * inch))

    # Discharge instructions
    if patient.discharge_instructions:
        story.append(Paragraph("Discharge Instructions", styles["h1"]))
        story.append(HRFlowable(width="100%", thickness=0.5, color=NAVY,
                                spaceBefore=2, spaceAfter=8))
        for instruction in patient.discharge_instructions:
            story.append(Paragraph(f"• {instruction}", styles["bullet"]))
        story.append(Spacer(1, 0.1 * inch))

    # Follow-up appointments
    if patient.follow_up:
        story.append(Paragraph("Follow-Up Appointments", styles["h1"]))
        story.append(HRFlowable(width="100%", thickness=0.5, color=NAVY,
                                spaceBefore=2, spaceAfter=8))
        fu_data = [["Provider", "Specialty", "Date", "Contact"]]
        for fu in patient.follow_up:
            fu_data.append([
                fu.get("provider", ""),
                fu.get("specialty", ""),
                fu.get("date", ""),
                fu.get("contact", ""),
            ])
        fut = Table(fu_data, colWidths=[1.8*inch, 1.5*inch, 1.5*inch, 2.05*inch])
        fut.setStyle(TableStyle([
            ("BACKGROUND",     (0, 0), (-1, 0),  NAVY),
            ("TEXTCOLOR",      (0, 0), (-1, 0),  WHITE),
            ("FONTNAME",       (0, 0), (-1, 0),  "Helvetica-Bold"),
            ("FONTSIZE",       (0, 0), (-1, -1), 8.5),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, STRIP]),
            ("GRID",           (0, 0), (-1, -1), 0.35, LGREY),
            ("TOPPADDING",     (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING",  (0, 0), (-1, -1), 4),
            ("LEFTPADDING",    (0, 0), (-1, -1), 5),
        ]))
        story.append(fut)
        story.append(Spacer(1, 0.1 * inch))

    # Clinical notes
    if patient.notes:
        story.append(Paragraph("Clinical Notes", styles["h1"]))
        story.append(HRFlowable(width="100%", thickness=0.5, color=NAVY,
                                spaceBefore=2, spaceAfter=8))
        story.append(Paragraph(patient.notes, styles["body"]))

    story.append(PageBreak())
    return story


# ── Main report builder ───────────────────────────────────────────────────────
def build_report(patient, include_guidelines=True, output_filename=None):
    """
    Build a full patient PDF report including:
    - Patient cover page (demographics, diagnoses, medications)
    - Relevant condition guidelines based on ICD-10 codes

    Args:
        patient           : Patient object
        include_guidelines: Whether to append condition guidelines
        output_filename   : Custom output filename (default: MRN_report.pdf)
    """
    os.makedirs(REPORTS_DIR, exist_ok=True)

    if output_filename is None:
        safe_name = patient.name.replace(" ", "_").lower()
        output_filename = f"{safe_name}_{patient.mrn}_report.pdf"

    output_path = os.path.join(REPORTS_DIR, output_filename)

    doc = BaseDocTemplate(
        output_path, pagesize=letter,
        rightMargin=MARGIN, leftMargin=MARGIN,
        topMargin=MARGIN + 18, bottomMargin=MARGIN,
        title=f"Patient Report — {patient.name}",
        author="ClinicalDocsPro"
    )

    frame = Frame(
        MARGIN, MARGIN,
        PAGE_W - 2 * MARGIN,
        PAGE_H - 2 * MARGIN - 18,
        id="main"
    )

    doc.addPageTemplates([
        PageTemplate(id="main", frames=frame, onPage=make_page)
    ])

    styles = get_styles()
    story  = []

    # Patient cover page
    print(f"  Building patient cover page for: {patient.name}")
    story.extend(build_patient_cover(patient, styles))

    # Condition guidelines
    if include_guidelines:
        condition_files = patient.condition_files()
        if condition_files:
            print(f"  Appending {len(condition_files)} condition guideline(s):")
            for fname in condition_files:
                print(f"    • {fname}")
                story.extend(build_condition_story(fname, styles))
        else:
            print("  No matching condition guidelines found.")

    # Disclaimer
    story.append(Spacer(1, 0.2 * inch))
    story.append(HRFlowable(width="100%", thickness=0.5, color=LGREY, spaceAfter=6))
    story.append(Paragraph(
        "DISCLAIMER: This report is generated by ClinicalDocsPro for educational and reference "
        "purposes only. It does not constitute medical advice. All patient data shown is "
        "fictional and for demonstration purposes only.",
        styles["disc"]
    ))

    print(f"\n  Building PDF...")
    doc.build(story)
    print(f"  Saved to: {output_path}")
    return output_path


# ── Sample patient test ───────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=== ClinicalDocsPro — Report Builder ===\n")

    sample_patient = Patient(
        name               = "John M. Doe",
        dob                = "March 14, 1958",
        mrn                = "0047821-B",
        sex                = "Male",
        admitting_physician= "Dr. Sarah L. Martinez, MD",
        admission_date     = "April 28, 2026",
        discharge_date     = "May 3, 2026",
        primary_diagnosis  = {"code": "I50.22"},
        secondary_diagnoses= [
            {"code": "I48.91"},
            {"code": "E11.65"},
            {"code": "N18.32"},
            {"code": "I10"},
        ],
        medications = [
            {"name": "Furosemide",       "dose": "80 mg",    "route": "Oral", "frequency": "BID",          "purpose": "Diuresis"},
            {"name": "Bisoprolol",       "dose": "5 mg",     "route": "Oral", "frequency": "Daily",        "purpose": "Rate/BP control"},
            {"name": "Lisinopril",       "dose": "10 mg",    "route": "Oral", "frequency": "Daily",        "purpose": "HF / BP"},
            {"name": "Apixaban",         "dose": "5 mg",     "route": "Oral", "frequency": "BID",          "purpose": "AFib / stroke prevention"},
            {"name": "Atorvastatin",     "dose": "40 mg",    "route": "Oral", "frequency": "Nightly",      "purpose": "Cholesterol"},
            {"name": "Metformin",        "dose": "500 mg",   "route": "Oral", "frequency": "BID",          "purpose": "Diabetes"},
            {"name": "Insulin Glargine", "dose": "20 units", "route": "SubQ", "frequency": "Bedtime",      "purpose": "Basal insulin"},
            {"name": "Insulin Lispro",   "dose": "4 units",  "route": "SubQ", "frequency": "TID w/ meals", "purpose": "Bolus insulin"},
            {"name": "Aspirin",          "dose": "81 mg",    "route": "Oral", "frequency": "Daily",        "purpose": "Cardioprotection"},
        ],
        allergies = [
            {"name": "Penicillin",  "reaction": "Rash (hives)"},
            {"name": "Sulfa drugs", "reaction": "Angioedema"},
            {"name": "Codeine",     "reaction": "Nausea/vomiting"},
        ],
        discharge_instructions = [
            "Sodium-restricted diet: NO MORE than 1,500 mg sodium per day",
            "Fluid restriction: limit to 1,500 mL (about 6 cups) per day",
            "Weigh yourself EVERY MORNING; call MD if +2 lbs in 1 day or +5 lbs in 1 week",
            "Light walking 10-15 minutes twice daily; gradually increase",
            "Inspect feet daily for sores, blisters, or redness",
            "Call 911 for: sudden severe dyspnoea, chest pain, one-sided weakness, fainting",
        ],
        follow_up = [
            {"provider": "Dr. R. Flores",      "specialty": "Primary Care", "date": "May 7, 2026",  "contact": "(936) 555-0142"},
            {"provider": "Dr. A. Hughes",      "specialty": "Cardiology",   "date": "May 12, 2026", "contact": "(936) 555-0287"},
            {"provider": "Dr. J. Nwachukwu",  "specialty": "Nephrology",   "date": "May 19, 2026", "contact": "(936) 555-0391"},
        ],
        notes = (
            "Patient admitted with acute decompensated heart failure. "
            "5-day admission with IV diuresis achieving 8 lb weight loss. "
            "Atrial fibrillation with RVR rate-controlled. Anticoagulation initiated. "
            "Diabetes regimen adjusted; HbA1c 8.9% at discharge. "
            "Discharged stable with home health services arranged."
        )
    )

    print(f"Patient: {sample_patient.name}")
    print(f"ICD-10 codes: {sample_patient.all_icd10_codes()}")
    print(f"Categories: {sample_patient.all_categories()}")
    print(f"Condition files: {sample_patient.condition_files()}")
    print()

    result = build_report(sample_patient, include_guidelines=True)
    if result:
        print(f"\nSuccess! Report saved to: {result}")