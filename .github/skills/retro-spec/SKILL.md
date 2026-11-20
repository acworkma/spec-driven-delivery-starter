---
name: retro-spec
description: Re-write an epic that was already delivered as a spec in this repository's format, and log the gaps the spec would have surfaced before build. Use for the retro-spec drill, to compare a past epic with spec-driven delivery, or to baseline how many gaps a team finds late.
argument-hint: "[path to or pasted text of the delivered epic and its stories]"
---

# Retro-spec

Help a product owner and engineer pair compare how an epic was written with how a spec would have framed it. See `retro-spec/vision-rider-2025/` for a finished example.

## Steps

1. **Ask for the epic** as it was originally written: its description, stories and acceptance criteria. If it contains anything that looks like PHI, real member data or real names, stop and ask for a sanitized copy.
2. **Draft a retro-spec** as `spec.md` in `docs/spec-conventions.md` format, with **Status**: `Retro-spec (delivered <year>)`.
   - For every question the spec forces that the original epic didn't answer, add a clarification line: `- Q: … → A: … (learned in <when>)`.
   - Ask the pair when they actually learned each answer: in refinement, in build, in UAT, in production, or never.
3. **Draft `gap-log.md`** as a table with columns `# | Gap the spec surfaces | Where it surfaced | Illustrative cost | Move that catches it`.
4. **Summarize the drill** in three lines: how many gaps, how many surfaced in UAT or later, and the one change the team would make next time.

## Rules

- The pair decides what really happened; you never invent history. Mark anything uncertain as "unknown".
