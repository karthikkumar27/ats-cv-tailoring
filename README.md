# ATS CV Tailoring

An agent skill that rewrites your resume for one job description. Paste a JD and you get back an ATS-friendly 2-page `.docx`, a matching 1-page cover letter, a fit verdict, a short list of what changed, and an honest list of the requirements you don't meet.

It works with Claude Code, Claude.ai, Codex, Cursor and any agent that reads `SKILL.md` or `AGENTS.md`.

## Why it exists

Most AI resume tools do two things wrong. They stuff every skill you've ever touched into the Skills section, and they quietly upgrade your claims ("mentored" becomes "managed", an estimate becomes a fact). This skill is built around the opposite rules:

- **JD-only skills.** The Skills section lists only what this JD asks for and you actually have, in the JD's own wording. Everything else stays out, even when it's true.
- **No invented claims.** The agent can only use what's on your master resume or in your confirmed facts log. Anything the JD wants that you don't have is reported as a gap, never added.
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

Zip `SKILL.md` and the `templates/` folder, then upload the zip under Settings, Capabilities, Skills.

### Codex, Cursor and other agents

Clone the repo and open your agent in it. `AGENTS.md` points the agent at `SKILL.md`. If your agent supports skills folders, copy the repo into its skills directory instead.

## Use

1. Open your agent in the folder where you keep your job search (or in this repo).
2. Paste a job description and ask for your resume to be rewritten for it.
3. **First run only:** the agent asks for your current resume, then sets up two files:
   - `profile/resume.md`: your master resume
   - `profile/facts.md`: your confirmed facts log, started from [templates/facts.md](templates/facts.md)

   It asks a few questions (team sizes, which numbers are estimates, tools you've only used lightly). Answer them once and every later resume follows them.
4. You get:
   - `applications/<Company>_<Role>/<First>_<Last>_<Role>_<Company>.docx`, the resume
   - `applications/<Company>_<Role>/<First>_<Last>_<Role>_<Company>_Cover_Letter.pdf`, a 1-page cover letter in the same layout as your previous ones
   - `applications/<Company>_<Role>/notes.md` with the fit verdict, the choices made, the gaps, the JD text and a cover letter summary
   - a short reply: fit rating, what changed, numbered gaps, and one question

When you confirm something new ("yes, I've used Terraform in production"), the agent adds it to your facts log so later resumes can use it, but only when a JD asks for it.

## Example

Maya Tan is an invented backend engineer with 6 years of experience. Her master resume lists Python, Go, Node.js, Docker, Kubernetes, PostgreSQL, Redis, AWS, React and Terraform.

Two lines from her `profile/facts.md`:

```markdown
- "Mentored 4 junior engineers". Never "managed", she didn't hire or run reviews.
- Kubernetes is familiarity only (one internal tool, never production).
```

She pastes this JD:

```text
Senior Backend Engineer, Payments (Singapore, hybrid)
- 5+ years building backend services in Python or Go
- Strong PostgreSQL, including query tuning
- AWS (Lambda, SQS, RDS)
- Experience with payment systems or PCI DSS
- Kafka or another event streaming platform
- Mentoring other engineers
```

**Skills section, before and after.** The master lists everything. The new version keeps only what the JD asks for and Maya has, in the JD's order and wording:

```text
Before: Python, Go, Node.js, Docker, Kubernetes, PostgreSQL, Redis, AWS, React, Terraform

After:  Languages: Python, Go
        Databases: PostgreSQL (query tuning, indexing)
        Cloud: AWS (Lambda, SQS, RDS)
```

Node.js, Docker, Redis, React and Terraform are all true, and all left out, because this JD never mentions them. Kubernetes stays out for the same reason, and it would only ever appear as familiarity.

**The agent's reply:**

```text
Fit: good. Hybrid in Singapore, and your facts log says you can work there.
No language or seniority blockers.

What changed
1. Headline is now "Senior Backend Engineer, Payments".
2. Skills cut from 10 tools to the 4 this JD names.
3. The billing migration bullet moved to the top and now leads with the
   PostgreSQL query tuning.
4. "Mentored 4 junior engineers" kept as written, not upgraded to "led".

Cover letter attached (1 page).

Gaps (not on the resume)
1. Payment systems or PCI DSS
2. Kafka or another event streaming platform

Have you worked with any event streaming, even SQS fan-out or Redis
Streams? If so, I'll add it to your facts log and cover the Kafka gap
honestly.
```

Files saved:

```text
applications/Acme_Senior-Backend-Engineer/
  Maya_Tan_Senior-Backend-Engineer_Acme.docx
  Maya_Tan_Senior-Backend-Engineer_Acme_Cover_Letter.pdf
  notes.md
```

The gap paragraph from her cover letter:

```text
I haven't worked on payment systems or under PCI DSS yet. The closest
work I've done is the billing migration at my current company, where I
moved 2 million invoices to PostgreSQL with no reconciliation errors.
```

## Your data stays local

`profile/` and `applications/` are git-ignored. If you fork this repo to use as your workspace, your resume and applications never get committed. Keep it that way: a public fork with a real resume in it is a gift to recruiters' scrapers and identity thieves.

## What the agent needs

- Something that can write `.docx`: a docx skill, `python-docx`, the `docx` npm package or `pandoc`.
- Something that can write a PDF for the cover letter: LibreOffice (`soffice --headless --convert-to pdf`), a PDF skill, or a library such as `reportlab`.
- **Recommended:** LibreOffice, so the agent can also convert the resume to PDF and confirm both page counts. Without it the agent says the page count is unverified.

## Format rules

One column, no tables or text boxes, contact details in the body (not the header), standard headings, a system font at 10 to 11pt, consistent `Mon YYYY – Mon YYYY` dates, `.docx` unless the posting asks for PDF. Override any of these in the Preferences section of `profile/facts.md`. Full list in [SKILL.md](SKILL.md#format-rules-ats-safe).

## Files

| File | What it is |
|---|---|
| [SKILL.md](SKILL.md) | The skill: workflow, honesty rules, cover letter, format rules |
| [templates/facts.md](templates/facts.md) | Starting point for your facts log |
| [AGENTS.md](AGENTS.md) | Instructions for any agent working in this repo |
| [CLAUDE.md](CLAUDE.md) | Claude Code entry point, imports AGENTS.md |
| `.claude-plugin/` | Claude Code plugin and marketplace manifests |

## Contributing

Issues and pull requests are welcome. Read [AGENTS.md](AGENTS.md) first: it covers keeping `SKILL.md` agent-neutral and the version number in sync. Never include a real person's resume in an issue or PR.

## License

[MIT](LICENSE)
