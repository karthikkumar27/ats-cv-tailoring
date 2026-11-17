# CLAUDE.md

@AGENTS.md

## Claude Code notes

- When the user pastes a job description, run the `ats-cv-tailoring` skill if it's installed, otherwise read `SKILL.md` in this repo and follow it. Both are the same instructions.
- For the .docx, use the `docx` skill when it's available. Otherwise use `python-docx` or `pandoc`, whichever is installed.
- Show the finished resume as a file, not as pasted text, so the user can open it in Word.
- If the user wants their application messages to sound less machine-written, the `humanizer` skill pairs well with this one. It must never change a fact, number or claim.
