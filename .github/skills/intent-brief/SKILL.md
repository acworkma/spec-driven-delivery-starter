---
name: intent-brief
description: Coach a product owner through move 1 of the first-spec method, the four-box intent brief, and save it as specs/NNN-name/intent-brief.md. Use when someone wants to start a new spec, frame an epic, or prepare input for /speckit-specify.
argument-hint: "[the epic or feature in one sentence]"
---

# Intent brief (move 1)

Help the product owner write a short intent brief before any spec is generated. The brief is theirs. Your job is to ask the questions that make it precise, not to invent the answers.

## Steps

1. **Ask one question at a time, up to six,** and stop once the four boxes are clear:
   - Who has the problem, and what happens to them today?
   - What should be different afterwards, and how will we measure it?
   - What is explicitly out of scope?
   - What rules or policies apply? Where does today's process go wrong (the exception)?
   - Which systems, teams or vendors are involved, and who has to do something?
   - What don't we know yet?
2. **Write the brief.** Use the format in [the template](./intent-brief-template.md) and keep it under 450 words. Put unknowns under "Improvements and unknowns" as questions; don't guess.
3. **Save it** as `specs/NNN-short-name/intent-brief.md`, using the next free number.
4. **Draft the prompt.** Write a 6–12 line `/speckit-specify` prompt from the brief, in plain language with no technology choices, and show it to the product owner to edit.

## Rules

- If the conversation contains anything that looks like PHI or real member data, stop and ask for it to be replaced with a synthetic example.
- Don't name languages, frameworks or products. Those come later, in the plan.
