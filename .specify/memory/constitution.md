# Contoso Health Plan Delivery Constitution

> **Starter constitution for a regulated health plan.** Every rule here should already be true in your organization; delete or replace anything that isn't before you ratify it. Contoso Health Plan is a fictional company.

## Core Principles

### I. Member privacy first (NON-NEGOTIABLE)

- **No real personal data in the delivery system.** No protected health information (PHI), member data or other real personal data goes into prompts, specs, issues, work items, commits, test fixtures or screenshots. Use synthetic data only.
- **Minimum necessary.** Features that touch member data show and store only what the user's task needs.
- **Audit everything.** Every view, export or change of member data, by a person or a system, is audit-logged.
- **Privacy questions are settled before Ready.** They are resolved with the Privacy Office before a spec is marked Ready, and the answer is recorded in the spec's Clarifications.

### II. Specs before code

- **Specs for the hard changes.** Ambiguous, rules-heavy, cross-team or regulated changes start from a spec in `specs/`. A small, well-understood change may use an issue or work item with acceptance criteria instead.
- **What and why, never how.** The spec has no languages, frameworks, databases or cloud services; those belong in the plan.
- **Two approvals, in the pull request.** The product owner approves the what and why; engineering approves feasibility.
- **Flow-forward.** When behavior changes, the spec changes in the same pull request, so the spec on `main` always describes what is in production or about to be.

### III. Testable acceptance

- **Scenario IDs and exception paths.** Every user story has Given/When/Then acceptance scenarios with IDs (`US1-AS1`), including at least one exception path.
- **Evidence before done.** Tests are named after the scenarios they prove. A story is not done until every scenario has passing evidence.
- **Measurable success.** Success criteria are measurable and technology-agnostic, with a baseline where one exists.

### IV. Accessible, plain-language member experiences

- **Accessibility.** Member-facing experiences meet WCAG 2.2 AA.
- **Plain language.** Member-facing text is written in plain language and tells the member what happens next.
- **Settled in the spec.** Language-access and alternate-format needs are confirmed in the spec, not discovered in testing.

### V. Secure and observable by default

- **Least privilege.** People, services and agents get least-privilege access. Secrets never live in the repository.
- **Approved interfaces only.** Integrations with systems of record use approved, versioned interfaces, never direct database access.
- **Clean, measurable telemetry.** Logs and telemetry carry no PHI, and every success criterion can be measured in production.

### VI. Small, reversible changes

- **Thin slices.** Deliver in independently testable slices, highest priority first.
- **Reversible releases.** Member-facing changes ship behind a feature flag with a rollback plan.

### VII. Humans decide, AI drafts

- **Drafts until approved.** AI-generated specs, plans, tasks and code are drafts until a named person approves them at a gate.
- **No auto-merge for agents.** Coding agents work on branches with least-privilege tokens, and their pull requests are never auto-merged.
- **Read-only by default.** Tools that can write to work tracking or source control run read-only unless a person turns writing on.

## Regulatory and Data Constraints

- **HIPAA.** HIPAA Privacy and Security Rule obligations apply to anything that stores, displays or transmits PHI.
- **Sensitive services and dependents.** State privacy rules for sensitive services and for dependents can override what a subscriber may see by default. The Privacy Office owns the interpretation.
- **BAA coverage.** Only platforms covered by the organization's business associate agreements may hold PHI. Planning and specification tools that are not covered stay PHI-free.
- **Records retention.** Retention follows the records-retention schedule. Specs never set retention periods without Records Management.

## Delivery Workflow and Quality Gates

| Gate | Passes when | Approved by |
|---|---|---|
| 1. Spec Ready | No open clarifications on P1 stories; quality checklist complete; spec gate passes | Product owner and engineering lead |
| 2. Plan approved | Constitution Check passes; contracts and data model reviewed | Tech lead (plus architecture for new patterns) |
| 3. Merge | Code review complete; tests for every touched scenario pass; spec gate passes; no PHI | A reviewer who is neither the author nor the agent |
| 4. Release | Feature flag and rollback plan in place; success-criteria telemetry live | Product owner and operations |

## Governance

- **Precedence.** This constitution overrides local conventions. Exceptions are recorded in the plan's Complexity Tracking table, with a reason and an owner.
- **Amendments.** Amendments are made by pull request and approved by the architecture and security leads. Versions follow semantic versioning.
- **Reviews.** Review the constitution every quarter and after any privacy or security incident.

**Version**: 0.1.0 | **Ratified**: 2026-11-18 | **Last Amended**: 2026-11-18
