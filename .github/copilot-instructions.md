# Copilot instructions for this repository

This repository practices spec-driven development with GitHub Spec Kit. The specs in `specs/` are the source of truth for what the software must do. Code, tests and work items trace back to them.

## Always

- **Follow the constitution.** Treat `.specify/memory/constitution.md` as non-negotiable. If a request conflicts with it, say so and stop.
- **No PHI or real data.** Never put protected health information, member data, real names or real identifiers into prompts, specs, issues, work items, code, tests or commit messages. Use the synthetic identifiers shown in `docs/spec-conventions.md`.
- **Keep `spec.md` technology-agnostic.** Languages, frameworks, databases and cloud services belong in `plan.md`.
- **Use the ID conventions in `docs/spec-conventions.md`:**
  - User stories: `### User Story N - Title (Priority: Pn)`
  - Scenarios: `[USn-ASm]`, with `(exception)` on exception paths
  - Requirements and success criteria: `FR-###`, `SC-###`
  - Tasks: `T###`
- **Right-size the work.** A small, well-understood change needs only an issue or work item with acceptance criteria. Ambiguous, rules-heavy, cross-team or regulated work gets the full flow.
- **Change the spec with the behavior (flow-forward).** If a change alters behavior, update `spec.md` in the same change, and say which FR or scenario changed.

## When you implement

- Cite the FR, scenario and task IDs in commit messages and pull request descriptions, for example `T014: claim list empty state (FR-003, US1-AS2)`.
- Name tests after the scenarios they prove, for example `US1_AS2_new_member_sees_empty_state`.
- Implement one phase of `tasks.md` at a time, and stop at each checkpoint for a person to review.

## Your output is a draft

- Product owners approve the what and why. Engineers approve feasibility, design and code. Never state or imply that a person has approved something.
- Before finishing any change under `specs/`, run `python tools/spec_lint.py specs/<feature>` and fix every error.
