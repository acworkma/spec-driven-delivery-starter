---
name: spec-review
description: Review a feature spec against this repository's quality bar before it is marked Ready, and report findings without rewriting the spec. Use when asked to review, check or critique a spec, or before opening a spec pull request.
argument-hint: "[path to the feature folder, e.g. specs/002-group-dental-rider-setup]"
---

# Spec review

Review `spec.md` in the given feature folder, along with `checklists/requirements.md` if it exists. Report your findings and leave the edits to the authors unless they ask you to make them.

## Steps

1. **Run the spec gate:** `python tools/spec_lint.py <feature-folder> --no-repo-scan`. Include its errors in your findings.
2. **Check what the gate can't:**
   - **Testability:** can QA name a test for every scenario? Flag vague words (fast, easy, appropriate, robust).
   - **Exception paths:** is each one the case today's process gets wrong, or just a token error message?
   - **Scope:** do the Out of Scope items match the stories? Is anything implied but never specified?
   - **Privacy:** are visibility, minimum-necessary and audit rules explicit wherever member data appears?
   - **Consistency:** do the clarification answers actually appear in the requirements and scenarios?
   - **Size:** if the spec runs past about 1,800 words or has more than five stories, suggest a split.
   - **Leakage:** check for technology choices in the spec, and for anything that looks like real data.
3. **Report a table** with columns `Severity (blocker / should fix / nice to have) | Where | Finding | Suggested fix`. Then give one sentence saying whether the spec is ready for the product owner and engineering lead to approve.

## Rules

- Never mark checklist items as done, or say the spec is approved. People approve; you draft.
