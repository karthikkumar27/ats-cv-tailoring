# ATS CV Tailoring

An agent skill that rewrites your resume for one job description. Paste a JD and you get back an ATS-friendly 2-page `.docx`, a fit verdict, a short list of what changed, and an honest list of the requirements you don't meet.

It works with Claude Code, Claude.ai, Codex, Cursor and any agent that reads `SKILL.md` or `AGENTS.md`.

## Why it exists

Most AI resume tools do two things wrong. They stuff every skill you've ever touched into the Skills section, and they quietly upgrade your claims ("mentored" becomes "managed", an estimate becomes a fact). This skill is built around the opposite rules:

- **JD-only skills.** The Skills section lists only what this JD asks for and you actually have, in the JD's own wording. Everything else stays out, even when it's true.
- **No invented claims.** The agent can only use what's on your master resume or in your confirmed facts log. Anything the JD wants that you don't have is reported as a gap, never added.
- **Fit check before work.** Location limits, visa requirements, languages, seniority mismatches and duplicate applications get flagged before anything is built.

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
   - `applications/<Company>_<Role>/<First>_<Last>_<Role>_<Company>.docx`
   - `applications/<Company>_<Role>/notes.md` with the fit verdict, the choices made, the gaps and the JD text
   - a short reply: fit rating, what changed, numbered gaps, and one question

When you confirm something new ("yes, I've used Terraform in production"), the agent adds it to your facts log so later resumes can use it, but only when a JD asks for it.

## Your data stays local

`profile/` and `applications/` are git-ignored. If you fork this repo to use as your workspace, your resume and applications never get committed. Keep it that way: a public fork with a real resume in it is a gift to recruiters' scrapers and identity thieves.

## What the agent needs

- Something that can write `.docx`: a docx skill, `python-docx`, the `docx` npm package or `pandoc`.
- **Optional:** LibreOffice (`soffice`), so the agent can convert to PDF and confirm the page count. Without it the agent says the page count is unverified.

## Format rules

One column, no tables or text boxes, contact details in the body (not the header), standard headings, a system font at 10 to 11pt, consistent `Mon YYYY – Mon YYYY` dates, `.docx` unless the posting asks for PDF. Override any of these in the Preferences section of `profile/facts.md`. Full list in [SKILL.md](SKILL.md#format-rules-ats-safe).

## Files

| File | What it is |
|---|---|
| [SKILL.md](SKILL.md) | The skill: workflow, honesty rules, format rules |
| [templates/facts.md](templates/facts.md) | Starting point for your facts log |
| [AGENTS.md](AGENTS.md) | Instructions for any agent working in this repo |
| [CLAUDE.md](CLAUDE.md) | Claude Code entry point, imports AGENTS.md |
| `.claude-plugin/` | Claude Code plugin and marketplace manifests |

## Contributing

Issues and pull requests are welcome. Read [AGENTS.md](AGENTS.md) first: it covers keeping `SKILL.md` agent-neutral and the version number in sync. Never include a real person's resume in an issue or PR.

## License

[MIT](LICENSE)
