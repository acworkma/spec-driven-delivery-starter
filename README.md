# Spec-driven delivery starter: health plan edition

A starter kit for product owners and engineers who want to **actually do** spec-driven development (SDD) with [GitHub Spec Kit](https://github.com/github/spec-kit) and GitHub Copilot, in a regulated setting. It works whether your work lives in **GitHub** or **Azure DevOps**.

Everything here is fictional. **Contoso Health Plan** is a made-up regional health plan, and every identifier is synthetic. There is no PHI and no real data.

## What's inside

| Folder | What it gives you |
|---|---|
| `specs/` | Three worked examples. Each starts from a product owner's intent brief and ends at a spec ready for planning; the first carries on through the plan and tasks. |
| `retro-spec/` | A delivered epic, re-written as a spec, with a log of the gaps the spec would have caught early |
| `.specify/memory/constitution.md` | A starter constitution for a regulated health plan: privacy, testable acceptance, accessibility, "humans decide, AI drafts" |
| `.github/` | Copilot guidance for both GitHub and Azure DevOps users: instructions, three skills (`intent-brief`, `spec-review`, `retro-spec`) and a `spec-coach` agent. Also the GitHub spec-gate workflow, the PR template and the intent-brief issue form. |
| `.azuredevops/`, `pipelines/` | The same PR template, Copilot code review rules and spec gate for Azure Repos and Azure Pipelines |
| `tools/` | `spec_lint.py`, the spec gate (traceability, readiness, data hygiene), and `tasks_export.py`, which turns `tasks.md` into GitHub issues or Azure Boards work items |
| `docs/` | Operating model, spec conventions, the GitHub and Azure DevOps paths, measures, guardrails and Spec Kit setup |
| `workshop/` | Facilitator guide, pair worksheet, retro-spec drill and readout template for a one-day working session |

## The method on one page

Seven moves take a team from an idea to a spec both sides have approved. A first spec stops after move 6.

| # | Move | Who leads | Done when |
|---|---|---|---|
| 1 | **Frame the intent**: the four-box canvas | Product owner | The engineer can restate it |
| 2 | **Draft the spec**: `/speckit-specify` | Product owner | No tech stack in the spec |
| 3 | **Clarify together**: `/speckit-clarify` | Pair | No open clarification on P1 stories |
| 4 | **Make it testable**: Given/When/Then with IDs, one exception per story | Pair and QA | QA can name the tests |
| 5 | **Check the quality**: `/speckit-checklist` and the spec gate | Pair | Checklist passes |
| 6 | **Review it like code**: a pull request with two approvals | Pair | Approved PR means Ready |
| 7 | **Plan and slice**: `/speckit-plan`, `/speckit-tasks`, export, build | Engineer | Every PR cites FR and scenario IDs |

**Right-size first.** A small, well-understood change only needs a work item with acceptance criteria. Ambiguous, rules-heavy, cross-team or regulated work gets the full flow. Details are in [docs/operating-model.md](docs/operating-model.md).

## The worked examples

| Example | The pattern it teaches | Goes as far as |
|---|---|---|
| [001 Member claim status](specs/001-member-claim-status/) | A member-facing web feature where privacy rules for dependents are the hard part. Hidden claims must leave no trace. | Intent brief → spec → checklist → plan → contracts → tasks |
| [002 Group dental rider setup](specs/002-group-dental-rider-setup/) | A product-configuration process with many handoffs, an outside administrator and proof that benefits pay as configured | Intent brief → spec → checklist (Ready) |
| [003 Inbound document triage](specs/003-inbound-document-triage/) | An operations workflow where AI classifies and suggests, and people decide anything uncertain | Intent brief → spec → checklist (Ready) |
| [Retro-spec: vision rider (2025)](retro-spec/vision-rider-2025/) | Re-specifying an epic that was already delivered, and counting the gaps that surfaced late | Original epic → retro-spec → gap log |

## Quick start

**Everyone**
1. Read `.specify/memory/constitution.md` and one worked example. Start with `intent-brief.md`, then `spec.md`.
2. Run the spec gate: `python tools/spec_lint.py`. It needs Python 3.9+ and nothing else.

**On GitHub:** follow [docs/path-github.md](docs/path-github.md).
- Select **Use this template** and create a *private* repository for real work.
- Turn on the spec-gate workflow.

**On Azure DevOps:** follow [docs/path-azure-devops.md](docs/path-azure-devops.md).
- Import this repository into Azure Repos.
- Create the pipeline from `pipelines/spec-gate.yml`.
- Add branch policies for reviewers, linked work items and build validation.

**Your own first spec**
1. In VS Code with GitHub Copilot, run the `intent-brief` skill, or use the issue form.
2. Paste the prompt it gives you into `/speckit-specify`.
3. Work through moves 3–6.

To add Spec Kit's own commands to your repository, see [docs/spec-kit-setup.md](docs/spec-kit-setup.md). This starter is pinned to v1.4.2.

## Guardrails

- **Synthetic data only.** No PHI, member data or real names in prompts, specs, issues, work items, code or tests.
- **People approve every gate.** AI output is a draft, and agent pull requests are never auto-merged.
- **Specs are PHI-free by design,** so they can live on any approved platform. See [docs/guardrails.md](docs/guardrails.md) for platform and agreement notes, and confirm current terms with your compliance team.

## Credits and license

- **This repository:** see [LICENSE](LICENSE).
- **GitHub Spec Kit:** files generated by `specify init` come from GitHub Spec Kit under the MIT license. See [THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md).
- **Fictional names.** Contoso, Fabrikam, Northwind, Tailspin Toys and Woodgrove are fictional names commonly used in Microsoft samples.
- **Not compliance advice.** This repository is not legal or compliance advice.
