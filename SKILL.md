---
name: ats-cv-tailoring
description: Rewrite your resume for one pasted job description as an ATS-friendly 2-page .docx plus a matching 1-page cover letter, with a fit verdict, a change log and an honest list of gaps. Use when someone pastes a job description (JD) and wants their resume or CV adapted to it, asks for an ATS check, or asks how well they fit a role.
metadata:
  version: 2.1.2
---

# ATS CV Tailoring

Use when the user pastes a job description (JD) and wants their resume rewritten for it.

The output has to pass two readers: an applicant tracking system (ATS) that parses the file and matches keywords, and a recruiter who spends a few seconds on it. Honesty comes before keyword match. A resume that overclaims gets people rejected at interview, or later.

## Sources

In the current project:

- `profile/resume_build.js` or `profile/resume.md`: the master resume, the source of truth. If the build script exists it wins, because it also fixes the layout. Otherwise any format works (`.md`, `.docx`, `.pdf`).
- `profile/facts.md`: the **confirmed facts log** and the user's standing rules (see "Reading the facts log").
- `applications/`: earlier applications, one folder per job. Start from the closest one.

In this skill's folder:

- `reference/ats-guide.md`: ATS do's and don'ts, the keyword method and the pre-submission checklist. Follow it on every application.
- `templates/`: `facts.md`, `cover-letter.md` and `resume_build.js` for first runs.
- `scripts/ats_check.py`: the mechanical checks (layout, contact, dates, keywords, page counts).

Per job, the user gives the JD (pasted text or a file) and any application notes, such as "PDF required" or "they asked for expected salary".

**First run (no `profile/`):** ask the user to paste or attach their current resume. Create `profile/resume.md` from it and `profile/facts.md` from `templates/facts.md`, then go through the template's first-run questions with them before building anything. Don't guess answers.

## Reading the facts log

`profile/facts.md` is a dated log. It grows over many applications, so read it with these rules:

- **The latest dated entry wins.** When two entries disagree, use the newer one, and treat older wording as replaced even if nobody deleted it.
- **Each fact carries its limits.** An entry usually says what's OK to write ("OK: 'led an offshore vendor team'") and what isn't confirmed ("Not confirmed: vendor selection"). Use the OK wording; never write the unconfirmed part.
- **Facts with no confirmed employer stay out of job bullets.** Put them in Skills or the Summary only. The same goes for facts marked "assumed" (an assumed employer isn't a confirmed one).
- **"Don't claim" entries are hard stops**, even when the JD asks for exactly that.
- **Situational facts appear only when the JD asks:** expected salary, travel, driving licence, notice period changes, and similar.
- **Work authorisation:** use the exact phrase logged. If the JD restricts who can apply ("citizens only", "no sponsorship", "local work rights only") and the log doesn't clearly meet it, that's a blocker in the fit check.
- **Standing rules in the log override this skill's defaults**: an "Always include" project list, job title variants by role type, page count, paper size, font, file names.

## Honesty rules (never break these)

- Claim only what's in the master resume or the facts log. Never invent tools, metrics, titles, employers, dates, team sizes or certifications.
- Keep hedged wording exactly as logged. An "estimated 3x" stays estimated. "Mentored" doesn't become "managed", and "familiarity" doesn't become "experience".
- Labels stay on: "(personal projects)", "(self-learning)", "(currently learning)".
- A credential that isn't earned yet is written as `[expected completion: Mon YYYY]`, or left out.
- Never include date of birth, a photo, marital status or a reason for leaving.
- Where the person has a close equivalent to a JD skill (Azure DevOps for "GitHub Actions", say), ask before using it. Don't substitute silently.
- If the JD warns against overclaiming or asks for evidence, say so in the fit check.

## JD-only rules (the most important ones)

The resume must read as if it was written for this one job, not as a list of everything the person has done.

1. **Skills section:** only skills the JD names (or clear synonyms) that the person actually has, in the JD's exact wording. If the JD writes "Google Cloud Platform (GCP)", so does the resume.
2. **Don't carry skills over** from the master resume, the facts log or earlier applications just because they're true. The facts log is a pool to draw from, not a list to include every time. A Python/AWS JD that never mentions Node.js or Docker gets neither in Skills.
3. **Order:** the most JD-relevant category first, and JD-matching skills first within each category.
4. **Back up the top JD skills** in the Summary or a bullet too, not only in the Skills list.
5. **Bullets** describe real work, but name only the tools that matter for this JD. Drop "Tech stack" lines unless they're mostly JD technologies.
6. **Projects:** keep the ones that support the JD and drop the rest, unless the facts log has an "Always include" list. Those stay on every resume; they can be shortened or merged into one bullet, never dropped.
7. **JD skills the person lacks never go on the resume.** They go in the reply and `notes.md` as gaps.

## Keywords

Follow section 4 of `reference/ats-guide.md`:

- Pull from the JD: the exact job title, hard skills and tools, certifications, domain terms, and any phrase repeated 2 or more times (those come first).
- Map each keyword to a real place in the resume (Summary, Skills or a bullet) or mark it a gap. Never place a keyword the person can't back up.
- Aim for 25 to 35 matched keywords, spread naturally. Fewer is fine when the person doesn't have more; never pad.
- Use the JD's exact phrase and acronym style. Write both forms once where it helps: "Amazon Web Services (AWS)".
- No keyword stuffing, no hidden or white text, no pasted JD.

## Steps

1. **Fit check first.** Read the JD and flag blockers before building anything:
   - location, relocation or work-authorisation limits, checked against the facts log
   - required spoken languages
   - seniority mismatch, in either direction
   - mandatory domain experience or certifications
   - a duplicate of a role already applied for (check `applications/`)

   Give a one-line rating: strong, good, moderate or long shot. If there's a hard blocker, say so and ask whether to continue before building.
2. **Keywords:** list them and map each one (see "Keywords"). Save the matched list as `applications/<Company>_<Role>/keywords.txt`, one per line.
3. **Build** from the closest earlier application, or from the master:
   - Headline: the exact JD job title plus a short focus line. Use the job title variant the facts log sets for this kind of role. If the JD title names a domain the person can't claim ("Senior Backend Engineer, Payments" with payments on the "Don't claim" list), drop that part on the resume. The cover letter heading still uses the full title, because there it names the role being applied for.
   - Summary: 3 to 4 lines in the JD's language, using confirmed facts only. The exact JD title appears in the first line.
   - Skills: 5 to 7 lines of `Category: a, b, c`, following the JD-only rules.
   - Most recent role: up to about 7 bullets, only as many as confirmed facts support, reordered and reworded for the JD. Each one is action verb + task (with a JD keyword) + a measured result where one is confirmed. Older roles get fewer bullets.
   - Roles in reverse chronological order, by start date.
4. **Render the .docx.** If `profile/resume_build.js` exists, copy it into the application folder, change only the content, and run it with `node`. Otherwise copy `templates/resume_build.js` the same way, or use what the environment has: a docx skill, `python-docx` or `pandoc`. Follow the format rules below.
5. **Check:** run `python scripts/ats_check.py <resume.docx> --keywords <keywords.txt> --pages 2` from this skill's folder. `--pages` is a maximum. It fails on tables, text boxes, images, text in headers or footers, missing contact details, mixed date formats, unmatched keywords and too many pages. Fix every failure and run it again. If it reports the page count as unverified (no PDF converter), say so in the reply.
6. **Self-review** against the honesty rules and the pre-submission checklist in `reference/ats-guide.md`. Remove any claim that isn't confirmed and any skill the JD doesn't name.
7. **Cover letter (every JD, always):** a 1-page PDF next to the resume, in the same layout every time. Start from the most recent cover letter in `applications/`. First time, fill in `templates/cover-letter.md`.
   - Same honesty rules and JD-only focus as the resume. Lead with what matches the JD. Never claim a skill the person lacks.
   - One plain gap paragraph when there's a real gap: what's missing, and the closest thing they have done.
   - Check it with `python scripts/ats_check.py <cover-letter.pdf> --pages 1`.
8. **Save** to `applications/<Company>_<Role>/`: the resume `.docx`, the cover letter PDF, any build scripts, `keywords.txt`, and `notes.md` with:
   - the fit verdict and blockers
   - the exact title used and the number of keywords matched
   - the choices made (what was cut, reordered or reworded, and why)
   - the gaps
   - a "Cover letter" section: date, file name, paragraph flow, the gap line, and anything deliberately not claimed
   - the full JD text
9. **Reply briefly:**
   - fit verdict and blockers
   - what changed, in 3 to 5 points
   - one line saying the cover letter is attached
   - a numbered list of **gaps only** (JD requirements the person doesn't have, or hasn't confirmed)
   - one focused question, usually whether they have experience with the biggest gap

## When the user confirms a new fact

- Add a dated entry to `profile/facts.md` in their approved wording, with what's OK to write and what still isn't confirmed.
- If it replaces an older entry, say so in the new entry ("replaces the 14 Oct note") and update or remove the old one.
- If it answers an item under "Still open", remove it from there.
- Update the master resume if it belongs there, and rebuild the current application.
- Offer to update other open applications it affects.
- A new fact goes into future resumes only when that JD asks for it.

## Format rules (ATS-safe)

Defaults. `profile/facts.md` can override any of them. The reasons are in `reference/ats-guide.md`.

- Length: at most 2 pages for the resume (or the count in the facts log), exactly 1 for the cover letter. Never pad to reach a page count; a strong 1-page resume beats a padded 2-page one.

- One column. No tables, text boxes, columns, images, icons, emoji, charts or skill bars.
- Name, email, phone, LinkedIn and city in the body at the top, not in the page header or footer.
- Standard section headings: Summary, Skills, Work Experience, Projects, Education, Certifications.
- Colour only as an accent: the headline and links in blue, everything else black. Never let colour carry meaning on its own.
- Calibri, Arial or another standard font, 10 to 12pt. A4 or US Letter to match the job's country.
- Work dates as `Mon YYYY – Mon YYYY`, the same way everywhere. Education can be year-only when months aren't known.
- Plain bullets (• or -). Separators `|` or `·`, never box-drawing characters like `│`.
- Locations include the country ("Chennai, India").
- File names, no spaces: `<First>_<Last>_<Role>_<Company>.docx` for the resume, `<First>_<Last>_<Role>_<Company>_Cover_Letter.pdf` for the cover letter.
- Submit the resume as `.docx` unless the posting asks for PDF. A PDF must be text-based (exported, not scanned).
