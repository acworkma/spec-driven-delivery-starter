# Feature Specification: Group dental rider setup

**Feature Branch**: `002-group-dental-rider-setup`  
**Created**: 2026-11-18  
**Status**: Ready for planning  
**Input**: User description: "Adding a standard dental rider to an employer group's medical plan is slow, and errors surface as claim denials after go-live. Get a signed request to ready to pay claims with fewer handoffs, less waiting and less rework."

## Clarifications

### Session 2026-11-18

- Q: Which riders does this flow cover? → A: The three standard dental riders in the 2027 catalog. Vision follows the same pattern next; custom benefits keep the existing process.
- Q: What is the minimum lead time? → A: The first of a month at least 30 calendar days after approval; shorter needs product owner and underwriting approval.
- Q: Who approves the configuration package? → A: A second configuration analyst (four-eyes); the product owner approves exceptions.
- Q: What proves a rider is ready to pay claims? → A: The catalog's eight standard test claims (preventive, basic, major, waiting period, annual maximum reached, out-of-network, dependent child, terminated member) all match expected results.
- Q: For mid-year additions, what happens to deductibles and annual maximums? → A: They start at zero on the rider's effective date, with no proration.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Submit a complete rider request (Priority: P1)

**Why this priority**: Incomplete requests cause most of today's back-and-forth; catching them at intake removes rework later.

**Independent Test**: Submit complete, incomplete, short-notice and incompatible synthetic requests; check each outcome.

**Acceptance Scenarios**:

1. [US1-AS1] **Given** Northwind Traders (GRP-10482) is active on a base plan compatible with Dental Plus, **When** the account manager submits complete request RR-2026-0117 on 2026-11-18, effective 2027-01-01, **Then** it is approved and moves to configuration.
2. [US1-AS2] **Given** a request missing one class's contribution split and effective mid-month (2027-01-15), **When** it is submitted, **Then** the system names both problems plainly and keeps it in draft.
3. [US1-AS3] (exception) **Given** today is 2026-11-18, **When** a request effective 2026-12-01 is submitted, **Then** it goes to the exception route, needing product owner and underwriting approval with a recorded reason.
4. [US1-AS4] (exception) **Given** Tailspin Toys' base plan is incompatible with Dental Complete, **When** that rider is chosen, **Then** the request is blocked with a plain explanation and the compatible riders listed.

---

### User Story 2 - Configure from the catalog, not from scratch (Priority: P1)

**Why this priority**: Hand-built configuration is where benefit errors start; catalog values and a second check stop them early.

**Independent Test**: Generate a package for each rider and compare every value with the catalog.

**Acceptance Scenarios**:

1. [US2-AS1] **Given** approved request RR-2026-0117 for Dental Plus, **When** the analyst generates the package, **Then** deductible, annual maximum, preventive, basic and major coinsurance, waiting periods and frequency limits come from the catalog and cannot be typed in.
2. [US2-AS2] **Given** a rider effective 2027-07-01, midway through the group's plan year, **When** the package is generated, **Then** deductibles and annual maximums start at zero that day, with no proration.
3. [US2-AS3] (exception) **Given** a generated package, **When** the analyst who generated it tries to approve it, **Then** the system refuses and asks for a second analyst.
4. [US2-AS4] (exception) **Given** the Dental Plus catalog version changed after approval, **When** the package is generated, **Then** the request is re-validated, differences are listed and the package waits for product owner approval.

---

### User Story 3 - Confirm the administrator is ready before go-live (Priority: P2)

**Why this priority**: Claims fail if the administrator cannot recognize members on day one; today, waiting on it is invisible.

**Independent Test**: Send a synthetic test file and record an acceptance, a rejection and a non-response.

**Acceptance Scenarios**:

1. [US3-AS1] **Given** an approved package for GRP-10482, **When** Fabrikam Dental Administrators accepts a synthetic test eligibility file that includes member CHP-0004417, **Then** the acceptance is recorded as readiness evidence.
2. [US3-AS2] (exception) **Given** Fabrikam rejects the test file, **When** the rejection is recorded, **Then** go-live stays blocked and the request returns to configuration with Fabrikam's errors attached.
3. [US3-AS3] (exception) **Given** Fabrikam has not responded within 5 business days, **When** the fifth business day ends, **Then** the vendor manager is alerted and the request shows as waiting on the administrator.

---

### User Story 4 - Prove benefits pay as configured (Priority: P2)

**Why this priority**: Today mismatches surface as denials after go-live; testing first removes that rework.

**Independent Test**: Run the eight test claims against a correct package and one with a deliberate error.

**Acceptance Scenarios**:

1. [US4-AS1] **Given** Fabrikam has accepted the test file, **When** all eight test claims match expected results in the claims test region, **Then** the request is ready to pay claims.
2. [US4-AS2] (exception) **Given** the annual-maximum-reached test claim pays more than expected, **When** the result is recorded, **Then** go-live is blocked and a defect with both results returns the request to configuration.

---

### User Story 5 - See where a request is (Priority: P3)

**Why this priority**: Status emails drive many handoffs today, but the flow works without this view.

**Independent Test**: Move test requests through each stage; check what each role sees and when flags appear.

**Acceptance Scenarios**:

1. [US5-AS1] **Given** RR-2026-0117 is waiting on Fabrikam, **When** the account manager or product owner opens it, **Then** they see its stage, owner, business days in stage and blocker.
2. [US5-AS2] (exception) **Given** a request has been in one stage for more than 5 business days, **When** the sixth business day begins, **Then** it is flagged to the product owner.

---

### Edge Cases

- **Effective date changes after approval**: validated like a new request; readiness evidence is re-run.
- **Group terminates before go-live**: the request is cancelled with a reason; nothing goes live.
- **Duplicate request**: a second open request for the same group and rider is blocked.
- **Retired catalog product**: cannot be chosen; if retired mid-flight, the product owner picks a replacement or cancels.
- **Classes with different contributions**: each eligible class needs its own split; the test file covers every class.
- **Employees in a new-hire waiting period**: the rider starts with their medical coverage.
- **Dependent age limits**: the same as the base medical plan.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST offer only the 2027 catalog's three standard dental riders, capturing effective date, eligible classes, dependent eligibility and each class's contribution split.
- **FR-002**: System MUST check at submission that the group is active, the rider fits the base plan, required fields are complete and the effective date is the first of a month at least 30 calendar days after approval (the day it passes these checks).
- **FR-003**: System MUST send shorter lead times to an exception route needing product owner and underwriting approval with a reason.
- **FR-004**: System MUST NOT accept a retired rider or a duplicate open request for the same group and rider.
- **FR-005**: System MUST build the configuration package from catalog values only; non-standard benefits go to the custom-benefit process.
- **FR-006**: System MUST start deductibles and annual maximums at zero on the rider's effective date, unprorated, and apply the base plan's dependent age limit and new-hire waiting period.
- **FR-007**: System MUST require a second configuration analyst, never the author, to approve each package and each change.
- **FR-008**: System MUST re-validate a request when its catalog version changes and hold the package for product owner approval.
- **FR-009**: System MUST send Fabrikam a synthetic test eligibility file covering every eligible class and record its response.
- **FR-010**: System MUST alert the vendor manager after 5 business days without a Fabrikam response and count each request's days waiting on the administrator.
- **FR-011**: System MUST compare expected and actual results for the eight test claims, raise a defect on any mismatch, and re-run all eight after any change.
- **FR-012**: System MUST block go-live until the package is approved, Fabrikam has accepted the test file and all eight test claims match.
- **FR-013**: System MUST re-validate a changed effective date as a new request and cancel requests for groups that terminate before go-live.
- **FR-014**: System MUST show each request's stage, owner, business days in stage and blockers, and flag to the product owner any request in one stage for more than 5 business days.
- **FR-015**: System MUST hold only group, product and synthetic test data, never real member data; account managers see only their own groups' requests.
- **FR-016**: System MUST log who did what and when for every change, approval, exception and stage change, kept per the records-retention schedule.

### Key Entities *(include if feature involves data)*

- **Employer group**: such as Northwind Traders (GRP-10482); status, employee classes, base plan.
- **Base plan**: the group's medical plan; sets dependent age limit and new-hire waiting period.
- **Rider product (catalog)**: Dental Core, Dental Plus or Dental Complete at a catalog version; benefit values, compatible base plans, test claims, status.
- **Rider request**: such as RR-2026-0117; effective date, classes, dependents, contribution splits, owner, stage.
- **Configuration package**: setup generated from one catalog version, with its author and approver.
- **Test eligibility file**: synthetic members, such as CHP-0004417, for every eligible class.
- **Administrator response**: acceptance or rejection, errors and dates.
- **Test claim scenario and result**: a standard test claim with expected and actual results.
- **Readiness checklist**: go-live conditions and their evidence.
- **Stage history**: each stage change with who, when and wait reason.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Median elapsed time from approved request to ready to pay claims falls 40% against the previous 12 months.
- **SC-002**: At least 90% of requests pass validation on first submission.
- **SC-003**: Zero pilot go-lives have a benefit mismatch found after the effective date.
- **SC-004**: Handoffs outside the system (emails, spreadsheets) fall to 2 or fewer per request.
- **SC-005**: No request is returned for missing or wrong information more than once (clarification loops ≤ 1).
- **SC-006**: 100% of requests show time spent waiting on the administrator.

## Assumptions

- The product owner maintains the 2027 catalog, including expected results for the eight test claims.
- Fabrikam Dental Administrators already administers Contoso's dental benefits; production eligibility feeds are unchanged.
- After a mid-year start, deductibles and maximums reset with the group's plan year.
- Baselines use the previous 12 months; off-system handoffs are sampled monthly, the rest comes from stage history.
- No member data is used, so no Privacy Office question is open. No member-facing text; staff screens meet WCAG 2.2 AA.

## Out of Scope

- Custom or non-standard benefits, such as waived waiting periods.
- Onboarding a new dental administrator.
- Pricing, rating and underwriting decisions.
- Member communications, such as ID cards and benefit summaries.
- Vision riders (next).
