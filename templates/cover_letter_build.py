#!/usr/bin/env python3
"""1-page cover letter as a text-based PDF, matching the resume builder's look (blue 1F4E79 title).

Copy it to profile/cover_letter_build.py, replace the invented data in LETTER, then:
  pip install reportlab
  python profile/cover_letter_build.py applications/<Company>_<Role>/<First>_<Last>_<Role>_<Company>_Cover_Letter.pdf

Layout follows templates/cover-letter.md. Helvetica is built into every PDF reader and matches Arial's metrics,
so no font files are needed.
"""
import sys
from xml.sax.saxutils import escape

from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

# Everything below is invented. Maya Tan is not a real person.
LETTER = {
    "name": "Maya Tan",
    "contact": ["Singapore | +65 8000 0000 | maya.tan@example.com", "linkedin.com/in/example | github.com/example"],
    "date": "18 Nov 2026",
    "to": ["Hiring Team", "Acme Pay", "Singapore"],
    "role": "Senior Backend Engineer, Payments",
    "salutation": "Dear Hiring Team,",
    "paragraphs": [
        "I'm applying for the Senior Backend Engineer, Payments role. Your posting centres on backend services in "
        "Python or Go, PostgreSQL query performance and event-driven work on AWS, and that is the work I've done for "
        "the last 6 years in billing, logistics and retail.",
        "At Northwind Logistics I owned the billing migration to PostgreSQL end to end, moving 2 million invoices with "
        "no reconciliation errors. I also cut p95 API latency by 40% by rewriting the slowest queries and adding "
        "covering indexes, and built an event-driven order pipeline on Lambda and SQS that handles 300,000 messages a day.",
        "I haven't worked on payment systems or with PCI DSS, and I haven't used Kafka. The closest I have is billing "
        "work: the invoice migration above, and invoice-diff, an open-source Python CLI that compares invoice exports "
        "between two databases and reports mismatches.",
        "I'm a Singapore Permanent Resident, no sponsorship needed, and available with 1 month notice. "
        "I'd welcome a conversation about the role.",
    ],
    "closing": "Kind regards,",
}

BLUE = HexColor("#1F4E79")
FONT, BOLD = "Helvetica", "Helvetica-Bold"
contact = ParagraphStyle("contact", fontName=FONT, fontSize=10, leading=13, alignment=TA_RIGHT)
body = ParagraphStyle("body", fontName=FONT, fontSize=10.5, leading=14.2, spaceAfter=9)
title = ParagraphStyle("title", parent=body, fontName=BOLD, fontSize=11.5, leading=15, textColor=BLUE, spaceBefore=14, spaceAfter=14)
closing = ParagraphStyle("closing", parent=body, spaceBefore=6, spaceAfter=0)

L = {k: escape(v) if isinstance(v, str) else [escape(x) for x in v] for k, v in LETTER.items()}  # & and < break reportlab markup
story = [
    Paragraph(f"<b>{L['name']}</b>", contact),
    *[Paragraph(line, contact) for line in L["contact"]],
    Spacer(1, 12),
    Paragraph(L["date"], body),
    Paragraph("<br/>".join(L["to"]), body),
    Paragraph(f"Application for {L['role']}", title),
    Paragraph(L["salutation"], body),
    *[Paragraph(p, body) for p in L["paragraphs"]],
    Paragraph(f"{L['closing']}<br/>{L['name']}", closing),
]

out = sys.argv[1] if len(sys.argv) > 1 else "cover_letter.pdf"
SimpleDocTemplate(
    out, pagesize=A4,  # US Letter: from reportlab.lib.pagesizes import letter
    leftMargin=23 * mm, rightMargin=23 * mm, topMargin=19 * mm, bottomMargin=19 * mm,
    title=f"{LETTER['name']} Cover Letter", author=LETTER["name"],
).build(story)
print(f"Wrote {out}")
