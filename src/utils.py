# utils.py
# Shared helpers, paths, colours, and styles for ClinicalDocsPro

import os
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT

# ── Project Paths ─────────────────────────────────────────────────────────────
BASE_DIR       = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONDITIONS_DIR = os.path.join(BASE_DIR, "conditions")
PATIENTS_DIR   = os.path.join(BASE_DIR, "patients")
REPORTS_DIR    = os.path.join(BASE_DIR, "reports")

# ── Page Settings ─────────────────────────────────────────────────────────────
PAGE_MARGIN = 0.85 * inch

# ── Colour Palette ────────────────────────────────────────────────────────────
NAVY   = colors.HexColor("#1a3a5c")
BLUE   = colors.HexColor("#2e5f8a")
TEAL   = colors.HexColor("#1a7a6e")
GREEN  = colors.HexColor("#2a6a2a")
PURPLE = colors.HexColor("#5a3a7a")
RED    = colors.HexColor("#8a2020")
ORANGE = colors.HexColor("#8a5010")
SLATE  = colors.HexColor("#3a4a5a")
BROWN  = colors.HexColor("#6a3a1a")
PINK   = colors.HexColor("#7a2050")
LGREY  = colors.HexColor("#aabbcc")
STRIP  = colors.HexColor("#eef2f7")
NOTE   = colors.HexColor("#f0f4f8")
WARN   = colors.HexColor("#fff0f0")
WHITE  = colors.white

# Condition → colour mapping
CONDITION_COLOURS = {
    "diabetes":            TEAL,
    "hypertension":        BLUE,
    "heart_failure":       RED,
    "ckd":                 SLATE,
    "copd":                ORANGE,
    "atrial_fibrillation": PURPLE,
    "hyperlipidaemia":     GREEN,
    "asthma":              PINK,
    "obesity":             BROWN,
    "depression":          NAVY,
}

# ── Style Builder ─────────────────────────────────────────────────────────────
def get_styles():
    SS = getSampleStyleSheet()

    def ps(name, parent="Normal", **kw):
        return ParagraphStyle(name, parent=SS[parent], **kw)

    return {
        "title":    ps("Title",  "Title",   fontSize=22, textColor=NAVY,
                       spaceAfter=4, alignment=TA_CENTER),
        "subtitle": ps("Subt",   "Normal",  fontSize=12, textColor=BLUE,
                       spaceAfter=2, alignment=TA_CENTER),
        "meta":     ps("Meta",   "Normal",  fontSize=8,  textColor=colors.grey,
                       spaceAfter=10, alignment=TA_CENTER),
        "h1":       ps("H1",     "Heading1",fontSize=13, textColor=NAVY,
                       spaceBefore=12, spaceAfter=5),
        "h2":       ps("H2",     "Heading2",fontSize=10.5, textColor=BLUE,
                       spaceBefore=8, spaceAfter=3),
        "body":     ps("Body",   "Normal",  fontSize=9.5, leading=14,
                       spaceAfter=5, alignment=TA_JUSTIFY),
        "bullet":   ps("Bullet", "Normal",  fontSize=9.5, leading=13,
                       leftIndent=16, spaceAfter=2),
        "small":    ps("Small",  "Normal",  fontSize=8.5, leading=11,
                       textColor=colors.HexColor("#444444"), spaceAfter=3),
        "note":     ps("Note",   "Normal",  fontSize=8.5, leading=12,
                       leftIndent=8, backColor=NOTE, borderPad=5, spaceAfter=7),
        "warn":     ps("Warn",   "Normal",  fontSize=8.5, leading=12,
                       leftIndent=8, textColor=colors.HexColor("#7a2020"),
                       backColor=WARN, borderPad=5, spaceAfter=7),
        "disc":     ps("Disc",   "Normal",  fontSize=7.5, leading=10,
                       alignment=TA_CENTER, textColor=colors.grey),
    }

# ── Helper: get colour for a condition ───────────────────────────────────────
def get_condition_colour(filename):
    key = os.path.splitext(os.path.basename(filename))[0].lower()
    return CONDITION_COLOURS.get(key, NAVY)

# ── Helper: list all condition files ─────────────────────────────────────────
def list_conditions():
    if not os.path.exists(CONDITIONS_DIR):
        return []
    return sorted([
        f for f in os.listdir(CONDITIONS_DIR)
        if f.endswith(".txt")
    ])

# ── Helper: read a text file safely ──────────────────────────────────────────
def read_file(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return ""