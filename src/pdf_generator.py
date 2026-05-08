# pdf_generator.py
# Reads condition .txt files and generates formatted PDF guideline reports

import os
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

# Import project‑specific helpers
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils import (
    BASE_DIR, CONDITIONS_DIR, REPORTS_DIR,
    NAVY, BLUE, LGREY, WHITE, STRIP, NOTE, WARN,
    get_styles, get_condition_colour, list_conditions, read_file
)

PAGE_W, PAGE_H = letter
MARGIN = 0.85 * inch

# ── Page Header & Footer ──────────────────────────────────────────────────────
def make_page(canvas, doc):
    canvas.saveState()
    # Header bar
    canvas.setFillColor(NAVY)
    canvas.rect(0, PAGE_H - 34, PAGE_W, 34, fill=1, stroke=0)
    canvas.setFillColor(WHITE)
    canvas.setFont("Helvetica-Bold", 8.5)
    canvas.drawString(MARGIN, PAGE_H - 21, "CLINICALDOCSPRO — MEDICAL DOCUMENTATION SYSTEM")
    canvas.setFont("Helvetica", 8.5)
    canvas.drawRightString(PAGE_W - MARGIN, PAGE_H - 21, "General Hospital  |  May 2026")
    # Footer bar
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, PAGE_W, 26, fill=1, stroke=0)
    canvas.setFillColor(WHITE)
    canvas.setFont("Helvetica", 7.5)
    canvas.drawString(MARGIN, 8, "FOR EDUCATIONAL USE ONLY — NOT FOR DIRECT CLINICAL USE")
    canvas.drawRightString(PAGE_W - MARGIN, 8, f"Page {doc.page}")
    canvas.restoreState()

# ── Reusable Table Builder ────────────────────────────────────────────────────
def build_table(data, col_widths, header_colour=NAVY, row_colours=(WHITE, STRIP)):
    t = Table(data, colWidths=col_widths)
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0),  header_colour),
        ("TEXTCOLOR",     (0, 0), (-1, 0),  WHITE),
        ("FONTNAME",      (0, 0), (-1, 0),  "Helvetica-Bold"),
        ("FONTSIZE",      (0, 0), (-1, -1), 8.5),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1), row_colours),
        ("GRID",          (0, 0), (-1, -1), 0.35, LGREY),
        ("TOPPADDING",    (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING",   (0, 0), (-1, -1), 5),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 5),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
        ("WORDWRAP",      (0, 0), (-1, -1), True),
    ]))
    return t

# ── Colour Badge (section header) ────────────────────────────────────────────
def build_badge(text, colour):
    style = ParagraphStyle(
        "Badge", fontName="Helvetica-Bold", fontSize=11,
        textColor=WHITE, alignment=TA_CENTER
    )
    data = [[Paragraph(text, style)]]
    t = Table(data, colWidths=[PAGE_W - 2 * MARGIN])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), colour),
        ("TOPPADDING",    (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    return t

# ── HR Line Helper ────────────────────────────────────────────────────────────
def hr(colour=NAVY, thickness=1.5):
    return HRFlowable(
        width="100%", thickness=thickness,
        color=colour, spaceAfter=5
    )

def section_rule(colour=NAVY):
    return HRFlowable(
        width="100%", thickness=0.5,
        color=colour, spaceBefore=2, spaceAfter=8
    )

# ── Parse a condition .txt file into sections ─────────────────────────────────
def parse_condition_file(filepath):
    """
    Reads a condition .txt file and returns a list of
    (section_title, lines[]) tuples.
    """
    content = read_file(filepath)
    sections = []
    current_title = "Overview"
    current_lines = []

    for line in content.splitlines():
        stripped = line.strip()
        # Detect numbered section headers e.g. "1. WHAT IS DIABETES?"
        if stripped and stripped[0].isdigit() and ". " in stripped[:6]:
            if current_lines:
                sections.append((current_title, current_lines))
            current_title = stripped
            current_lines = []
        elif stripped.startswith("=") or stripped.startswith("-" * 5):
            continue  # skip decorative lines
        elif stripped:
            current_lines.append(stripped)

    if current_lines:
        sections.append((current_title, current_lines))

    return sections

# ── Build story elements for one condition ────────────────────────────────────
def build_condition_story(filename, styles):
    filepath = os.path.join(CONDITIONS_DIR, filename)
    colour   = get_condition_colour(filename)
    name     = os.path.splitext(filename)[0].replace("_", " ").title()
    sections = parse_condition_file(filepath)
    story    = []

    # Section badge
    story.append(build_badge(name.upper(), colour))
    story.append(Spacer(1, 0.1 * inch))

    for title, lines in sections:
        # Section heading
        h1_style = ParagraphStyle(
            f"H1_{name}_{title[:10]}",
            parent=get_styles()["h1"],
            textColor=colour
        )
        story.append(Paragraph(title, h1_style))
        story.append(HRFlowable(
            width="100%", thickness=0.5,
            color=colour, spaceBefore=2, spaceAfter=8
        ))

        for line in lines:
            # Bullet points
            if line.startswith("-"):
                text = line.lstrip("- ").strip()
                story.append(Paragraph(f"• {text}", styles["bullet"]))
            # Sub-bullets
            elif line.startswith("  -") or line.startswith("    -"):
                text = line.lstrip(" -").strip()
                story.append(Paragraph(f"    ◦ {text}", styles["bullet"]))
            # Note lines
            elif line.lower().startswith("note:"):
                story.append(Paragraph(f"<i>{line}</i>", styles["note"]))
            # Warning lines
            elif line.lower().startswith("important:") or line.lower().startswith("warning:"):
                story.append(Paragraph(f"<b>{line}</b>", styles["warn"]))
            # Regular body text
            else:
                story.append(Paragraph(line, styles["body"]))

        story.append(Spacer(1, 0.06 * inch))

    story.append(PageBreak())
    return story

# ── Main PDF Generator ────────────────────────────────────────────────────────
def generate_pdf(
    output_filename="clinical_guidelines.pdf",
    condition_files=None,
    title="Clinical Practice Guidelines",
    subtitle="Comprehensive Chronic Disease Reference"
):
    """
    Generate a PDF from condition .txt files.

    Args:
        output_filename : name of the output PDF file
        condition_files : list of .txt filenames to include
                          (None = include all conditions)
        title           : document title shown on cover
        subtitle        : document subtitle shown on cover
    """
    os.makedirs(REPORTS_DIR, exist_ok=True)
    output_path = os.path.join(REPORTS_DIR, output_filename)

    # Default to all conditions if none specified
    if condition_files is None:
        condition_files = list_conditions()

    if not condition_files:
        print("No condition files found in conditions/ folder.")
        return None

    # Set up document
    doc = BaseDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=MARGIN,
        leftMargin=MARGIN,
        topMargin=MARGIN + 18,
        bottomMargin=MARGIN,
        title=title,
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

    # ── Cover Page ────────────────────────────────────────────────────────────
    story.append(Spacer(1, 0.4 * inch))
    story.append(Paragraph(title.upper(), styles["title"]))
    story.append(Paragraph(subtitle, styles["subtitle"]))
    story.append(Spacer(1, 0.05 * inch))
    story.append(Paragraph(
        f"Version 1.0  |  May 2026  |  ClinicalDocsPro  |  {len(condition_files)} Conditions",
        styles["meta"]
    ))
    story.append(hr(NAVY, 2))
    story.append(Spacer(1, 0.15 * inch))

    # Cover info table
    cover_data = [
        ["System:",       "ClinicalDocsPro — Medical Documentation System"],
        ["Conditions:",   ", ".join(
            f.replace(".txt","").replace("_"," ").title()
            for f in condition_files
        )],
        ["Output:",       output_path],
        ["Classification:", "Educational Reference — Not for Direct Clinical Use"],
    ]
    cover_table = Table(cover_data, colWidths=[1.5 * inch, 5.35 * inch])
    cover_table.setStyle(TableStyle([
        ("FONTNAME",        (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTSIZE",        (0, 0), (-1, -1), 9),
        ("TEXTCOLOR",       (0, 0), (0, -1), NAVY),
        ("TOPPADDING",      (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING",   (0, 0), (-1, -1), 5),
        ("LEFTPADDING",     (0, 0), (-1, -1), 6),
        ("ROWBACKGROUNDS",  (0, 0), (-1, -1), [NOTE, WHITE]),
        ("GRID",            (0, 0), (-1, -1), 0.3, LGREY),
    ]))
    story.append(cover_table)
    story.append(PageBreak())

    # ── Condition Sections ────────────────────────────────────────────────────
    for i, filename in enumerate(condition_files):
        print(f"  [{i+1}/{len(condition_files)}] Adding: {filename}")
        story.extend(build_condition_story(filename, styles))

    # ── Disclaimer Page ───────────────────────────────────────────────────────
    story.append(Spacer(1, 0.3 * inch))
    story.append(hr(LGREY, 0.5))
    story.append(Spacer(1, 0.1 * inch))
    story.append(Paragraph(
        "DISCLAIMER: This document is generated by ClinicalDocsPro for educational and "
        "reference purposes only. It does not constitute medical advice and must not be "
        "used for direct clinical decision-making without qualified physician review. "
        "All patient examples are entirely fictional.",
        styles["disc"]
    ))

    # ── Build PDF ─────────────────────────────────────────────────────────────
    print(f"\nBuilding PDF...")
    doc.build(story)
    print(f"Done! PDF saved to: {output_path}")
    return output_path

# ── Run directly to test ──────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=== ClinicalDocsPro — PDF Generator ===\n")
    print("Conditions found:")
    conditions = list_conditions()
    for c in conditions:
        print(f"  • {c}")

    print(f"\nGenerating PDF with {len(conditions)} conditions...\n")
    result = generate_pdf(
        output_filename="clinical_guidelines.pdf",
        title="Clinical Practice Guidelines",
        subtitle="Diabetes · Hypertension · Heart Failure · CKD · COPD · AF · Lipids · Asthma · Obesity · Depression"
    )
    if result:
        print(f"\nSuccess! Open: {result}")