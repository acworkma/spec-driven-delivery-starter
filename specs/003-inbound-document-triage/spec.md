# Feature Specification: Inbound document triage

**Feature Branch**: `003-inbound-document-triage`  
**Created**: 2026-11-18  
**Status**: Ready for planning  
**Input**: User description: "Route inbound documents to the right queue fast, attach them only when certain, and put people on everything uncertain."

## Clarifications

### Session 2026-11-18

- Q: Which document types are routed automatically? → A: Claim forms, medical records, prior-authorization requests, appeals and grievances, and provider correspondence. Anything else is "Other" and goes to human review.
- Q: When may the system attach a document to a member without a person? → A: Only on an exact member-ID match plus a matching date of birth or claim number; anything less goes to review (Privacy Office agreed).
- Q: What confidence threshold triggers auto-routing? → A: Operations sets it per type from evaluation results: 0.90 for every type at launch, reviewed monthly. A misroute rate above 2% pauses that type.
- Q: When does the deadline clock start? → A: At the fax receipt timestamp, including nights, weekends and holidays (utilization-management and appeals policy owners).
- Q: What data may be used to evaluate and improve classification? → A: Outside production, only synthetic or de-identified documents. Production corrections stay in production, used only under procedures the Privacy Office approves.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Route each document to the right queue (Priority: P1)

Each document gets a controlled type and confidence score; confident ones go straight to the owning team's queue.

**Why this priority**: Hand sorting is intake's biggest workload and main source of misroutes.

**Independent Test**: Run the synthetic fax set; compare each document's queue with its known type.

**Acceptance Scenarios**:

1. [US1-AS1] **Given** claim forms classified at 0.96 and 0.72 against a 0.90 threshold, **When** routing runs, **Then** the first reaches the claims queue untouched; the second goes to human review.
2. [US1-AS2] (exception) **Given** fax FAX-20261118-0042 with blank or unreadable pages, **When** it is classified, **Then** it goes to human review marked "unreadable".
3. [US1-AS3] (exception) **Given** a fax holding an appeal and a medical record, **When** it arrives, **Then** it is split into two documents, and a person confirms any uncertain split.

---

### User Story 2 - Identify the member and claim safely (Priority: P1)

Identifiers are matched to records; documents attach only when the match is certain.

**Why this priority**: Keying identifiers is the slowest step; a wrong-member attachment is a privacy incident.

**Independent Test**: Match synthetic documents with exact, partial and conflicting identifiers.

**Acceptance Scenarios**:

1. [US2-AS1] **Given** a document showing member ID CHP-0004417 and that member's claim CLM-2026-000183, **When** matching runs, **Then** the document is attached to both.
2. [US2-AS2] **Given** an exact member-ID match, a different date of birth and no claim number, **When** matching runs, **Then** a reviewer sees candidate matches with only the details needed to confirm one.
3. [US2-AS3] (exception) **Given** a document showing member ID CHP-0004417 and another member's claim, **When** matching runs, **Then** the document goes on privacy hold, unattached, for a privacy-trained reviewer.
4. [US2-AS4] (exception) **Given** an exact match for a member whose coverage has ended, **When** matching runs, **Then** it is still attached, flagged "coverage ended".

---

### User Story 3 - Review uncertain documents quickly (Priority: P2)

Reviewers confirm or correct suggestions shown beside the document with confidence scores.

**Why this priority**: P1 can use today's manual review; this makes it faster and safer.

**Independent Test**: Confirm, correct and escalate one synthetic task each.

**Acceptance Scenarios**:

1. [US3-AS1] **Given** a task suggesting "medical record" at 0.71, **When** the reviewer changes it to "appeal or grievance" with a reason code, **Then** it routes to the appeals and grievances queue, clocked from receipt, and the correction becomes a labeled example.
2. [US3-AS2] (exception) **Given** a reviewer who cannot decide, **When** they escalate, **Then** the task moves to the supervisor queue and any clock keeps running.

---

### User Story 4 - Never miss a deadline (Priority: P2)

Prior-authorization requests and appeals are timed from arrival; expedited ones are flagged and go first.

**Why this priority**: P1 already cuts waiting; this protects deadlines set by Contoso's utilization-management or appeals policy.

**Independent Test**: Send synthetic expedited requests at different hours.

**Acceptance Scenarios**:

1. [US4-AS1] **Given** an expedited prior-authorization request received at 9:05 a.m., **When** it is routed at 9:20 a.m., **Then** it tops the utilization-management queue, flagged, clocked from 9:05 a.m.
2. [US4-AS2] **Given** an unassigned expedited appeal, **When** half its window has passed, **Then** the queue supervisor is alerted.
3. [US4-AS3] (exception) **Given** an expedited appeal received at 11:40 p.m. on a Saturday, **When** it is classified, **Then** its clock starts at 11:40 p.m. and the on-call queue is notified.

---

### User Story 5 - Know how intake is performing (Priority: P3)

The product owner and supervisors see daily, by type, how intake performs, including misroutes (documents re-routed downstream).

**Why this priority**: Tunes the pilot; its misroute pause must be live before auto-routing begins.

**Independent Test**: Load a week of synthetic results.

**Acceptance Scenarios**:

1. [US5-AS1] **Given** yesterday's documents, **When** the intake report opens, **Then** it shows by type the volume, auto-route, human-review and misroute rates, time to queue, deadline-risk items and unreconciled pages, without member identifiers.
2. [US5-AS2] (exception) **Given** provider correspondence misrouted at 2.4% over the past week, **When** the rate is calculated, **Then** its auto-routing pauses and the product owner is alerted.

### Edge Cases

- **Duplicate faxes**: linked to the original; nothing is discarded without a person.
- **Non-member documents**, such as a Proseware marketing flyer: classified "Other" and reviewed.
- **Languages other than English**: human review through the existing language-access process.
- **Handwritten forms**: identifiers not read with confidence go to review, never guessed.
- **Faxes over 50 pages**, usually medical records: kept whole unless a person confirms a split.
- **Outage**: staff follow the manual downtime procedure; FR-020 applies.
- **Claim already closed**: attached, flagged "claim closed"; reopening stays a person's decision.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST give each fax or scanned batch a tracking ID, receipt timestamp (for mail, the mailroom's date-received stamp) and page count.
- **FR-002**: System MUST split multi-document faxes before classification; a person confirms uncertain splits.
- **FR-003**: System MUST classify each document as a claim form, medical record, prior-authorization request, appeal or grievance, provider correspondence, or Other, with a confidence score.
- **FR-004**: System MUST auto-route only non-Other documents at or above their type's threshold; the rest go to human review with a reason.
- **FR-005**: System MUST let Operations set each type's threshold (0.90 at launch) and record every change.
- **FR-006**: System MUST pause a type's auto-routing when its misroute rate exceeds 2% over a rolling week and alert the product owner; only a person resumes it.
- **FR-007**: System MUST extract member ID, name, date of birth, claim number and provider identifiers, with confidence scores.
- **FR-008**: System MUST attach automatically only on an exact member-ID match plus a matching date of birth or claim number; otherwise a reviewer sees candidate matches.
- **FR-009**: System MUST hold, unattached, any document whose identifiers point to different members, for privacy-trained reviewers only.
- **FR-010**: System MUST still attach documents for members whose coverage has ended, flagged "coverage ended".
- **FR-011**: System MUST pause automatic attachment and open a Privacy Office incident review whenever a wrong-member attachment is found.
- **FR-012**: System MUST show reviewers only the document, suggestions and member details needed to confirm a match, and let them confirm, correct with a reason code, or escalate.
- **FR-013**: System MUST keep corrections as labeled examples inside production, used only under Privacy Office procedures; evaluation elsewhere uses only synthetic or de-identified documents.
- **FR-014**: System MUST start a deadline clock at receipt, including nights, weekends and holidays, for every confirmed or suggested prior-authorization request, appeal or grievance.
- **FR-015**: System MUST flag expedited documents and put them first; uncertain ones count as expedited until a person decides.
- **FR-016**: System MUST alert the supervisor when half a window passes unassigned, and the on-call queue when expedited documents arrive outside business hours.
- **FR-017**: System MUST report the User Story 5 measures daily by type, without member identifiers or document content.
- **FR-018**: System MUST reconcile every received page daily and report any gap to the intake supervisor.
- **FR-019**: System MUST audit-log every view, route, attachment and correction, by a person or the system.
- **FR-020**: System MUST lose nothing during an outage, keep clocks running from receipt, and clear the backlog earliest deadline first.
- **FR-021**: System MUST process and store documents only in environments approved for protected health information, under the existing records-retention schedule.
- **FR-022**: System MUST NOT decide any authorization, appeal, grievance or claim; people decide.

### Key Entities *(include if feature involves data)*

- **Inbound fax**: also covers scanned batches; tracking ID, receipt timestamp, sender and page count.
- **Page**: one image, belonging to a document, hold or duplicate.
- **Document**: one logical document within a fax.
- **Document type**: one of six controlled types, with its threshold and queue.
- **Classification result**: suggested type, confidence and expedited indicator.
- **Extracted identifier**: a value read from a document, with confidence.
- **Match result**: the attached member and claim, or review candidates.
- **Work queue**: a team's work list, such as human review or on-call.
- **Review task**: a person's confirm, correct or escalate decision.
- **Deadline clock**: receipt start, policy window and alert time.
- **Privacy hold**: blocks attachment until a privacy-trained reviewer resolves it.
- **Audit event**: who or what acted on a document, and when.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Within 60 days of pilot start, at least 60% of documents auto-route untouched, with misroutes at 2% or less.
- **SC-002**: Median time from receipt to the correct queue falls from today's baseline to 30 minutes or less.
- **SC-003**: Zero documents attached to the wrong member; any occurrence triggers FR-011.
- **SC-004**: 100% of expedited prior-authorization requests and appeals reach the correct queue within 60 minutes of receipt, at any hour.
- **SC-005**: Manual keying time per document falls 50% against a time-study baseline.
- **SC-006**: 100% of received pages are reconciled daily.

## Assumptions

- Deadline windows come from Contoso's utilization-management and appeals policies, retention from the records-retention schedule; this spec sets neither.
- The pilot starts suggest-only; Operations turns on auto-routing type by type.
- Member-facing text and accessibility: not applicable, as nothing reaches members; staff screens follow Contoso's accessibility standard.

## Out of Scope

- Replacing the fax channel; a provider upload portal is a later feature.
- Clinical review of document content.
- Any automated decision on authorizations, appeals or claims.
- Email intake.
- Outbound faxes.
