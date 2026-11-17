---
name: ats-cv-tailoring
description: Rewrite your resume for one pasted job description as an ATS-friendly 2-page .docx plus a matching 1-page cover letter, with a fit verdict, a change log and an honest list of gaps. Use when someone pastes a job description (JD) and wants their resume or CV adapted to it, asks for an ATS check, or asks how well they fit a role.
metadata:
  version: 1.1.1
---

# ATS CV Tailoring

Use when the user pastes a job description (JD) and wants their resume rewritten for it.

The output has to pass two readers: an applicant tracking system (ATS) that parses the file and matches keywords, and a recruiter who spends a few seconds on it. Honesty comes before keyword match. A resume that overclaims gets people rejected at interview, or later.

## Sources

Look for a `profile/` folder in the current project:

- `profile/resume.md`: the master resume, the source of truth. Any format works (`.md`, `.docx`, `.pdf`), Markdown is easiest to keep current.
- `profile/facts.md`: the **confirmed facts log**. True things that aren't on the master resume yet, plus limits on how facts may be worded ("led" vs "mentored", "estimated" numbers, tools that belong to no single job). It also holds format preferences.
- `applications/`: earlier rewritten resumes, one folder per application. Start from the closest one.

**First run (no `profile/`):** ask the user to paste or attach their current resume. Create `profile/resume.md` from it and `profile/facts.md` from this skill's `templates/facts.md`, then walk through the template's questions with them before building anything. Don't guess answers to those questions.

## Honesty rules (never break these)

- Claim only what's in `profile/resume.md` or `profile/facts.md`. Never invent tools, metrics, titles, employers, dates, team sizes or certifications.
- Don't move a tool or achievement under a specific job unless the facts log says it belongs there. Tools with no confirmed home stay in Skills or the summary.
- Keep hedged wording exactly as logged. An "estimated 3x" stays estimated. "Mentored" doesn't become "managed", and "familiarity" doesn't become "experience".
- Follow every wording limit in the facts log, even when the JD would reward breaking it.
- If the JD warns against overclaiming or asks for evidence, say so in the fit check.

## JD-only skills rule (the most important one)

The resume must read as if it was written for this one job, not as a list of everything the person has done.

- **Skills section:** only skills the JD names (or clear synonyms) that the person actually has, in the JD's wording and roughly its order. Nothing else.
- **Don't carry skills over** from the master resume, the facts log or earlier applications just because they're true. The facts log is a pool to draw from, not a list to include every time. A Python/AWS JD that never mentions Node.js or Docker gets neither in Skills.
- **Bullets** still describe real work, but name only the tools that matter for this JD. Drop "Tech stack" lines unless they're mostly JD technologies.
- **Projects:** keep the ones that support the JD and drop the rest.
- **JD skills the person lacks never go on the resume.** They go in the reply as gaps.

## Steps

1. **Fit check first.** Read the JD and flag blockers before building anything:
   - location, relocation or work-authorisation limits (country-only roles, named on-site cities, visa sponsorship)
   - required spoken languages
   - seniority mismatch, in either direction
   - mandatory domain experience or certifications
   - a duplicate of a role already applied for (check `applications/`)

   Give a one-line rating: strong, good, moderate or long shot. If there's a hard blocker, say so and ask whether to continue before building.
2. **Build** the new resume from the closest earlier application or the master:
   - Headline: the exact JD job title plus a short focus line.
   - Summary: 3 to 4 lines in the JD's language, using confirmed facts only.
   - Skills: 5 to 7 lines of `Category: a, b, c`, following the JD-only rule.
   - Most recent role: about 7 bullets, reordered and reworded for the JD, each starting with a verb and carrying a number where one is confirmed. Older roles get fewer bullets.
   - Roles in reverse chronological order, by start date.
3. **Render the .docx** with whatever the environment has: a docx skill, `python-docx`, the `docx` npm package, or `pandoc`. Follow the format rules below.
4. **Verify:**
   - Page count is 2 (or the count set in `profile/facts.md`). Convert to PDF with LibreOffice (`soffice --headless --convert-to pdf`) when it's available. If no converter exists, say the count is unverified.
   - Plain-text check: extract the text (`pandoc -t plain`, `python-docx`, or unzip `word/document.xml`) and confirm the JD's key terms appear, the reading order is right, and nothing is lost in headers, footers or text boxes.
5. **Self-review** the summary, skills and bullets against the honesty rules. Remove any claim that isn't confirmed and any skill the JD doesn't name.
6. **Cover letter (every JD, always):** write a 1-page PDF cover letter alongside the resume, in the same layout every time. Start from the most recent cover letter in `applications/` so the format stays identical across applications. First time, fill in this skill's `templates/cover-letter.md`, which sets the layout, the heading and the paragraph order.
   - The same honesty rules and JD-only focus as the resume. Lead with what matches the JD. Never claim a skill the person lacks.
   - Render it and confirm it's 1 page.
7. **Save** to `applications/<Company>_<Role>/`: the resume `.docx`, the cover letter PDF, any build scripts, and `notes.md` holding the fit verdict, the choices made, the gaps, the full JD text, and a short "Cover letter" section (date, file name, paragraph flow, the gap line, and anything deliberately not claimed).
8. **Reply briefly:**
   - fit verdict and blockers
   - what changed, in 3 to 5 points
   - one line saying the cover letter is attached
   - a numbered list of **gaps only** (JD requirements the person doesn't have, or hasn't confirmed)
   - one focused question, usually whether they have experience with the biggest gap

## When the user confirms a new fact

Add it to `profile/facts.md` with the exact wording they approved and any limits on it, update `profile/resume.md` if it belongs there, and rebuild the current resume. Offer to update other open applications it affects. A new fact goes into future resumes only when that JD asks for it.

## Format rules (ATS-safe)

Defaults. `profile/facts.md` can override any of them.

- One column. No tables, text boxes, columns, images, icons, charts or skill bars.
- Contact details in the body, not in the page header or footer.
- Standard section headings: Summary, Skills, Experience, Projects, Education, Certifications.
- Calibri, Arial or another system font, 10 to 11pt. A4 or US Letter to match the job's country.
- Dates as `Mon YYYY – Mon YYYY`, the same way everywhere.
- Plain bullets (• or -), no custom symbols.
- File names, no spaces: `<First>_<Last>_<Role>_<Company>.docx` for the resume, `<First>_<Last>_<Role>_<Company>_Cover_Letter.pdf` for the cover letter.
- Submit the resume as `.docx` unless the posting asks for PDF.
