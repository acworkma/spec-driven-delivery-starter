# Feature Specification: Vision rider for employer groups (retro-spec)

**Feature Branch**: none (retro-spec of epic EP-2025-0412)  
**Created**: 2026-11-18  
**Status**: Retro-spec (delivered 2025)  
**Input**: User description: "Offer employer groups a vision rider administered by Fabrikam Vision Services, so account managers can sell it, eligibility reaches Fabrikam and claims pay correctly."

> Written in 2026 from the [original epic](original-epic.md). Each Clarification notes when the 2025 team learned the answer; the [gap log](gap-log.md) adds up the cost.

## Clarifications

### Session 2026-11-18

- Q: Who approves the configuration? → A: A second configuration analyst; the product owner approves exceptions. (learned in build, week 6)
- Q: Are dependents covered, and to what age? → A: Yes, if the group covers dependents on medical, with the same age limit. (learned in UAT, week 9)
- Q: When does a new hire in a waiting period get the rider? → A: When their medical coverage starts. (learned in UAT, week 10)
- Q: How much lead time does setup need? → A: The first of a month at least 30 calendar days after approval; shorter needs product owner and underwriting approval. (learned in production, week 12)
- Q: What must be true before go-live? → A: Fabrikam accepts a synthetic test file and the eight standard test claims match. (learned in production, week 12)
- Q: What if a group terminates before go-live? → A: Cancel the request and tell Fabrikam to drop the group. (learned in production, week 14)
- Q: For mid-year additions, are allowances and frequency limits prorated? → A: No; they start fresh on the rider's effective date. (learned in production, week 15)

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Request a vision rider for a group (Priority: P1)

**Why this priority**: Every later step depends on a complete request with a workable date.

**Independent Test**: Submit complete, short-notice and terminated-group requests and check each outcome.

**Acceptance Scenarios**:

1. [US1-AS1] **Given** Woodgrove Bank (GRP-20417) is active on a compatible base plan, **When** complete request RR-2025-0042 is submitted on 2025-05-12, effective 2025-07-01, **Then** it is approved and moves to configuration.
2. [US1-AS2] (exception) **Given** today is 2025-06-10, **When** a request effective 2025-07-01 is submitted, **Then** it needs product owner and underwriting approval with a recorded reason.
3. [US1-AS3] (exception) **Given** Alpine Ski House's coverage ends before the requested effective date, **When** a request is submitted, **Then** it is blocked with a plain explanation.

---

### User Story 2 - Configure vision benefits from the grid (Priority: P1)

**Why this priority**: Errors made here surface later as wrong payments.

**Independent Test**: Build a test package and compare every value with the benefit grid.

**Acceptance Scenarios**:

1. [US2-AS1] **Given** approved request RR-2025-0042, **When** the configuration analyst builds the package, **Then** copays, frame and contact lens allowances and frequency limits match the benefit grid.
2. [US2-AS2] (exception) **Given** a built package, **When** the analyst who built it tries to approve it, **Then** approval is refused until a second analyst reviews it.
3. [US2-AS3] **Given** a rider effective 2025-07-01 for a group with a January plan year, **When** the package is built, **Then** allowances and frequency limits start fresh that day, with no proration.

---

### User Story 3 - Confirm Fabrikam Vision Services is ready (Priority: P2)

**Why this priority**: If Fabrikam cannot read our eligibility, members are turned away on day one.

**Independent Test**: Send a synthetic file; record an acceptance, a rejection and a non-response.

**Acceptance Scenarios**:

1. [US3-AS1] **Given** an approved package, **When** Fabrikam accepts a synthetic test file with an employee, a dependent child and a new hire, **Then** the acceptance is recorded as readiness evidence.
2. [US3-AS2] (exception) **Given** Fabrikam rejects the file or is silent for 5 business days, **When** that is recorded, **Then** go-live stays blocked and the vendor manager is alerted.

---

### User Story 4 - Prove vision claims pay as configured (Priority: P2)

**Why this priority**: Mismatches found after go-live mean reprocessed claims and member calls.

**Independent Test**: Run the eight test claims against a correct package and one with a deliberate error.

**Acceptance Scenarios**:

1. [US4-AS1] **Given** Fabrikam has accepted the test file, **When** the eight standard test claims run (exam, lenses, frames, contacts instead of glasses, frequency limit reached, out-of-network, dependent child, terminated member), **Then** all match expected results.
2. [US4-AS2] (exception) **Given** the frames claim pays above the allowance, **When** the result is recorded, **Then** go-live is blocked and the request returns to configuration with the evidence.

---

### User Story 5 - Go live, or stop cleanly (Priority: P3)

**Why this priority**: Go-live is one step, but the cases that stop it cause the costliest cleanup.

**Independent Test**: Take test requests to go-live: all checks passed, a new hire still waiting, a terminated group.

**Acceptance Scenarios**:

1. [US5-AS1] **Given** every readiness check has passed, **When** the effective date arrives, **Then** the rider is active for eligible employees and dependents.
2. [US5-AS2] **Given** an employee in a new-hire waiting period, **When** the rider goes live, **Then** their rider starts when their medical coverage starts.
3. [US5-AS3] (exception) **Given** the group terminates before go-live, **When** that is recorded, **Then** the request is cancelled and Fabrikam is told to drop the group.

---

### Edge Cases

- **Effective date changes after approval**: validated like a new request; readiness checks are re-run.
- **Glasses bought under prior coverage**: no carry-over; the full allowance applies from the effective date.
- **Only some employee classes eligible**: only those classes go on the eligibility file.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST capture rider, effective date, eligible employee classes and dependent eligibility for every request.
- **FR-002**: System MUST accept only first-of-month effective dates at least 30 calendar days after approval, unless the product owner and underwriting approve an exception.
- **FR-003**: System MUST block requests for groups that are inactive or whose coverage ends before the effective date.
- **FR-004**: System MUST build configuration from the benefit grid only, with approval by a second configuration analyst.
- **FR-005**: System MUST start allowances and frequency limits fresh on the rider's effective date, with no proration or carry-over.
- **FR-006**: System MUST apply the base plan's dependent age limit and new-hire waiting period.
- **FR-007**: System MUST send Fabrikam Vision Services a synthetic test eligibility file before go-live, record its response, and alert the vendor manager after 5 business days without one.
- **FR-008**: System MUST compare expected and actual results for the eight standard test claims and return any mismatch to configuration.
- **FR-009**: System MUST block go-live until configuration is approved, Fabrikam has accepted the test file and all eight test claims match.
- **FR-010**: System MUST cancel a request when its group terminates before go-live and tell Fabrikam to drop the group.
- **FR-011**: System MUST log who approved what and when, and use only synthetic members, such as CHP-0002286, in tests.

### Key Entities *(include if feature involves data)*

- **Employer group**: status, employee classes and base plan.
- **Rider request**: such as RR-2025-0042; effective date, eligible classes, dependent eligibility and approvals.
- **Benefit grid**: approved vision copays, allowances and frequency limits.
- **Configuration package**: setup built from the grid, with builder and approver.
- **Test eligibility file and administrator response**: synthetic members sent to Fabrikam, and its acceptance or rejection.
- **Test claim result**: expected and actual results for each standard test claim.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Fabrikam accepts every group's test eligibility file before the group's effective date.
- **SC-002**: Zero benefit mismatches are found after any group's effective date.
- **SC-003**: At least 90% of requests pass validation on first submission.
- **SC-004**: No rider starts inside the 30-day lead time without a recorded exception approval.

## Assumptions

- Fabrikam Vision Services is contracted to administer the vision benefit.
- The product owner owns the benefit grid and the test claims' expected results.
- Fabrikam's eligibility file layout must carry the new rider; the plan confirms this dependency.
- No member data is used, and no member-facing text is in scope.

## Out of Scope

- Pricing, rating and underwriting decisions.
- Member communications, such as ID cards and benefit summaries.
- Custom vision benefits.
- Contracting with Fabrikam Vision Services.
