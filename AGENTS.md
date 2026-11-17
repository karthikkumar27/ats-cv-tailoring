# AGENTS.md

Instructions for any coding agent (Codex, Cursor, Gemini CLI, OpenCode, Claude Code and others) working in this repo.

This repo is two things at once:

1. **A workspace.** Someone clones it, opens an agent in it, and pastes a job description. You rewrite their resume for that job.
2. **The source of a portable agent skill.** `SKILL.md` is the skill. People also install it on its own.

## When the user pastes a job description

Read `SKILL.md` and follow it step by step. It's the source of truth for the workflow, the honesty rules and the format rules. Don't work from memory of an earlier version.

- Their data lives in `profile/` (master resume and confirmed facts log) and `applications/` (one folder per job). Both are git-ignored. Never commit them, never move them out of those folders, and never paste their contents into issues, commits or web requests.
- If `profile/` doesn't exist, it's their first run: follow the "First run" section of `SKILL.md`. Templates are in `templates/`.
- Ask before building when the fit check finds a hard blocker.
- Claim nothing that isn't in `profile/`. This is the one rule that matters more than any keyword score.

## When the user asks you to change the skill

- `SKILL.md` is the only skill file. Keep it agent-neutral: no tool names that only one agent has, no absolute paths, no sandbox paths like `/mnt/...`.
- Keep `README.md` in sync with `SKILL.md` (steps, rules, file layout).
- Keep one version number in three places: `metadata.version` in `SKILL.md`, `.claude-plugin/plugin.json`, and the newest heading in `CHANGELOG.md`.
- The plugin manifests reuse the first sentence of the `SKILL.md` description. Change them together.
- Never put a real person's resume, facts or job applications in the repo. Examples use invented people.

## Layout

```
SKILL.md                    the skill (workflow, honesty rules, format rules)
templates/facts.md          starting point for a user's facts log
templates/cover-letter.md   layout for a user's first cover letter
.claude-plugin/             Claude Code plugin and marketplace manifests
AGENTS.md                   this file
CLAUDE.md                   Claude Code entry point, imports this file
README.md                   install and use
CHANGELOG.md                release notes, newest first
profile/                    user data, git-ignored, created on first run
applications/               user output, git-ignored
```
