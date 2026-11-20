# Operating model: how a spec moves from idea to production

## Who does what

| Role | Owns | Approves |
|---|---|---|
| Product owner | The what and why: problem, outcomes, rules, acceptance scenarios, scope | Spec Ready (gate 1), release (gate 4) |
| Engineering lead | Feasibility, the plan, task breakdown, quality of the build | Spec Ready (gate 1), plan (gate 2) |
| Engineers | Implementation and tests named after scenarios | Code review (gate 3), never their own pull request |
| QA | Testability of every scenario; evidence | Joins gate 1 when a scenario can't be tested |
| Privacy and security | Visibility rules, minimum necessary, audit, threat model | Any spec or plan that touches member data |
| Architecture | Constitution, reference patterns, exceptions | Plans that introduce a new pattern |
| AI assistants and agents | Drafts: specs, clarifying questions, plans, tasks, code, review comments | Nothing. They never approve. |

## The four gates

| Gate | Passes when |
|---|---|
| 1. Spec Ready | No open clarifications on P1 stories; quality checklist complete; spec gate passes; the product owner and engineering lead approve the pull request |
| 2. Plan approved | The plan's Constitution Check passes; contracts and data model reviewed; tasks exported to issues or work items |
| 3. Merge | Tests for every touched scenario pass; spec gate passes; reviewed by someone other than the author or agent |
| 4. Release | Feature flag and rollback plan ready; telemetry for each success criterion is live |

## Right-size before you start

Answer three questions:

1. Do the product owner and engineer disagree, or are they unsure, about any rule or outcome?
2. Does it touch member data, money, a regulatory rule or another team's system?
3. Would a mistake surface only after release, in claims, complaints or audits?

**If all three answers are no**, a work item or issue with acceptance criteria is the spec. **If any answer is yes**, use the full flow below.

## The seven moves to a first spec

| # | Move | Who leads | How | Done when |
|---|---|---|---|---|
| 1 | Frame the intent | Product owner | Four-box intent brief (`intent-brief` skill or issue form) | The engineer can restate it |
| 2 | Draft the spec | Product owner drives | `/speckit-specify` with the brief | No tech stack in the spec |
| 3 | Clarify together | Pair | `/speckit-clarify` (up to 5 questions); answers go into the spec | No open clarification on P1 stories |
| 4 | Make it testable | Pair and QA | Given/When/Then with scenario IDs; one exception per story; the constitution's NFRs | QA can name the tests |
| 5 | Check the quality | Pair | `/speckit-checklist`, `spec-review` skill, spec gate | Checklist passes or gaps are logged |
| 6 | Review it like code | Pair | Pull request; two approvals | Approved PR means Ready |
| 7 | Plan and slice | Engineer | `/speckit-plan`, `/speckit-tasks`, `/speckit-analyze`, export tasks, `/speckit-implement` one phase at a time, `/speckit-converge` | Every PR cites FR and scenario IDs |

A first spec stops after move 6. Moves 1 to 6 take about 80 minutes for a well-chosen epic.

## When reality changes the spec

- **Flow-forward.** If a build discovery changes behavior, update `spec.md` in the same pull request and add a clarification line saying what was learned.
- **Converge after each phase.** Run `/speckit-converge` to find drift between the spec, the plan and the code. It can only add tasks; it never rewrites the spec.
- **Archive, don't delete.** The spec on `main` describes what is in production or about to be.

## Anti-patterns

- **The spec as a handoff document.** The product owner writes it alone and throws it over the wall. Moves 3 to 6 are done together.
- **Thirty-page specs.** Past roughly 1,800 words or five stories, split the feature.
- **Technology in the spec.** "Use a queue" belongs in the plan.
- **Skipping clarify.** It is the cheapest gap-finder in the whole flow.
- **Rubber-stamping AI output.** An approval means you read it.
- **Measuring lines of AI-generated code.** See `docs/measures.md` instead.
