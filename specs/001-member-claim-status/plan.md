# Implementation Plan: Member claim status

**Branch**: `001-member-claim-status` | **Date**: 2026-11-18 | **Spec**: [spec.md](./spec.md)  
**Input**: Feature specification from `specs/001-member-claim-status/spec.md`

> Move 7 of the first-spec method. `/speckit-plan` drafted this plan from the spec and the constitution; it stays a draft until the tech lead approves it at Gate 2, with architecture reviewing the new service and cache. The technology named here is this example's assumption. Replace it with your team's standards.

## Summary

Signed-in members get a Claims area in the existing member portal: claims from the last 24 months with plain-language status (US1, P1), claim details with service lines, denial reasons and next steps (US2, P1), dependents' claims within the Privacy Office's rules (US3, P2), and Explanation of Benefits (EOB) downloads (US4, P3).

A new, read-only claim-status service sits between the portal and the systems of record. It reads the claims system only through its approved, versioned read interface, gets EOB links from the document service, and keeps member-facing claim views in a read-through cache with a 24-hour maximum age. Internal codes become member-facing text through a mapping that Claims Operations owns as data. One server-side policy component decides what a subscriber may see before any response is built, so hidden claims leave no trace. No new system of record. [research.md](./research.md) records the four decisions behind this design.

## Technical Context

**Language/Version**: Team standard; this example assumes TypeScript for the portal front end and C# (.NET) for a claim-status service; replace with yours.  
**Primary Dependencies**: Existing member portal and Contoso design system (components, Spanish support, accessibility patterns); existing enterprise sign-in (the service validates members' tokens); the claims system's approved read interface (versioned; claims, service lines, status and reason codes, the sensitive-service marking, plus the member and household records that carry coverage dates, relationship, date of birth and confidential communication requests); the document service that stores EOBs (issues short-lived links); the existing enterprise audit store; the existing feature-flag service.  
**Storage**: No new system of record. A read-through cache of member-facing claim views with a 24-hour maximum age (team-standard distributed cache, encrypted at rest, on a platform covered by Contoso's business associate agreements). Status mapping and reason text live in a versioned data file owned by Claims Operations.  
**Testing**: Team standard; this example assumes xUnit for the service, Vitest for portal units, Playwright for end-to-end tests with axe-core accessibility checks, and contract checks that validate every API test response against [contracts/claim-status-api.yaml](./contracts/claim-status-api.yaml). Tests are named after the scenario they prove: `US3_AS2_sensitive_claim_of_16_year_old_leaves_no_trace` in C#, `US3-AS2 ...` as an end-to-end test title. Fixtures are synthetic households only.  
**Target Platform**: Existing member portal (responsive web, current major browsers on phone and desktop). The service runs on the team's standard container hosting in a covered environment, behind the portal's existing gateway.  
**Project Type**: Web application: a feature in the existing portal front end plus one new back-end service.  
**Performance Goals**: Claims list p95 under 2 seconds; claim detail p95 under 1.5 seconds; EOB link issued p95 under 1 second; 50 requests per second at peak (Monday mornings and the weeks after open enrollment).  
**Constraints**: Claim information never more than 24 hours behind the claims system; hidden, unknown and malformed claim references all return the same `404`; no PHI in logs, telemetry or URLs (paths use opaque references, never member IDs or claim numbers); responses carry `Cache-Control: no-store`; WCAG 2.2 AA; English and Spanish text; ships behind feature flags with a rollback plan; the claims system's read interface is rate-limited (assumed 200 requests per second shared across consumers).  
**Scale/Scope**: About 400,000 members, about 180,000 registered for the portal; up to 500 claims per member in the 24-month window; 2 portal pages, 4 components, 4 read-only API operations.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.* Result: **pass**, re-checked after Phase 1 design on 2026-11-18.

| Principle | How this plan satisfies it | Result |
|---|---|---|
| I. Member privacy first | Synthetic households only, in fixtures, docs and screenshots. HIPAA minimum necessary: the service never requests diagnosis codes or clinical notes, the cache holds member-facing views only, and closed response schemas stop anything else leaving. Dependent visibility follows Clarification 3 (Privacy Office, 2026-11-18) and is decided in one server-side component that fails closed. Every list, detail and EOB request writes an audit event to the existing audit store. | Pass |
| II. Specs before code | The spec is Ready for planning with five recorded clarifications. The contract, data model and every task trace to FR and scenario IDs. Behavior changes update `spec.md` in the same pull request. | Pass |
| III. Testable acceptance | Each story phase starts with tests named after its scenario IDs; every acceptance scenario has at least one test task. Every success criterion has a PHI-free measure in production; SC-001's baseline is the 90 days of Member Services call-reason data before launch. | Pass |
| IV. Accessible, plain-language member experiences | Design-system components, automated axe-core checks in CI and a manual WCAG 2.2 AA audit before launch (SC-005). Status, reason and next-step text comes from Claims Operations in English and Spanish, reviewed by Language Services. EOB alternate formats and languages use Contoso's existing request process. | Pass |
| V. Secure and observable by default | Claims data comes only through the claims system's approved, versioned read interface. The service has a least-privilege, read-only identity; secrets stay in the team's vault. Logs and telemetry carry opaque references, counts and timings only. Telemetry measures SC-001 to SC-006 in production. | Pass |
| VI. Small, reversible changes | Four slices in priority order, each independently testable. Flag `member-claim-status` covers US1, US2 and US4; `member-claim-status-dependents` covers US3 so it can launch, or roll back, on its own. Rollback is turning a flag off: no data migration, and cached views expire within 24 hours. | Pass |
| VII. Humans decide, AI drafts | This plan and `tasks.md` are drafts until the tech lead approves them at Gate 2. Agent pull requests are never auto-merged. CODEOWNERS makes the Privacy Office a required reviewer for the visibility policy and Claims Operations for the status mapping. | Pass |

**Regulatory and data constraints**: PHI stays on platforms covered by Contoso's business associate agreements (service, cache, audit store). Audit records follow the records-retention schedule; this plan sets no retention period. The cache's 24-hour limit is a freshness limit, not a retention period.

## Project Structure

### Documentation (this feature)

```text
specs/001-member-claim-status/
├── intent-brief.md              # Move 1: four-box canvas (product owner)
├── spec.md                      # Moves 2–5: /speckit-specify, /speckit-clarify
├── checklists/
│   └── requirements.md          # Move 5: specification quality checklist
├── plan.md                      # This file (/speckit-plan)
├── research.md                  # Phase 0: decisions
├── data-model.md                # Phase 1: entities, status mapping, visibility decision table
├── quickstart.md                # Phase 1: validate the P1 scenarios with synthetic households
├── contracts/
│   └── claim-status-api.yaml    # Phase 1: OpenAPI 3.1 contract
└── tasks.md                     # Phase 2 (/speckit-tasks)
```

### Source Code (repository root)

```text
portal/                                          # existing member portal (TypeScript)
├── src/
│   ├── config/feature-flags.ts                  # member-claim-status, member-claim-status-dependents
│   └── features/claims/
│       ├── api/claim-status-client.ts           # generated from contracts/claim-status-api.yaml
│       ├── pages/
│       │   ├── ClaimsListPage.tsx
│       │   └── ClaimDetailPage.tsx
│       ├── components/
│       │   ├── MemberSelector.tsx               # self and dependents; same privacy note for every dependent
│       │   ├── FreshnessNotice.tsx              # "Updated" time, delayed and unavailable messages
│       │   ├── ServiceLinesTable.tsx
│       │   └── EobDownload.tsx
│       ├── session/claims-session.ts            # clears claim data on timeout; returns to the same page
│       └── content/
│           ├── claims.en.json                   # page text; status and reason text come from the service
│           └── claims.es.json
└── tests/
    ├── e2e/claims/                              # Playwright; titles start with the scenario ID
    │   ├── claims-list.spec.ts
    │   ├── claim-detail.spec.ts
    │   ├── dependents.spec.ts
    │   ├── eob.spec.ts
    │   └── session-timeout.spec.ts
    └── a11y/claims.a11y.spec.ts                 # axe-core, WCAG 2.2 AA rules

services/claim-status/                           # new read-only service (C#/.NET); no system of record
├── src/
│   ├── ClaimStatus.Api/
│   │   ├── Program.cs
│   │   ├── appsettings.json                     # flags, cache limits; no secrets
│   │   ├── Auth/MemberContext.cs                # sign-in token; opaque memberRef and claimId
│   │   ├── Endpoints/
│   │   │   ├── HouseholdEndpoints.cs
│   │   │   ├── ClaimsEndpoints.cs
│   │   │   └── EobEndpoints.cs
│   │   ├── Errors/ProblemResponses.cs           # one 404 for hidden, unknown and malformed references
│   │   └── Telemetry/ClaimStatusMetrics.cs      # counts and timings only
│   ├── ClaimStatus.Core/
│   │   ├── Claims/ClaimViewBuilder.cs
│   │   ├── Status/StatusMappingLoader.cs
│   │   ├── Status/StatusMapper.cs
│   │   ├── Visibility/VisibilityPolicy.cs       # the only place visibility is decided
│   │   └── Audit/AuditEvent.cs
│   └── ClaimStatus.Infrastructure/
│       ├── ClaimsSystem/ClaimsReadClient.cs     # approved, versioned read interface
│       ├── Cache/ClaimViewCache.cs              # read-through; 24-hour maximum age
│       ├── Documents/EobLinkClient.cs           # short-lived EOB links
│       └── Audit/AuditStoreWriter.cs            # existing enterprise audit store
├── config/status-mapping.json                   # owned by Claims Operations
└── tests/
    ├── ClaimStatus.Core.Tests/                  # xUnit; method names start with the scenario ID
    │   ├── Claims/
    │   ├── Freshness/
    │   ├── Status/
    │   ├── Visibility/                          # one test per decision-table row
    │   ├── Audit/
    │   └── Eob/
    ├── ClaimStatus.Api.Tests/
    │   ├── Contract/ContractAssertions.cs       # every response checked against the contract
    │   └── Privacy/                             # 404 parity
    ├── fixtures/households/                     # synthetic HH-01, HH-05, HH-06, HH-07, HH-08
    └── harness/                                 # test builds only: claims-read fault switch, cache clock

.github/
├── CODEOWNERS                                   # Claims Operations, Privacy Office as required reviewers
└── workflows/claim-status.yml                   # build, tests, contract lint, spec gate

docs/runbooks/member-claim-status.md             # flag rollback; success-criteria dashboard
```

**Structure Decision**: The portal keeps its existing structure and gains one feature folder, so the design system, sign-in and session handling are reused rather than rebuilt. Claim logic lives in a separate read-only service so that one component holds the claims-read credentials, the cache and the privacy policy, and can be reviewed, tested and audited on its own. Core rules (status mapping, visibility, view building) sit in `ClaimStatus.Core` with no I/O, so the decision table and the scenarios run as fast unit tests.

## Complexity Tracking

No constitution principle is violated. The constitution asks for exceptions to be recorded with a reason and an owner; these two design choices add moving parts, so they are recorded here for the Gate 2 review.

| Choice | Why needed | Simpler alternative rejected because | Owner |
|---|---|---|---|
| Read-through cache: a second, short-lived copy of member claim views | Keeps status available during claims-system outages (FR-003) and within the read interface's rate limit at peak | Live calls only leave members with nothing during outages and exceed the rate limit; a nightly copy would always be stale and would become a second system of record | Engineering lead, Member Portal |
| New claim-status service rather than code in the portal's existing back end | Isolates the claims-read credentials, the cache and the visibility policy behind one least-privilege identity with its own reviewers | Adding to the portal back end would spread PHI handling and privacy rules across a much larger codebase with broader access | Engineering lead, Member Portal (architecture review at Gate 2) |
