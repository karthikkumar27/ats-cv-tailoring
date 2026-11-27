# ATS CV Tailoring

[![test](https://github.com/karthikkumar27/ats-cv-tailoring/actions/workflows/test.yml/badge.svg)](https://github.com/karthikkumar27/ats-cv-tailoring/actions/workflows/test.yml)

An agent skill that rewrites your resume for one job description. Paste a JD and you get back an ATS-friendly 2-page `.docx`, a matching 1-page cover letter, a fit verdict, a short list of what changed, and an honest list of the requirements you don't meet.

It works with Claude Code, Claude.ai, Codex, Cursor and any agent that reads `SKILL.md` or `AGENTS.md`.

[![Watch the 77-second overview on YouTube](https://img.youtube.com/vi/cR8tZk3bBwU/maxresdefault.jpg)](https://www.youtube.com/watch?v=cR8tZk3bBwU)

*Watch the 77-second overview on YouTube.*

## Why it exists

Most AI resume tools do two things wrong. They stuff every skill you've ever touched into the Skills section, and they quietly upgrade your claims ("mentored" becomes "managed", an estimate becomes a fact). This skill is built around the opposite rules:

- **JD-only skills.** The Skills section lists only what this JD asks for and you actually have, in the JD's own wording. Everything else stays out, even when it's true.
- **No invented claims.** The agent can only use what's on your master resume or in your confirmed facts log. Anything the JD wants that you don't have is reported as a gap, never added.
- **Keywords the way ATS search works.** It pulls the exact title, tools, certifications and repeated phrases from the JD, maps each one to something you've really done, and aims for 25 to 35 matches without stuffing.
- **A facts log that remembers.** Every fact you confirm is dated, with what's OK to write and what isn't. The newest entry wins, so the agent never reuses wording you've since corrected.
- **Fit check before work.** Location limits, visa requirements, languages, seniority mismatches and duplicate applications get flagged before anything is built.
- **A cover letter with every JD, under the same rules.** Same facts, same JD focus, same layout every time, and one plain paragraph about the real gap instead of pretending it isn't there.

## Install

### Claude Code (plugin)

```
/plugin marketplace add karthikkumar27/ats-cv-tailoring
/plugin install ats-cv-tailoring@ats-cv-tailoring
```

### Claude Code (manual)

```bash
git clone https://github.com/karthikkumar27/ats-cv-tailoring ~/.claude/skills/ats-cv-tailoring
```

### Claude.ai

Zip `SKILL.md` with the `reference/`, `templates/` and `scripts/` folders, then upload the zip under Settings, Capabilities, Skills.

### Codex, Cursor and other agents

Clone the repo and open your agent in it. `AGENTS.md` points the agent at `SKILL.md`. If your agent supports skills folders, copy the repo into its skills directory instead.

## Set up your job-search folder (once)

The skill works inside one folder that holds your master CV, your facts log and every application you've made. Pick any private folder, for example `~/job-search`. Don't put it in a public repo.

```text
job-search/
  profile/
    resume_build.js     your master CV as a build script (optional, best layout control)
    resume.md           or your master CV as Markdown, .docx or .pdf
    facts.md            your confirmed facts log
  applications/
    Acme_Senior_Backend_Engineer/
      ...one folder per job, written by the skill
```

1. **Add your master CV** to `profile/`. This is the base every tailored resume starts from. Choose one:
   - **Markdown, .docx or .pdf** (`profile/resume.md`, `resume.docx` or `resume.pdf`): the easiest start. The agent builds each new resume from its content.
   - **A build script** (`profile/resume_build.js`): your CV written as code, so every resume comes out in exactly the same layout, fonts and colours. Copy [templates/resume_build.js](templates/resume_build.js), replace the example data with yours, and run `npm install docx@9` in the folder. If this file exists, the skill uses it.
2. **Start your facts log**: copy [templates/facts.md](templates/facts.md) to `profile/facts.md`. Fill in the standing rules (page limit, paper size, work authorisation) and anything true that isn't on your CV yet. You don't have to finish it: the agent asks the first-run questions and adds facts as you confirm them.
3. **Optional: earlier applications.** If you've tailored resumes before, put each one in its own `applications/<Company>_<Role>/` folder. The skill starts from the closest match.

Skip all of this and the skill does it for you: on the first run with no `profile/` folder, it asks for your current resume and sets up both files.

## From JD to tailored CV

Open your agent in the job-search folder and paste the job description, with any notes from the posting ("PDF only", "include expected salary"). The skill then works through these steps:

```text
paste JD
  -> 1. Fit check       location, work rights, languages, seniority, duplicates
                        (it stops and asks if there's a hard blocker)
  -> 2. Keywords        exact title, tools, certifications, repeated phrases,
                        each mapped to your real experience or marked a gap
  -> 3. Build           headline, summary, JD-only skills, bullets, from your
                        master CV and facts log
  -> 4. Check           scripts/ats_check.py: layout, contact, dates,
                        keywords, page count, then page images the agent
                        looks at (one-word lines, empty last page)
  -> 5. Cover letter    1 page, same facts, one honest gap paragraph
  -> 6. Save + reply    files in applications/, fit verdict, gaps, one question
```

You get:

- `applications/<Company>_<Role>/<First>_<Last>_<Role>_<Company>.docx`, the resume
- `applications/<Company>_<Role>/<First>_<Last>_<Role>_<Company>_Cover_Letter.pdf`, a 1-page cover letter in the same layout as your previous ones
- `applications/<Company>_<Role>/keywords.txt`, the JD keywords the resume matches
- `applications/<Company>_<Role>/notes.md` with the fit verdict, the exact title used, the keyword count, the choices made, the gaps, the JD text and a cover letter summary
- a short reply: fit rating, what changed, numbered gaps, and one question

**Answer the question at the end.** It's usually about the biggest gap ("have you used Kafka, even in a side project?"). When you confirm something, the agent adds it to `profile/facts.md` with the date and the exact wording you approved, and rebuilds the resume. Your facts log gets more complete with every application, so later resumes have more true material to draw from. A new fact only appears on a resume when that JD asks for it.

**Review before you send.** Open the .docx, read every line, and check you can talk about each claim in an interview. The skill keeps to your facts, but you're the one applying.

## Example

This is real output from the skill's test run on [examples/maya/](examples/maya). Maya Tan is invented: a backend engineer with 6 years of experience whose master resume lists 14 tools.

Three lines from her `profile/facts.md`:

```markdown
- **Mentoring (2026-10-02):** mentored 4 junior engineers. Never "managed" or "led a team".
- **Kubernetes (2026-10-08):** familiarity only, never production. Replaces the 2026-10-02 note.
- Don't claim: payment systems, PCI DSS, Kafka.
```

The JD is a Senior Backend Engineer, Payments role at a payments company: Python or Go, PostgreSQL query tuning, AWS Lambda/SQS/RDS, event-driven architecture (Kafka a plus), payment systems or PCI DSS, TDD, GitHub Actions, and "must be able to work in Singapore without sponsorship".

**Skills, before and after:**

```text
Before: Python, Go, TypeScript, Node.js, PostgreSQL, MySQL, Redis, AWS (Lambda,
        SQS, RDS, S3), Docker, Kubernetes, Terraform, GitHub Actions, React,
        TDD, code review, Agile

After:  Languages: Python, Go
        Databases: PostgreSQL (query tuning, indexing, query performance)
        Cloud: AWS (Lambda, SQS, RDS)
        Architecture: Event-driven architecture, backend services
        Engineering practices: Test-driven development (TDD), CI/CD with GitHub
        Actions, code review, mentoring
```

TypeScript, Node.js, MySQL, Redis, Docker, Kubernetes, Terraform, React and Agile are all true, and all left out, because this JD doesn't ask for them.

**The agent's reply (shortened):**

```text
Fit: good. No hard blockers. The JD needs work in Singapore without
sponsorship and you're logged as "Singapore Permanent Resident, no
sponsorship needed". 6 years against 5+. The big gap is payments.

What changed
- Headline and summary lead with "Senior Backend Engineer". "Payments" is
  left out of the headline because you can't claim payments work; the cover
  letter uses the full title.
- Skills cut to what the JD names.
- Northwind: 6 bullets aimed at the JD, "Tech stack" line dropped.
- Kept invoice-diff (closest thing to reconciliation work), dropped shelf-scan.
- 23 keywords matched, below the 25 to 35 target on purpose: the rest are gaps.

The 1-page cover letter PDF is next to the resume.

Gaps
1. Payment systems (authorisation, settlement). On your don't-claim list.
2. PCI DSS. On your don't-claim list.
3. Kafka (a plus). On your don't-claim list.
4. Owning PostgreSQL schemas. Not confirmed: migration and tuning are
   logged, schema design isn't.
5. Reliability work on settlement or reconciliation jobs.

On the billing migration, did you design or own the PostgreSQL schemas, or
only move and tune the data?
```

**The gap paragraph from the cover letter:**

```text
I haven't worked on payment systems or with PCI DSS, and I haven't used
Kafka. The closest I have is billing work: the invoice migration above, and
invoice-diff, an open-source Python CLI I wrote that compares invoice exports
between two databases and reports mismatches.
```

**Files saved:**

```text
applications/AcmePay_Senior_Backend_Engineer/
  Maya_Tan_Senior_Backend_Engineer_AcmePay.docx
  Maya_Tan_Senior_Backend_Engineer_AcmePay_Cover_Letter.pdf
  keywords.txt
  notes.md
  resume_build.js
```

## Try it on the example

[examples/maya/](examples/maya) has an invented candidate (`profile/resume.md`, `profile/facts.md`) and a sample JD (`jd.txt`). Copy the folder somewhere, open your agent in it, and paste the JD. It's also what the skill is tested against.

## Your data stays local

`profile/` and `applications/` are git-ignored. If you fork this repo to use as your workspace, your resume and applications never get committed. Keep it that way: a public fork with a real resume in it is a gift to recruiters' scrapers and identity thieves.

## What the agent needs

- Python 3 for the check script (standard library only; `pypdf` makes PDF page counts exact).
- Something that can write `.docx`: a docx skill, `python-docx`, the `docx` npm package or `pandoc`.
- **Optional, for an identical layout every time:** copy [templates/resume_build.js](templates/resume_build.js) to `profile/resume_build.js`, replace the example data with yours, and run `npm install docx@9`. The agent then edits only the content and runs it with `node`.
- Something that can write a PDF for the cover letter. The simplest is the included [templates/cover_letter_build.py](templates/cover_letter_build.py) with `pip install reportlab`; LibreOffice or a PDF skill also work.
- **Optional, for the visual check:** `pip install pypdfium2 pillow`. The check script then saves each page as a PNG, warns about one word alone on a line and a nearly empty last page, and an agent that can read images looks at every page.
- **Recommended:** LibreOffice, so the agent can also convert the resume to PDF and confirm both page counts. Without it the agent says the page count is unverified.

## Format rules

One column, no tables or text boxes, contact details in the body (not the header), standard headings, a standard font at 10 to 12pt, consistent `Mon YYYY – Mon YYYY` dates, `.docx` unless the posting asks for PDF. Override any of these in the Standing rules section of `profile/facts.md`. The reasons behind each rule are in [reference/ats-guide.md](reference/ats-guide.md). Full list in [SKILL.md](SKILL.md#format-rules-ats-safe).

## Files

| File | What it is |
|---|---|
| [SKILL.md](SKILL.md) | The skill: workflow, honesty rules, cover letter, format rules |
| [reference/ats-guide.md](reference/ats-guide.md) | How ATS parsing works, do's and don'ts, keyword method, pre-submission checklist |
| [scripts/ats_check.py](scripts/ats_check.py) | Checks layout, contact details, dates, keywords and page counts (`--render DIR` for page images, `--self-test` to test it) |
| [templates/facts.md](templates/facts.md) | Starting point for your facts log |
| [templates/cover-letter.md](templates/cover-letter.md) | Layout for your first cover letter |
| [templates/cover_letter_build.py](templates/cover_letter_build.py) | Matching 1-page PDF cover letter builder (invented example data, needs `reportlab`) |
| [templates/resume_build.js](templates/resume_build.js) | Optional resume builder with a fixed ATS-safe layout (invented example data) |
| [examples/maya/](examples/maya) | Invented candidate and JD for trying and testing the skill |
| [AGENTS.md](AGENTS.md) | Instructions for any agent working in this repo |
| [CLAUDE.md](CLAUDE.md) | Claude Code entry point, imports AGENTS.md |
| `.claude-plugin/` | Claude Code plugin and marketplace manifests |

## Contributing

Issues and pull requests are welcome. Read [AGENTS.md](AGENTS.md) first: it covers keeping `SKILL.md` agent-neutral and the version number in sync. Run `python tests/run_tests.py` before opening a pull request (needs `npm install --no-save docx@9` and `pip install pypdf reportlab pypdfium2 pillow`); CI runs the same tests on every push. Never include a real person's resume in an issue or PR.

## License

[MIT](LICENSE)
