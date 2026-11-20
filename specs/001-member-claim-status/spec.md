# Feature Specification: Member claim status

**Feature Branch**: `001-member-claim-status`  
**Created**: 2026-11-18  
**Status**: Ready for planning  
**Input**: User description: "Members call to ask where their claim is and why it was denied. Show claim status, next steps, dependents' claims within privacy rules, and Explanation of Benefits (EOB) documents."

## Clarifications

### Session 2026-11-18

- Q: How far back should claims go? → A: 24 months by date of service, matching what members can request by phone.
- Q: Which member-facing statuses, and who owns the mapping? → A: Received, In review, Waiting for information, Processed, Denied, Adjusted. Claims Operations owns the mapping and reason text; unmapped codes get a generic message.
- Q: What can a subscriber see about dependents' claims? → A: The User Story 3 rules (FR-011), confirmed with the Privacy Office on 2026-11-18, including the no-trace rule.
- Q: How fresh must status be? → A: Within 24 hours of the claims system, with "Updated [date and time]" on the list.
- Q: Spanish at launch? → A: Yes for status labels, reason text and next steps; EOB documents stay as the document service produces them.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - See my recent claims (Priority: P1)

**Why this priority**: "Where is my claim?" is a top call driver.

**Independent Test**: Compare a synthetic member's list with the claims system's test data.

**Acceptance Scenarios**:

1. [US1-AS1] **Given** member CHP-0004417 has recent claims, **When** they open Claims, **Then** they see each claim's number, date of service, provider, status, amount billed, plan paid and what they may owe, newest first, with the "Updated" time.
2. [US1-AS2] **Given** a new member with no claims, **When** they open Claims, **Then** they're told claims usually appear a few weeks after a visit.
3. [US1-AS3] (exception) **Given** the claims system is down and claims were updated 6 hours ago, **When** the member opens Claims, **Then** those claims show with the "Updated" time and a note that recent changes may be missing.
4. [US1-AS4] (exception) **Given** claims haven't been updated for over 24 hours, **When** the member opens Claims, **Then** no claims show, and a message explains how to get help.
5. [US1-AS5] (exception) **Given** an adjusted claim, **When** the member opens Claims, **Then** it appears once, as its latest version, labeled Adjusted.

---

### User Story 2 - Understand a claim and what happens next (Priority: P1)

**Why this priority**: "Why was it denied?" is the other top call driver.

**Independent Test**: Open synthetic claims in each status and check each explanation and next step.

**Acceptance Scenarios**:

1. [US2-AS1] **Given** processed claim CLM-2026-000183 has three lines, **When** the member opens it, **Then** each line shows a plain-language description and amounts, and no diagnosis codes or clinical notes appear.
2. [US2-AS2] **Given** claims waiting on the provider and on the member's other-insurance details, **When** the member opens each, **Then** each says who we're waiting on and what, if anything, the member must do.
3. [US2-AS3] **Given** a denied claim, **When** the member opens it, **Then** they see the plain-language reason, how to appeal and by when, and the EOB.
4. [US2-AS4] **Given** one of a claim's three lines was denied, **When** the member opens it, **Then** each line shows its own status, and the denied line its reason.
5. [US2-AS5] (exception) **Given** a denial reason with no plain-language mapping, **When** the member opens the claim, **Then** a generic "We're reviewing this claim" message replaces the code, and the gap is logged for Claims Operations.

---

### User Story 3 - See my dependents' claims within privacy rules (Priority: P2)

**Why this priority**: Parents call about children's claims, but privacy mistakes cause real harm.

**Independent Test**: As synthetic household HH-07's subscriber (dependents aged 9, 16 and 19), check each dependent against the rules.

**Acceptance Scenarios**:

1. [US3-AS1] **Given** the 9-year-old has claims, including CLM-2026-000201, **When** the subscriber opens them, **Then** all are shown, and each view is audit-logged.
2. [US3-AS2] (exception) **Given** the 16-year-old has two routine claims and one sensitive-service claim, **When** the subscriber views that dependent, **Then** only the routine claims appear, and no count, total or message hints at a third.
3. [US3-AS3] **Given** the 19-year-old, **When** the subscriber selects them, **Then** a message says adult dependents' claims are private, whether or not any exist.
4. [US3-AS4] (exception) **Given** a 9-year-old with a confidential communication request on file, **When** the subscriber views that dependent, **Then** the page looks exactly like one for a dependent with no claims.
5. [US3-AS5] (exception) **Given** a link to the 16-year-old's sensitive-service claim, **When** the subscriber opens it, **Then** they see the same "We can't find this claim" page as for a nonexistent claim.

---

### User Story 4 - Download my Explanation of Benefits (Priority: P3)

**Why this priority**: Members already get EOBs by mail.

**Independent Test**: Download a synthetic claim's EOB and read it with a screen reader.

**Acceptance Scenarios**:

1. [US4-AS1] **Given** a processed claim, **When** the member selects "Download Explanation of Benefits", **Then** an accessible document opens, with help for other formats or languages.
2. [US4-AS2] (exception) **Given** a claim processed yesterday, **When** the member opens it, **Then** it says the EOB is usually ready within 3 business days after processing.
3. [US4-AS3] (exception) **Given** a dependent's hidden claim, **When** the subscriber requests its EOB, **Then** the response matches that for a nonexistent claim.

### Edge Cases

- **Coverage ended**: claims from covered dates stay visible within the 24-month window.
- **Other plan paid first**: the claim says "Processed by your other plan first".
- **Duplicate submission**: Denied, with the reason "This is a copy of a claim we already received. You don't need to do anything."
- **Many service lines**: totals first, then every line, readable on a phone.
- **Dental and vision**: not shown; the page says where to find them.
- **Session timeout**: details leave the screen; after sign-in, the member returns to the same page.
- **Spanish preference**: labels and messages switch; provider names and EOB documents appear as received.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST show signed-in members their own claims from the last 24 months by date of service, newest first, including ended coverage; adjusted claims appear once, as the latest version.
- **FR-002**: System MUST show each claim's number, date of service, provider, status, amount billed, plan paid and what the member may owe (once processed).
- **FR-003**: System MUST show claim information no more than 24 hours behind the claims system, with its "Updated" time, and say plainly when it can't refresh.
- **FR-004**: System MUST show a plain-language empty state when there are no claims.
- **FR-005**: System MUST give each claim one of the six statuses, using Claims Operations' mapping, with plain-language text on what happens next.
- **FR-006**: System MUST say whom a Waiting for information claim awaits (provider or member) and what, if anything, the member must do.
- **FR-007**: System MUST show every service line with a plain-language description, amounts and its own status, and say "Processed by your other plan first" when another plan paid first.
- **FR-008**: System MUST show for denials the plain-language reason, how and by when to appeal, a link to the existing appeal process, and the EOB.
- **FR-009**: System MUST show "We're reviewing this claim. Please contact us." for unmapped codes, never the code, and log the gap for Claims Operations.
- **FR-010**: System MUST NOT show diagnosis codes, clinical notes or other clinical detail.
- **FR-011**: System MUST let only the subscriber see dependents' claims, by age on the viewing day: under 13, all; 13–17, all but sensitive-service claims (per Contoso's privacy policy); 18 and over, none. It MUST show none for a dependent with a confidential communication request, or whose age or privacy status it can't confirm.
- **FR-012**: System MUST leave no trace of hidden claims in any list, count, total, message or EOB, and answer requests for them exactly as for nonexistent claims.
- **FR-013**: System MUST show one privacy note on every dependent's page and, for dependents 18 and over, that their claims are private, whether or not any exist.
- **FR-014**: System MUST offer an accessible EOB for Processed, Denied and Adjusted claims, explain other formats and languages, and say when one isn't ready (usually 3 business days after processing).
- **FR-015**: System MUST audit-log every view of claim information and every EOB request: who, whose claim, which claim, what and when.
- **FR-016**: System MUST show status labels, reason text and next steps in English or Spanish, per the member's language preference.
- **FR-017**: System MUST meet WCAG 2.2 AA on every member-facing page.
- **FR-018**: System MUST clear claim information from the screen on session timeout and return the member to the same page after sign-in.

### Key Entities *(include if feature involves data)*

- **Member**: a covered person; member ID such as CHP-0004417.
- **Coverage**: covered dates, and the subscriber.
- **Dependent relationship**: subscriber, dependent and age band.
- **Claim**: numbered like CLM-2026-000183; adjusted claims have versions.
- **Claim line**: one service: description, amounts, status.
- **Member-facing status**: one of six, in English and Spanish.
- **Reason mapping**: plain-language text for each internal code; owned by Claims Operations.
- **EOB document**: a claim's Explanation of Benefits, from the document service.
- **Privacy restriction**: sensitive-service marking or confidential communication request.
- **Audit event**: who viewed which claim information, and when.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Claim-status calls from portal-registered members fall 25% in the 90 days after launch versus the 90 days before.
- **SC-002**: In moderated usability testing, 9 of 10 members find a claim's status and next step in under 60 seconds.
- **SC-003**: No restricted dependent claim is shown to a subscriber in user acceptance testing or the first 90 days (privacy audit sample).
- **SC-004**: Portal status matches the claims system within 24 hours for 99.5% of sampled claims.
- **SC-005**: Member-facing pages pass a WCAG 2.2 AA audit before launch.
- **SC-006**: At least 95% of denied claims show a mapped plain-language reason.

## Assumptions

- Members use the existing sign-in; the claims system and document service stay the systems of record.
- The claims system marks sensitive-service claims per the Privacy Office's definition (one such line marks the whole claim) and holds confidential communication requests.
- Claims Operations supplies English and Spanish text before launch; Language Services reviews the Spanish.
- Audit records follow Contoso's records-retention schedule, set by Records Management.

## Out of Scope

- Dental and vision claims.
- Adult dependents granting a subscriber access.
- Filing appeals online.
- Provider and customer-service views.
- Notifications.
