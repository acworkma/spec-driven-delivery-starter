# Gap log: Vision rider (2025)

The gaps the [retro-spec](spec.md) surfaces in the [original epic](original-epic.md), with where the spec now covers each one. Weeks count from the start of the 2025 project: build ran in weeks 1–8, UAT in weeks 9–11, and the first groups went live in week 12. **Every cost is illustrative**, not real data.

| # | Gap the spec surfaces | Where it surfaced in 2025 | Illustrative cost | Move that catches it |
|---|---|---|---|---|
| 1 | No named approver: "Configuration is reviewed" never says by whom (FR-004, US2-AS2) | Build, week 6: a package reached testing with the wrong frames allowance | 3 days of rework (illustrative) | Quality checklist |
| 2 | Fabrikam's eligibility file layout had no code for the new rider (Assumptions) | Build, week 7: Fabrikam's change window held up file testing | 10 days of waiting and 2 days of rework (illustrative) | Plan |
| 3 | Dependents: covered when the group covers them on medical, with the same age limit (FR-006, US3-AS1) | UAT, week 9: dependents were missing from the eligibility file | 4 days of rework (illustrative) | Quality checklist |
| 4 | New-hire waiting period: the rider starts when medical coverage starts (FR-006, US5-AS2) | UAT, week 10: new hires showed as covered before their medical started | 3 days of rework (illustrative) | Clarify |
| 5 | Lead time: the first of a month, at least 30 days after approval (FR-002, US1-AS2) | Production, week 12: a group's rider started 12 days after its request, before setup was done | 6 days of rework and one group's claims reprocessed (illustrative) | Clarify |
| 6 | Administrator readiness: Fabrikam accepts a test file before go-live (FR-007, FR-009, US3-AS1, US3-AS2) | Production, week 12: Fabrikam rejected the first live file, and providers could not find members for 4 days | 8 days of rework and about 60 member calls (illustrative) | Make it testable |
| 7 | Group terminates before go-live: cancel and tell Fabrikam (FR-010, US5-AS3) | Production, week 14: a terminated group stayed on Fabrikam's file | 3 days of rework (illustrative) | Make it testable |
| 8 | Mid-year additions: allowances and frequency limits start fresh, with no proration (FR-005, US2-AS3) | Production, week 15: July starters got half allowances, and their claims were adjusted | 5 days of rework and about 40 claims adjusted (illustrative) | Clarify |

**Summary**

- 8 gaps; 6 surfaced in UAT or production and 2 during build.
- About 34 days of rework plus 10 days of waiting (illustrative).
- Next time we would clarify and write exception scenarios before build: those two moves catch 5 of the 8 (Clarify 3, Make it testable 2, Quality checklist 2, Plan 1).
