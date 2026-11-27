# Changelog

## 2.5.0 (2026-11-27)

Added `templates/cover_letter_build.py`: a reportlab builder for the 1-page PDF cover letter, in the same look as the resume (right-aligned contact block, bold blue "Application for" title, Helvetica 10.5pt, A4). It escapes `&` and `<` so company names like "R&D" render. The skill now uses it to render cover letters, and the test suite builds it, checks it is 1 text-based page, and checks the ATS check catches a letter that spills onto page 2.

## 2.4.1 (2026-11-26)

Added `tests/run_tests.py` and a GitHub Actions workflow that runs it on every push and pull request, with LibreOffice for real page counts. It checks version sync, the plugin manifests, the check script's self-test, and builds the example resume (plus no-certifications, no-link and no-projects variants) through the ATS check and the house-style checks.

## 2.4.0 (2026-11-26)

Removed the "Tech stack" line under each job from `templates/resume_build.js`, and the skill no longer adds one. JD tools go in the bullets and the Skills section. The optional "Selected projects" line stays.

## 2.3.0 (2026-11-26)

`templates/resume_build.js` now matches a real, ATS-checked resume in every section:

- Name in capitals; tighter header spacing.
- Projects: a bold title line, an italic "Open-source project | link" line (link optional), then bullets.
- Education lines include the location; an optional Certifications line, with the heading switching to "Education and Certifications" when there are any.
- Bullet indent 330/220 and page margins 700 top and bottom, 880 left and right.

## 2.2.0 (2026-11-26)

`templates/resume_build.js` now follows a real working resume more closely:

- One dark blue (`1F4E79`) for the headline and every link, set in a single `BLUE` constant.
- Each job is a bold title line, then an italic `Company | Location | Dates` line, both kept with the bullets that follow.
- Optional "Selected projects:" and "Tech stack:" lines under each job.
- Bullets use a defined `•` list instead of Word's default, with tighter spacing.

## 2.1.2 (2026-11-26)

Section headings in `templates/resume_build.js` are in capitals again (SUMMARY, WORK EXPERIENCE), keeping the 2.1.1 spacing, rule and `keepNext`.

## 2.1.1 (2026-11-26)

`templates/resume_build.js` section headings: tighter spacing (125 before, 45 after), a thinner grey rule (`808080`, size 4), `keepNext` so a heading never sits alone at the bottom of a page, and headings print as written instead of in capitals.

## 2.1.0 (2026-11-18)

`templates/resume_build.js` now matches a real working resume: blue headline, clickable blue email, LinkedIn and GitHub links, and a bold "Availability:" line under the contact details. The format rules allow colour as an accent on the headline and links only.

## 2.0.0 (2026-11-18)

Rebuilt from the full working version of the workflow.

- Facts log rules: latest dated entry wins, OK wording vs not confirmed, unattributed facts stay out of job bullets, "Don't claim" hard stops, situational facts only when asked.
- Keyword method (25 to 35 exact JD phrases, mapped to real experience) and `keywords.txt` per application.
- Optional "Always include" project list and job title variants in the facts log.
- `reference/ats-guide.md`: ATS guide and pre-submission checklist.
- `scripts/ats_check.py`: layout, contact, date, keyword and page-count checks, with a self-test.
- `examples/maya/`: invented candidate and JD for trying and testing the skill.
- Facts template restructured by topic, with dated entries.
- Fixes from the first skill test: page counts are a maximum (never pad), a JD title naming an unclaimable domain is trimmed on the resume, bullet count follows the confirmed facts, the check script warns when it can't verify a PDF's text.

## 1.2.0 (2026-11-18)

Added `templates/resume_build.js`, an optional docx-js resume builder with invented example data. Copy it to `profile/resume_build.js` to get the exact same ATS-safe layout on every application.

## 1.1.1 (2026-11-18)

Added `templates/cover-letter.md`, a Markdown skeleton for the first cover letter, so every agent lays it out the same way.

## 1.1.0 (2026-11-18)

A 1-page PDF cover letter now comes with every JD: same honesty rules and JD focus as the resume, the same layout as your last cover letter, and one honest gap paragraph when there is a real gap. Saved next to the resume and summarised in notes.md.

## 1.0.0 (2026-11-17)

First public release: fit check, JD-only skills rule, honesty rules, ATS format rules, facts log template, Claude Code plugin manifests, AGENTS.md for other agents.
