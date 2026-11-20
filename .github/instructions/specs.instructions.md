---
applyTo: "specs/**"
---

# Writing and editing specs

- **Format.** Follow `docs/spec-conventions.md`: GitHub Spec Kit's spec template, plus scenario IDs and exception paths.
- **Every story has an exception.** Each user story needs at least two acceptance scenarios, one line each, in Given/When/Then form. At least one is marked `(exception)`, and it should be the case today's process gets wrong.
- **Requirements must be testable.** Functional requirements say MUST or MUST NOT. Replace vague words like fast, easy, robust or intuitive with numbers or observable behavior.
- **Success criteria must be measurable** and technology-agnostic. Name the baseline when one exists.
- **Mark unknowns honestly.** Use `[NEEDS CLARIFICATION: question]` rather than guessing. When a question is answered, record it under `## Clarifications` as `- Q: … → A: …` and update the affected requirements and scenarios.
- **Settle privacy before Ready.** Privacy, visibility and audit rules must be explicit before a spec is marked Ready for planning.
- **Keep it reviewable.** Aim for 1,000–1,800 words. If a spec grows past that, propose splitting it.
- **Synthetic examples only.** Use synthetic identifiers and the fictional company names already in use. Never add real people, members, providers or customers.
