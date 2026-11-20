# Spec conventions

These conventions sit on top of GitHub Spec Kit's templates. They make every requirement traceable to a test, and they let `tools/spec_lint.py` check a spec before it merges.

## Folder layout

```text
specs/NNN-short-name/
├── intent-brief.md              # Move 1: the four-box canvas (product owner)
├── spec.md                      # Moves 2–5: /speckit-specify, /speckit-clarify, made testable
├── checklists/requirements.md   # Move 5: specification quality checklist
├── plan.md, research.md, data-model.md, quickstart.md, contracts/   # Move 7: /speckit-plan
└── tasks.md                     # Move 7: /speckit-tasks
```

A first spec stops at `checklists/requirements.md`. Plan and tasks come when the team is ready to build.

## Spec header

```markdown
# Feature Specification: <Feature name>

**Feature Branch**: `NNN-short-name`
**Created**: YYYY-MM-DD
**Status**: Draft | Ready for planning | In build | Delivered
**Input**: User description: "<the intent brief, condensed>"
```

## Section order

1. Header (above)
2. `## Clarifications` with `### Session YYYY-MM-DD` and one `- Q: … → A: …` line per answered question
3. `## User Scenarios & Testing *(mandatory)*`: user stories, then `### Edge Cases`
4. `## Requirements *(mandatory)*`: `### Functional Requirements`, then `### Key Entities` when data is involved
5. `## Success Criteria *(mandatory)*`: `### Measurable Outcomes`
6. `## Assumptions`
7. `## Out of Scope`

## IDs

| Thing | Format | Example |
|---|---|---|
| User story | `### User Story N - Title (Priority: Pn)` | `### User Story 1 - See my recent claims (Priority: P1)` |
| Acceptance scenario | `N. [USn-ASm] **Given** …, **When** …, **Then** …` (one line) | `1. [US1-AS1] **Given** a member with three claims, **When** …, **Then** …` |
| Exception scenario | Add `(exception)` after the ID | `3. [US1-AS3] (exception) **Given** …` |
| Functional requirement | `- **FR-###**: System MUST …` | `- **FR-004**: System MUST NOT show …` |
| Success criterion | `- **SC-###**: …` | `- **SC-002**: …` |
| Task | `- [ ] T### [P] [USn] … (FR-###, USn-ASm)` | `- [ ] T014 [US1] … (FR-001, US1-AS2)` |

## Rules the spec gate checks

1. Every user story has at least two acceptance scenarios with IDs, and at least one is marked `(exception)`.
2. Scenario IDs are unique and match their story number.
3. FR and SC IDs are unique. A spec has at least one of each.
4. A spec whose Status is **Ready for planning** or **In build** has:
   - no `[NEEDS CLARIFICATION` markers;
   - a `## Clarifications` section with at least one `- Q: … → A: …` line;
   - every item in `checklists/requirements.md` checked.
5. When `tasks.md` exists:
   - task IDs are unique;
   - story tags and scenario IDs exist in the spec;
   - every FR is referenced by at least one task.
6. No SSN-like numbers anywhere, and none of the terms in the `SPEC_LINT_BANNED_TERMS` secret.

The gate also warns about these, without failing:
- tech-stack words in `spec.md`;
- acceptance scenarios that no task references.

## Writing rules

- **What and why, never how.** No languages, frameworks, databases or cloud services in `spec.md`; those belong in `plan.md`.
- **Plain language.** A product owner who has never used Spec Kit must be able to read and approve the spec.
- **Right-size it.** Aim for 1,000–1,800 words. A first spec that runs longer is usually two features.
- **Every story earns its exception path.** Name the case the current process gets wrong.
- **Fictional and synthetic only.** Use Contoso Health Plan and other fictional companies. Use synthetic identifiers such as member ID `CHP-0004417` and claim number `CLM-2026-000183`. Never use real people, customers, members, providers or data.
