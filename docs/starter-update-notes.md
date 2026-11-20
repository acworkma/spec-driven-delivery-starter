# Starter archive update - 2026-11-19

## Baseline and scope

Compared the updated `spec-driven-delivery-starter.zip` with commit `e2982d0`,
the previously imported starter on top of Spec Kit v1.4.2.

- Archive SHA-256: `1A7EF764AAFA45D052ADF8014747A25D76171D9847029DB544C98F38099C8242`.
- Of the archive's 49 files, nine changed and 40 are byte-for-byte identical.
- No starter files were added, removed, or renamed by the archive.
- This change note is an additional repository file, not part of the ZIP.

## What changed

The update removes configurable banned-term scanning and its setup
requirements. SSN-like-number scanning remains enabled by default.

| File | Change |
|---|---|
| `tools/spec_lint.py` | Removes `banned_terms()` and term matching from the repository scan. Updates the module documentation and `--no-repo-scan` help to describe the remaining SSN-like-number check. |
| `.github/workflows/spec-gate.yml` | Stops passing the `SPEC_LINT_BANNED_TERMS` secret into the gate. |
| `pipelines/spec-gate.yml` | Removes the optional banned-term variable-group guidance and environment-variable mapping. |
| `PUBLISHING.md` | Removes banned-term environment and secret setup; simplifies and renumbers the publishing smoke-test steps. |
| `README.md` | Removes the banned-term secret from the GitHub quick start. |
| `docs/guardrails.md` | Describes the gate's remaining repository-wide SSN-like-number check instead of custom term detection. |
| `docs/path-github.md` | Removes the instruction to configure the banned-term secret. |
| `docs/path-azure-devops.md` | Removes the optional banned-term variable-group setup. |
| `docs/spec-conventions.md` | Removes configurable banned terms from the automated gate criteria. |

## Operational impact

The gate no longer rejects customer names, code names, or people based on a
configured list. Setting `SPEC_LINT_BANNED_TERMS` has no effect on the updated
tool, and neither CI configuration supplies it.

This is reduced automated scan coverage, not a relaxation of the constitution:
the existing no-real-data and synthetic-example rules still apply. The gate
does not establish that content is free of all personal or sensitive data.
Human review remains necessary.

The constitution, worked specs, sample plans/tasks, Copilot instructions and
skills, Spec Kit assets, task exporter, and LICENSE did not change.
Specification structure, readiness, traceability checks, and report generation
were not changed by the archive.

## Verification

- Rehearsed extraction with Windows `tar` before applying the real overlay.
- Verified all 49 imported files against their ZIP SHA-256 hashes and
  preserved all 69 non-changing tracked files.
- Compared old and new scanners using disposable synthetic fixtures:
  the old scanner rejected a configured fictional term, the new scanner did
  not, and both rejected a synthetic SSN-shaped pattern.
- Ran `uv run --offline --no-project --python 3.14 .\tools\spec_lint.py`:
  all three example specs passed with zero errors and zero warnings.
- Ran `git diff --cached --check` with the repository's Windows line-ending
  configuration: passed.

No hosted CI execution or organization-specific data-policy approval is
claimed by these local checks.
