# Quickstart: Validate the P1 scenarios

**Feature**: [spec.md](./spec.md) | **Plan**: [plan.md](./plan.md) | **Date**: 2026-11-18

How a product owner, tester or engineer proves User Stories 1 and 2 (both P1) in the test environment. Synthetic data only: never use a real member's account or data, even with their permission.

## Prerequisites

- A test environment with the claim-status service, the claims system's test region and the document-service sandbox, loaded with the synthetic households below from `services/claim-status/tests/fixtures/households/`. Dates are set relative to the day the fixtures load.
- Feature flag `member-claim-status` on for synthetic test accounts only. Leave `member-claim-status-dependents` off until US3 is ready.
- A test sign-in account for each household's subscriber, from the test instance of the enterprise sign-in.
- The test harness (test builds only, never deployed to production) to make claims-system reads fail and to move the cache clock.

## Synthetic households

| Household | Members (age) | Used for |
|---|---|---|
| HH-01 | Subscriber 31 (CHP-0004401), enrolled this month, no claims | US1-AS2 |
| HH-05 | Subscriber 38; dependents aged 12 and 13, each with one sensitive-service claim | US3 age boundary (decision-table rows V02 and V06) |
| HH-06 | Subscriber 50; spouse 48, also a member but not the subscriber; dependent aged 10 | US3: only the subscriber sees dependents' claims |
| HH-07 | Subscriber 45 (CHP-0004417); dependents aged 9, 16 (one sensitive-service claim) and 19 | US1 and US2 (the subscriber's own claims); US3 |
| HH-08 | Subscriber 41; dependent aged 9 with a confidential communication request on file | US3-AS4 |

Claims for the HH-07 subscriber:

| Claim | Date of service | Set-up | Proves |
|---|---|---|---|
| CLM-2026-000183 | 20 days ago | Processed; three lines; EOB available | US1-AS1, US2-AS1 |
| CLM-2026-000184 | 3 months ago | Adjusted; versions 1 and 2 in the claims system | US1-AS5 |
| CLM-2026-000185 | 12 days ago | Waiting for information from the provider | US2-AS2 |
| CLM-2026-000186 | 6 weeks ago | Waiting for the member's other-insurance details | US2-AS2 |
| CLM-2026-000187 | 2 months ago | Denied, reason `R-AUTH`; EOB available | US2-AS3 |
| CLM-2026-000188 | 4 months ago | Processed; one of three lines denied, reason `R-NCOV` | US2-AS4 |
| CLM-2026-000189 | 5 months ago | Denied with deliberately unmapped reason `ZZ-999` | US2-AS5 |
| CLM-2026-000190 | 7 months ago | Processed; another plan paid first | Edge case: other plan paid first |
| CLM-2026-000191 | 1 day ago | Processed yesterday; EOB not generated yet | US4-AS2 (P3) |
| CLM-2024-000455 | 25 months ago | Processed | Outside the 24-month window (FR-001) |

## 1. Run the automated checks

```bash
# Service: P1 scenario tests (C# test names start with the scenario ID)
dotnet test services/claim-status --filter "FullyQualifiedName~US1_|FullyQualifiedName~US2_"

# Portal: P1 end-to-end tests in English, then Spanish (titles start with the scenario ID)
npx playwright test portal/tests/e2e/claims --grep "US1-AS|US2-AS"
CLAIMS_TEST_LANGUAGE=es npx playwright test portal/tests/e2e/claims --grep "US1-AS|US2-AS"

# Accessibility: automated WCAG 2.2 AA checks for the Claims pages
npx playwright test portal/tests/a11y/claims.a11y.spec.ts

# Spec gate
python3 tools/spec_lint.py specs/001-member-claim-status
```

Every P1 scenario ID (US1-AS1 to US1-AS5, US2-AS1 to US2-AS5) must appear in the results with a passing test.

## 2. Walk through the P1 scenarios

Sign in as the HH-07 subscriber unless the table says otherwise.

| Scenario | Do | Expect |
|---|---|---|
| US1-AS1 | Open Claims. | Claims newest first. Each shows claim number, date of service, provider, status, amount billed, plan paid and what you may owe. "Updated" shows today's date and time. CLM-2024-000455 is not listed. |
| US1-AS2 | Sign in as the HH-01 subscriber and open Claims. | A plain-language message that there are no claims yet and that claims usually appear a few weeks after a visit. |
| US1-AS3 | Open Claims. In the harness, make claims reads fail and move the cache clock forward 6 hours. Reload. | The same claims, "Updated" 6 hours ago, and a note that recent changes may be missing. |
| US1-AS4 | Keep reads failing and move the cache clock to 25 hours. Reload. | No claims. A message says claims can't be shown right now and how to get help. |
| US1-AS5 | Find CLM-2026-000184. | It appears once, labeled Adjusted, with version 2's amounts. |
| US2-AS1 | Open CLM-2026-000183. | Three lines with plain-language descriptions and amounts. No diagnosis codes or clinical notes on the page or in the network response. |
| US2-AS2 | Open CLM-2026-000185, then CLM-2026-000186. | The first says we've asked the provider and you don't need to do anything. The second asks for other-insurance details and says how to send them. |
| US2-AS3 | Open CLM-2026-000187. | The plain-language reason, how to appeal, the appeal deadline, a link to the existing appeal page and a link to the EOB. |
| US2-AS4 | Open CLM-2026-000188. | Lines 1 and 2 show Processed. Line 3 shows Denied with "Your plan doesn't cover this service." |
| US2-AS5 | Open CLM-2026-000189. | "We're reviewing this claim. Please contact us." `ZZ-999` appears nowhere on the page or in the response, and an `unmapped_code` event appears in telemetry. |

Then:

- **Spanish**: set the test account's language preference to Spanish and repeat US1-AS1, US2-AS3 and US2-AS5. Labels, reasons and next steps appear in Spanish; provider names stay as received.
- **Other plan paid first**: open CLM-2026-000190. It says "Processed by your other plan first".
- **Keyboard and screen reader**: complete US1-AS1 and US2-AS4 with the keyboard only and with a screen reader.

## 3. Record the evidence

- Attach the test report and the walkthrough results to the pull request. Gate 3 needs a passing test for every touched scenario.
- Take screenshots of synthetic data only. Never capture a real member's data, and never paste real data into prompts, issues or work items.
- In the audit store, confirm one `listViewed` or `detailViewed` event per view above, each with viewer, subject, claim numbers and time, and no clinical detail.

## Next: P2 privacy smoke test (US3)

With `member-claim-status-dependents` on for test accounts, sign in as the HH-07 subscriber and check US3-AS1 to US3-AS5 against the [visibility decision table](./data-model.md#visibility-decision-table):

- The 9-year-old's claims all show, and each view adds an audit event.
- The 16-year-old shows two claims, and no count, total or message hints at a third.
- The 19-year-old shows the adult-dependent privacy message.
- A saved link to the 16-year-old's sensitive-service claim (CLM-2026-000213) gets the same "We can't find this claim" page as a made-up claim reference.

Use HH-08 for US3-AS4, and HH-05 and HH-06 for the boundary rows.
