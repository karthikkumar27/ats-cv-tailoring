# Changelog

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
