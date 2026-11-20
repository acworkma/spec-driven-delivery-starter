# Tasks: Member claim status

**Input**: Design documents from `specs/001-member-claim-status/`  
**Prerequisites**: [plan.md](./plan.md), [spec.md](./spec.md), [research.md](./research.md), [data-model.md](./data-model.md), [contracts/](./contracts/), [quickstart.md](./quickstart.md)

**Tests**: Included. The constitution requires tests named after the scenarios they prove. In each story phase, write the tests first and confirm they fail before implementing.

**Organization**: Tasks are grouped by user story so each story can be built, tested and released on its own.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies on incomplete tasks)
- **[Story]**: The user story the task belongs to (US1 to US4)
- References in parentheses trace each task to functional requirements and acceptance scenarios in spec.md. The spec gate checks that they exist and that every FR has a task.

## Path Conventions

- Portal: `portal/src/features/claims/`, `portal/tests/`
- Service: `services/claim-status/src/`, `services/claim-status/tests/`, `services/claim-status/config/`

---

## Phase 1: Setup (shared infrastructure)

**Purpose**: Project skeleton, flags, ownership and synthetic test data.

- [ ] T001 Create the claim-status service solution (Api, Core and Infrastructure projects, plus Core and Api test projects) in services/claim-status/ as laid out in plan.md
- [ ] T002 [P] Add feature flags `member-claim-status` and `member-claim-status-dependents`, both off by default, in portal/src/config/feature-flags.ts and services/claim-status/src/ClaimStatus.Api/appsettings.json
- [ ] T003 [P] Add the CI workflow (build, tests, OpenAPI lint of contracts/claim-status-api.yaml, spec gate) in .github/workflows/claim-status.yml, and CODEOWNERS entries making Claims Operations a required reviewer of the status mapping and the Privacy Office of the visibility policy in .github/CODEOWNERS
- [ ] T004 [P] Create synthetic households HH-01, HH-05, HH-06, HH-07 and HH-08, with dates relative to the test run and no real data, in services/claim-status/tests/fixtures/households/, and the test-only harness (claims-read fault switch, cache clock) in services/claim-status/tests/harness/

---

## Phase 2: Foundational (blocks every user story)

**Purpose**: Read access, caching, mapping, audit, errors and contract checks that every story uses.

- [ ] T005 Implement the read-only client for the claims system's approved, versioned read interface, requesting no diagnosis codes or clinical notes, in services/claim-status/src/ClaimStatus.Infrastructure/ClaimsSystem/ClaimsReadClient.cs (FR-001, FR-010)
- [ ] T006 Implement the member context from the enterprise sign-in token, issuing and resolving opaque `memberRef` and `claimId` values, in services/claim-status/src/ClaimStatus.Api/Auth/MemberContext.cs (FR-001, FR-011)
- [ ] T007 Implement the read-through cache (refresh after 15 minutes, never serve anything over 24 hours old, member-facing fields only) in services/claim-status/src/ClaimStatus.Infrastructure/Cache/ClaimViewCache.cs (FR-003)
- [ ] T008 Implement the status-mapping loader and its CI check (six statuses, English and Spanish text, no raw codes) in services/claim-status/src/ClaimStatus.Core/Status/StatusMappingLoader.cs (FR-005, FR-016)
- [ ] T009 [P] Implement the audit writer for the existing enterprise audit store in services/claim-status/src/ClaimStatus.Infrastructure/Audit/AuditStoreWriter.cs (FR-015)
- [ ] T010 [P] Implement error responses (one `404` body for hidden, unknown and malformed references; `503` when nothing under 24 hours old exists; `Cache-Control: no-store` on every response) in services/claim-status/src/ClaimStatus.Api/Errors/ProblemResponses.cs (FR-003, FR-012)
- [ ] T011 [P] Implement the document-service client for 5-minute, single-document EOB links in services/claim-status/src/ClaimStatus.Infrastructure/Documents/EobLinkClient.cs (FR-014)
- [ ] T012 [P] Add contract checks that validate every API test response against contracts/claim-status-api.yaml, including closed schemas, in services/claim-status/tests/ClaimStatus.Api.Tests/Contract/ContractAssertions.cs (FR-002, FR-010, FR-012)
- [ ] T013 [P] Add PHI-free telemetry for SC-001 to SC-006 (counts and timings only, a daily status-match sample for SC-004, no member IDs or claim numbers) in services/claim-status/src/ClaimStatus.Api/Telemetry/ClaimStatusMetrics.cs

**Checkpoint**: Foundation ready. User story work can start.

---

## Phase 3: User Story 1 - See my recent claims (Priority: P1) 🎯 MVP

**Goal**: A signed-in member sees their claims from the last 24 months, newest first, with an honest freshness message.

**Independent Test**: Compare the HH-07 subscriber's list with the fixture data (quickstart.md, US1 rows).

### Tests for User Story 1 (write first; they must fail)

- [ ] T014 [P] [US1] Write tests US1_AS1 and US1_AS5 (every field, newest first, 24-month window, adjusted claim once as Adjusted) in services/claim-status/tests/ClaimStatus.Core.Tests/Claims/ClaimListTests.cs (FR-001, FR-002, US1-AS1, US1-AS5)
- [ ] T015 [P] [US1] Write tests US1_AS3 and US1_AS4 with the harness clock (a copy under 24 hours old is shown as delayed; nothing older is shown) in services/claim-status/tests/ClaimStatus.Core.Tests/Freshness/FreshnessTests.cs (FR-003, US1-AS3, US1-AS4)
- [ ] T016 [P] [US1] Write end-to-end tests US1-AS1 to US1-AS5 with households HH-07 and HH-01 in portal/tests/e2e/claims/claims-list.spec.ts (FR-001, FR-002, FR-003, FR-004, US1-AS1, US1-AS2, US1-AS3, US1-AS4, US1-AS5)

### Implementation for User Story 1

- [ ] T017 [US1] Implement the list view builder (24-month window on the viewing date, newest first, latest version only, amounts empty until processed) in services/claim-status/src/ClaimStatus.Core/Claims/ClaimViewBuilder.cs (FR-001, FR-002)
- [ ] T018 [US1] Implement GET /v1/members/{memberRef}/claims for `self`, with freshness and one audit event per view, in services/claim-status/src/ClaimStatus.Api/Endpoints/ClaimsEndpoints.cs (FR-001, FR-003, FR-015)
- [ ] T019 [US1] Build the claims list page and freshness notice ("Updated" time, delayed note, unavailable message, empty state, where to find dental and vision claims), with English and Spanish page text, in portal/src/features/claims/pages/ClaimsListPage.tsx and portal/src/features/claims/content/ (FR-002, FR-003, FR-004, FR-016)

**Checkpoint**: US1 works on its own behind `member-claim-status`.

---

## Phase 4: User Story 2 - Understand a claim and what happens next (Priority: P1)

**Goal**: A member opens a claim and sees each line, the status in plain language, why anything was denied and what to do next.

**Independent Test**: Open each HH-07 claim listed for US2 in quickstart.md and check the explanation and next step.

### Tests for User Story 2 (write first; they must fail)

- [ ] T020 [P] [US2] Write tests US2_AS1 and US2_AS4 (every line with a plain-language description and its own status; the other-plan note; no diagnosis codes or clinical notes anywhere in the response) in services/claim-status/tests/ClaimStatus.Core.Tests/Claims/ClaimDetailTests.cs (FR-007, FR-010, US2-AS1, US2-AS4)
- [ ] T021 [P] [US2] Write tests US2_AS2 and US2_AS3 (who we're waiting on and what to do; denial reason, appeal deadline, appeal link and EOB link) in services/claim-status/tests/ClaimStatus.Core.Tests/Status/NextStepTests.cs (FR-005, FR-006, FR-008, US2-AS2, US2-AS3)
- [ ] T022 [P] [US2] Write test US2_AS5 (an unmapped code gets the generic message in English and Spanish, never the code, and raises `unmapped_code`) in services/claim-status/tests/ClaimStatus.Core.Tests/Status/UnmappedCodeTests.cs (FR-009, FR-016, US2-AS5)
- [ ] T023 [P] [US2] Write end-to-end tests US2-AS1 to US2-AS5, in English and Spanish, in portal/tests/e2e/claims/claim-detail.spec.ts (FR-006, FR-007, FR-008, FR-009, FR-016, US2-AS1, US2-AS2, US2-AS3, US2-AS4, US2-AS5)

### Implementation for User Story 2

- [ ] T024 [US2] Implement the status mapper with the generic fallback and the `unmapped_code` event in services/claim-status/src/ClaimStatus.Core/Status/StatusMapper.cs (FR-005, FR-006, FR-009)
- [ ] T025 [US2] Implement GET /v1/members/{memberRef}/claims/{claimId} (lines, next step, denial details, other-plan flag) with one audit event per view in services/claim-status/src/ClaimStatus.Api/Endpoints/ClaimsEndpoints.cs (FR-007, FR-008, FR-010, FR-015)
- [ ] T026 [US2] Implement GET /v1/members/{memberRef}/claims/{claimId}/eob through the same claim lookup as T025, with an audit event, in services/claim-status/src/ClaimStatus.Api/Endpoints/EobEndpoints.cs (FR-008, FR-014, FR-015)
- [ ] T027 [US2] Build the claim detail page and service-lines table (totals first, every line, phone layout, denial and appeal panel, EOB link) in portal/src/features/claims/pages/ClaimDetailPage.tsx (FR-006, FR-007, FR-008)
- [ ] T028 [US2] Load Claims Operations' launch mapping (status, reason and next-step text in English and Spanish) into services/claim-status/config/status-mapping.json (FR-005, FR-008, FR-016)

**Checkpoint**: US1 and US2 together are the P1 release. Run quickstart.md before turning on `member-claim-status` beyond test accounts.

---

## Phase 5: User Story 3 - See my dependents' claims within privacy rules (Priority: P2)

**Goal**: The subscriber sees dependents' claims exactly as the Privacy Office's rules allow, and hidden claims leave no trace.

**Independent Test**: As the HH-07 subscriber, check each dependent against the visibility decision table in data-model.md.

### Tests for User Story 3 (write first; they must fail)

- [ ] T029 [P] [US3] Write table-driven tests for every row of the visibility decision table (V01 to V13), plus US3_AS1 and US3_AS3, in services/claim-status/tests/ClaimStatus.Core.Tests/Visibility/VisibilityPolicyTests.cs (FR-011, FR-013, US3-AS1, US3-AS3)
- [ ] T030 [P] [US3] Write tests US3_AS2 and US3_AS4 that compare whole responses (claims, list length, `updatedAt`, freshness, messages) with those for a dependent with no claims, in services/claim-status/tests/ClaimStatus.Core.Tests/Visibility/NoTraceTests.cs (FR-012, US3-AS2, US3-AS4)
- [ ] T031 [P] [US3] Write test US3_AS5 (hidden, unknown and malformed claim references get byte-identical `404` bodies) in services/claim-status/tests/ClaimStatus.Api.Tests/Privacy/NotFoundParityTests.cs (FR-012, US3-AS5)
- [ ] T032 [P] [US3] Write audit tests for US3_AS1 (subscriber, dependent, claim, action and time recorded; no clinical detail) in services/claim-status/tests/ClaimStatus.Core.Tests/Audit/DependentAuditTests.cs (FR-015, US3-AS1)
- [ ] T033 [P] [US3] Write end-to-end tests US3-AS1 to US3-AS5 with households HH-07 and HH-08 in portal/tests/e2e/claims/dependents.spec.ts (FR-011, FR-012, FR-013, US3-AS1, US3-AS2, US3-AS3, US3-AS4, US3-AS5)

### Implementation for User Story 3

- [ ] T034 [US3] Implement the visibility policy (fresh age and request inputs, fail closed) and apply it after fetch, cache and freshness but before anything is counted, sorted or returned, in services/claim-status/src/ClaimStatus.Core/Visibility/VisibilityPolicy.cs (FR-011, FR-012)
- [ ] T035 [US3] Implement GET /v1/household and dependent `memberRef` resolution in services/claim-status/src/ClaimStatus.Api/Endpoints/HouseholdEndpoints.cs (FR-011, FR-013)
- [ ] T036 [US3] Build the member selector with one privacy note on every dependent page and the adult-dependent message in portal/src/features/claims/components/MemberSelector.tsx (FR-013, FR-016)

**Checkpoint**: US3 works on its own behind `member-claim-status-dependents`. The Privacy Office signs off on T029 to T034 before the flag goes beyond test accounts.

---

## Phase 6: User Story 4 - Download my Explanation of Benefits (Priority: P3)

**Goal**: A member downloads an accessible EOB for any processed claim, or learns when it will be ready.

**Independent Test**: Download the EOB for CLM-2026-000183 and read it with a screen reader.

### Tests for User Story 4 (write first; they must fail)

- [ ] T037 [P] [US4] Write tests US4_AS1 and US4_AS2 (EOB offered for Processed, Denied and Adjusted claims; `EOB_NOT_READY` with the 3-business-days message) in services/claim-status/tests/ClaimStatus.Core.Tests/Eob/EobAvailabilityTests.cs (FR-014, US4-AS1, US4-AS2)
- [ ] T038 [P] [US4] Write test US4_AS3 (an EOB request for a hidden claim gets the standard `404`) in services/claim-status/tests/ClaimStatus.Api.Tests/Privacy/EobNotFoundTests.cs (FR-012, US4-AS3)
- [ ] T039 [P] [US4] Write end-to-end tests US4-AS1 and US4-AS2, including a screen-reader check of a synthetic EOB, in portal/tests/e2e/claims/eob.spec.ts (FR-014, FR-017, US4-AS1, US4-AS2)

### Implementation for User Story 4

- [ ] T040 [US4] Build the EOB download for every Processed, Denied and Adjusted claim, with the not-ready message and how to get other formats or languages, in portal/src/features/claims/components/EobDownload.tsx (FR-014, FR-016)

**Checkpoint**: All four stories work on their own.

---

## Phase 7: Polish and cross-cutting concerns

- [ ] T041 [P] Clear claim data on session timeout and return the member to the same page after sign-in in portal/src/features/claims/session/claims-session.ts, tested in portal/tests/e2e/claims/session-timeout.spec.ts (FR-018)
- [ ] T042 [P] Add axe-core checks for every Claims page in portal/tests/a11y/claims.a11y.spec.ts and complete the manual WCAG 2.2 AA audit with Digital Accessibility (FR-017)
- [ ] T043 [P] Get Language Services' review of Spanish text in portal/src/features/claims/content/claims.es.json and services/claim-status/config/status-mapping.json (FR-016)
- [ ] T044 Run quickstart.md with synthetic households, attach scenario evidence to the pull request, and write the flag rollback runbook and success-criteria dashboard guide in docs/runbooks/member-claim-status.md

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: no dependencies.
- **Foundational (Phase 2)**: depends on Setup; blocks every story.
- **User stories (Phases 3 to 6)**: depend on Foundational. Build in priority order (US1, US2, then US3, then US4), or in parallel with enough people.
- **Polish (Phase 7)**: after the stories it touches.

### User Story Dependencies

- **US1 (P1)**: needs only Foundational.
- **US2 (P1)**: needs Foundational; opens claims from the US1 list but its service tests run on their own. It delivers the EOB operation (T026) that US4 reuses.
- **US3 (P2)**: needs Foundational. Its policy then applies to every operation, including those from US1, US2 and US4.
- **US4 (P3)**: needs T026 from US2. US4-AS3 also needs the US3 policy (T034).

### Within Each User Story

- Tests first, named by scenario ID, and failing before implementation.
- Core logic before endpoints; endpoints before portal pages.
- A story is done when every one of its scenarios has passing evidence (constitution, principle III).

### Parallel Opportunities

- T002 to T004 in Setup, and T009 to T013 in Foundational.
- Every test task marked [P] within a story.
- Once Foundational is done, US1 and US2 can proceed in parallel, then US3.

## Parallel Example: User Story 1

```text
Task: "Write tests US1_AS1 and US1_AS5 in ClaimListTests.cs"
Task: "Write tests US1_AS3 and US1_AS4 in FreshnessTests.cs"
Task: "Write end-to-end tests US1-AS1 to US1-AS5 in claims-list.spec.ts"
```

## Implementation Strategy

### MVP first (P1: User Stories 1 and 2)

1. Complete Phase 1 and Phase 2.
2. Complete US1, then US2.
3. **Stop and validate** with quickstart.md, then turn on `member-claim-status` for a pilot group.
4. Measure against SC-001, SC-002, SC-004 and SC-006 before widening.

### Incremental delivery

1. US3 behind `member-claim-status-dependents`, after the Privacy Office signs off and the SC-003 audit sample is in place.
2. US4 last.
3. Each step is reversible: turning a flag off removes the feature with no data migration.

## Notes

- Tasks are AI-drafted and stay drafts until the tech lead approves them at Gate 2.
- Commit after each task or logical group; agent pull requests are never auto-merged.
- Use synthetic data only, in tests, screenshots, prompts and work items.
