# Intent brief: Member claim status

**Product owner**: Product owner, Member Digital  |  **Engineering lead**: Engineering lead, Member Portal  |  **Date**: 2026-11-18

> Move 1 of the first-spec method. Ten minutes, product owner leads. This is the input to `/speckit-specify`.

## 1. Problem and outcome

- **Who**: members, subscribers managing household claims, and call-center agents.
- **Today**: "Where is my claim?" and "Why was it denied?" are top call drivers; the portal shows little.
- **Change**: members see claims, plain-language status and next steps, without calling.
- **Out of scope**: dental and vision claims, online appeals, notifications, provider and customer-service views.

## 2. Spec and acceptance

- **Rules and assumptions**: the claims system is the system of record; the document service holds Explanations of Benefits (EOBs); no diagnosis codes or clinical notes; dependents' claims only as Contoso's privacy policy allows; audit every view.
- **Happy path**: **Given** member CHP-0004417 has processed claim CLM-2026-000183, **When** they open Claims, **Then** they see its status, plan paid and what they may owe.
- **Exception**: **Given** the claims system is down, **When** the member opens Claims, **Then** they see a clear message and the last-updated time.

## 3. Handoffs and evidence

- **Systems**: claims system, document service, member portal, sign-in, audit store.
- **People**: Claims Operations, Privacy Office, Member Services, Language Services, Digital Accessibility.
- **Dependencies**: reason text from Claims Operations; claims-system test access.
- **Test data**: synthetic, e.g. household HH-07: subscriber 45; dependents aged 9, 16 (one sensitive-service claim) and 19.
- **Evidence**: call volumes, usability test, privacy audit sample, accessibility audit.

## 4. Improvements and unknowns

- **Catch gaps earlier**: Claims Operations and the Privacy Office review rules before build.
- **Open questions** (for `/speckit-clarify`):
  1. How far back should claims go?
  2. Which member-facing statuses, and who owns the mapping?
  3. What can a subscriber see about dependents' claims?
  4. How fresh must status be?
  5. Spanish at launch?
- **Measures to baseline**: claim-status calls from portal-registered members (90 days); share of denial codes with plain-language text.

## Prompt for /speckit-specify

```text
Add claim status to the member portal: "where is my claim?" and "why was it denied?" drive calls.
Members see recent claims: date of service, provider, status, billed, plan paid, what they may owe.
Explain each status plainly, with next steps, including denials and appeals.
Subscribers see dependents' claims only as privacy rules allow, with no trace of hidden ones.
Offer Explanation of Benefits downloads. No diagnosis codes or clinical notes; audit every view.
If the claims system is down, say so and show the last-updated time. Meet WCAG 2.2 AA.
Open: how far back, statuses and owner, dependent visibility, freshness, Spanish. Out: dental, vision, online appeals, notifications.
```
