# Facilitator guide: first-spec working session

**Outcome.** Every product owner and engineer pair leaves with a first spec for one of their own epics, reviewed as a pull request. The room also leaves with a starter constitution, a list of blockers, and two measures to baseline.

**Who's in the room**
- Product owner and engineer pairs, one per team.
- One or two architects.
- A privacy or security lead.
- A QA lead.
- A sponsor, who opens and closes the session.

**Length.** About six hours, built from modular blocks.

## Roles

| Role | Job |
|---|---|
| Lead facilitator | Runs the day and drives the live build as the engineer |
| Product-owner role-player | Plays the product owner in the live build and answers the clarifying questions |
| Coaches | One for every three pairs. Coaches ask questions; they don't type. |
| Note-taker | Captures blockers, decisions and quotes for the readout and playbook |
| Sponsor | Opens with the why, closes with decisions |

## Before the day

- [ ] **Each pair's laptop:**
  - VS Code with GitHub Copilot signed in, with agent mode and skills allowed by policy;
  - a sandbox repository, either a private GitHub repo created from this template or this starter imported into Azure Repos;
  - rights to open a pull request.
- [ ] **Each pair brings two epics:** one recently delivered (for the retro-spec drill) and one upcoming. Descriptions, stories and acceptance criteria only, with no PHI.
- [ ] **Architects and security** have read `.specify/memory/constitution.md` and marked anything that isn't true for them.
- [ ] **The live build has been dry-run end to end and timed.** The answer keys are open in a second window.
- [ ] **Materials printed:** `workshop/pair-worksheet.md` and `workshop/readout-template.md`.

## Run of show

| # | Block | Length | Output |
|---|---|---|---|
| 1 | Open: the sponsor's why; rules of the day (no PHI, process first, AI drafts and people decide) | 20 min | Shared goal |
| 2 | Live build: one spec end to end (script below) | 60 min | Everyone has seen the whole loop once |
| 3 | How it runs on Monday: roles and gates, right-sizing, GitHub or Azure DevOps, measures (`docs/operating-model.md`) | 30 min | Working agreements v0 |
| 4 | Retro-spec drill on each pair's delivered epic (`workshop/retro-spec-drill.md`) | 40 min | A gap count per pair: the first baseline |
| — | Lunch | 45 min | — |
| 5 | Breakouts: a first spec on each pair's upcoming epic, moves 1–6, with checkpoints every 30 minutes. In parallel for 60 minutes, architects and security edit the constitution. | 120 min | One spec PR per pair; constitution v0.1 |
| 6 | Readout: three minutes per pair (`workshop/readout-template.md`) | 35 min | Blocker list → playbook v0.1 |
| 7 | Close: pick 3–4 pilot epics and owners, two measures, next checkpoint | 10 min | Decisions |

## Live build script (block 2, 60 minutes)

Use `specs/001-member-claim-status`. Its files are the answer key if live generation is slow.

| Minute | Do | Say |
|---|---|---|
| 0–5 | Open `intent-brief.md`. The product-owner role-player reads boxes 1 and 4 aloud. | "Ten minutes of the product owner's time, before any AI." |
| 5–12 | Run `/speckit-specify` with the prompt at the bottom of the brief. | "A draft, not a decision. Notice there's no technology in it." |
| 12–25 | Run `/speckit-clarify`. The product-owner role-player answers each question. Show where the answers land in the spec. | "These are the questions that usually surface in UAT." |
| 25–33 | Make it testable: walk through US3's exception scenarios, where hidden claims leave no trace. | "The exception is where today's process goes wrong." |
| 33–40 | Run `/speckit-checklist`, then `python tools/spec_lint.py specs/001-member-claim-status`. Delete an `(exception)` tag to show the gate fail, then restore it. | "The gate checks structure. People check meaning." |
| 40–45 | Open a pull request with the template. Show the two approvals. | "Ready means two people approved it, not that a tool finished." |
| 45–55 | Show `plan.md`, `contracts/` and `tasks.md`. Run `tools/tasks_export.py` as a dry run for both `--target github` and `--target ado`. | "Same spec, either platform." |
| 55–60 | Show a task becoming a pull request that cites FR and scenario IDs: the coding agent on GitHub, or Copilot agent mode in VS Code on Azure Repos. Mention `/speckit-converge`. | "The spec stays true because it changes in the same pull request." |

## Coaching prompts

| Move | Ask |
|---|---|
| 1. Intent | "Who is hurting today, and how would you know it got better?" |
| 2. Draft | "Is anything in this draft a technology choice?" |
| 3. Clarify | "Which of these answers would surprise someone in another team?" |
| 4. Testable | "What would a tester check? Where does this go wrong today?" |
| 5. Quality | "Which checklist item would you be uncomfortable defending?" |
| 6. Review | "Product owner: is this what you meant? Engineer: can you build it as written?" |

**Spec smells to watch for:**
- technology in the spec;
- more than five stories;
- untestable adjectives;
- privacy left implicit;
- anything that looks like real data.

If a pair is stuck for more than five minutes, record a `[NEEDS CLARIFICATION]` with an owner and move on.

## After the session (within a week)

- **Playbook v0.1.** Consolidate the blocker list, with an owner for each blocker.
- **Baselines.** Agree how the two measures will be counted on the chosen platform (`docs/measures.md`).
- **Pilot epics.** Confirm the 3–4 pilot epics and schedule their spec reviews.
- **Constitution.** Merge constitution v0.1 through a pull request.
