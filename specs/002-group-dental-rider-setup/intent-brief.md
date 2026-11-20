# Intent brief: Group dental rider setup

**Product owner**: Product owner, Product Configuration  |  **Engineering lead**: Engineering lead, Benefits Platform  |  **Date**: 2026-11-18

> Move 1 of the first-spec method. Ten minutes, product owner leads. This is the input to `/speckit-specify`.

## 1. Problem and outcome

- **Who**: employer groups, account managers, six setup teams.
- **Today**: adding a standard dental rider is slow and costly: emailed spreadsheets, handoffs, and configuration errors found as claim denials after go-live.
- **Change**: signed request to "ready to pay claims" with fewer handoffs, less waiting and less rework.
- **Out of scope**: custom benefits, pricing, member communications, vision riders.

## 2. Spec and acceptance

- **Rules and assumptions**: Catalog riders only; active group; compatible base plan; first-of-month start with enough lead time; second-person configuration check; no go-live until Fabrikam Dental Administrators (our administrator) accepts a test file and test claims pass.
- **Happy path**: **Given** active group Northwind Traders (GRP-10482), **When** a complete request with enough lead time arrives, **Then** it goes to configuration with no email.
- **Exception**: **Given** an effective date inside the lead time, **When** submitted, **Then** it takes an exception route with a recorded reason.

## 3. Handoffs and evidence

- **People**: account manager, two configuration analysts, eligibility, claims configuration, testers, underwriting, vendor manager.
- **Systems and dependencies**: rider catalog, eligibility, claims test region; Fabrikam's test-file turnaround.
- **Test data**: synthetic (RR-2026-0117, CHP-0004417).
- **Evidence**: Fabrikam's acceptance, matching test claims, and stage history showing who waited.

## 4. Improvements and unknowns

- **Catch gaps earlier**: validate at intake; test claims before go-live.
- **Open questions**: Which riders are in scope? Minimum lead time, and who approves less? Who approves configuration? Which test claims prove readiness? Mid-year: deductibles and maximums from zero, or prorated?
- **Measures to baseline** (past 12 months):
  - *Fewer handoffs*: off-system emails and spreadsheets; returns for missing information.
  - *Less waiting*: days from approval to ready to pay; days waiting on Fabrikam.
  - *Less human-intensive work*: first-time validation pass rate; mismatches found after go-live.

## Prompt for /speckit-specify

```text
Make adding a standard dental rider to an employer group's medical plan faster.
Today: emailed spreadsheets, six teams, claim denials after go-live.
Goal: signed request to "ready to pay claims" with fewer handoffs, less waiting, less rework.
Account managers pick from the approved catalog; validate at submission.
Configuration comes from the catalog; a second analyst approves it.
Before go-live, Fabrikam Dental Administrators accepts a synthetic test file and test claims match.
Show each request's stage, owner and blockers; every story needs an exception path.
Open: riders in scope, lead time, approver, readiness proof, mid-year deductibles.
Synthetic data only. Out: custom benefits, pricing, member communications.
```
