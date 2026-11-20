# Data Model: Member claim status

**Feature**: [spec.md](./spec.md) | **Plan**: [plan.md](./plan.md) | **Date**: 2026-11-18

The claim-status service owns no system of record. It reads the claims system through its approved read interface, keeps member-facing claim views in a read-through cache for at most 24 hours, and writes audit events to the existing enterprise audit store. Field names match [contracts/claim-status-api.yaml](./contracts/claim-status-api.yaml). Every example is synthetic.

**Where each field lives**:

- **Returned**: sent to the portal in API responses.
- **Cached**: held in the read-through cache, never more than 24 hours.
- **Internal**: used in memory for one request; never cached, logged or returned.

## Entities

### Member

| Field | Type | Where | Rules |
|---|---|---|---|
| `memberId` | string | Internal | `CHP-` and 7 digits, such as `CHP-0004417`. Never in URLs, logs, telemetry or responses. |
| `memberRef` | string | Returned | `self`, or `m_` and 22 letters or digits for a dependent: a keyed hash scoped to the subscriber. Stable, not guessable, meaningless outside the service. |
| `displayName` | string | Returned | First name as held by Contoso, at most 60 characters. Test environments hold synthetic names only. |
| Language | `en` or `es` | Internal | From the `Accept-Language` header, which the portal sets from the member's language preference. Default `en`. |

### Coverage

| Field | Type | Where | Rules |
|---|---|---|---|
| `subscriberMemberId` | string | Internal | The subscriber on the coverage. |
| `startDate`, `endDate` | date | Internal | `endDate` is empty while coverage is active. Claims for dates inside a coverage period stay visible after it ends, within the 24-month window (FR-001). |

### Dependent relationship

| Field | Type | Where | Rules |
|---|---|---|---|
| `subscriberMemberId`, `dependentMemberId` | string | Internal | Only the subscriber can view a dependent's claims (FR-011). |
| `relationship` | `spouse`, `child`, `otherDependent` | Returned | Shown in the member selector. |
| `ageBand` | `under13`, `13to17`, `18plus`, `unknown` | Internal | Computed on every request from the date of birth on the viewing date, in Contoso's business time zone. The date of birth itself is never cached, logged or returned. `unknown` when it can't be read. |
| `confidentialCommunicationRequest` | `yes`, `no`, `unknown` | Internal | Read on every request; never cached. `unknown` when it can't be read. |
| `claimsAccess` | `available`, `adultDependentPrivate` | Returned | `adultDependentPrivate` for every dependent 18 or over. Never reveals a confidential communication request. |

### Claim

| Field | Type | Where | Rules |
|---|---|---|---|
| `claimId` | string | Returned, Cached | `c_` and 22 letters or digits: a keyed hash of the claim number. Stable, so saved links keep working; not guessable. |
| `claimNumber` | string | Returned, Cached | `CLM-`, a 4-digit year and 6 digits, such as `CLM-2026-000183`. Shown to the member; never logged or used in paths. |
| `version` | integer ≥ 1 | Cached | Each adjustment creates a version. Only the latest is used (FR-001). |
| `dateOfService` | date | Returned, Cached | First date of service; drives the 24-month window. |
| `providerName` | string | Returned, Cached | Display name of the billing provider. |
| `internalStatusCode` | string | Cached | Mapped to `status`; never returned. |
| `status` | member-facing status | Returned | One of the six values below. |
| `waitingOn` | `provider`, `member` or empty | Returned | From the mapping; set only for Waiting for information (FR-006). |
| `reasonCode` | string or empty | Cached | Denial reason. Mapped to plain-language text; never returned. |
| `amountBilled` | money | Returned, Cached | US dollars, two decimal places. |
| `planPaid`, `youMayOwe` | money or empty | Returned, Cached | Empty until the claim is processed. |
| `otherPlanPaidFirst` | boolean | Returned, Cached | Drives the note "Processed by your other plan first" (FR-007). |
| `sensitiveService` | boolean | Cached | The claims system's marking under the Privacy Office's definition. True when any line is a sensitive service, so a claim is hidden whole, never line by line. Never returned or logged. |
| `appealDeadline` | date or empty | Returned, Cached | For denied claims and denied lines. |
| `eobDocumentId` | string or empty | Cached | Document-service key; never returned. |
| `updatedAt` | timestamp | Returned | When the service last read this member's claims from the claims system. |

### Claim line

| Field | Type | Where | Rules |
|---|---|---|---|
| `lineNumber` | integer ≥ 1 | Returned, Cached | All lines are returned, however many there are. |
| `serviceDescription` | string | Returned, Cached | The claims system's member-friendly description, the same text printed on EOBs today, such as "Office visit". Never a diagnosis or procedure code. |
| `amountBilled`, `planPaid`, `youMayOwe` | money | Returned, Cached | `planPaid` and `youMayOwe` are empty until processed. |
| `status` | `processed`, `denied` or empty | Returned | Empty until processed (FR-007). |
| `reasonCode` | string or empty | Cached | Mapped to `denialReason`; never returned. |

### Member-facing status

| Value | English label | Spanish label |
|---|---|---|
| `received` | Received | Recibida |
| `inReview` | In review | En revisión |
| `waitingForInformation` | Waiting for information | En espera de información |
| `processed` | Processed | Procesada |
| `denied` | Denied | Denegada |
| `adjusted` | Adjusted | Ajustada |

Spanish labels agree with *reclamación* (claim). Language Services confirms them before launch.

### Reason mapping

One entry per internal code in `services/claim-status/config/status-mapping.json`, owned by Claims Operations: `code`, `kind` (`status` or `reason`), `memberStatus` (status codes only), `waitingOn`, and `text` and `nextStep` in `en` and `es`. CI rejects the file unless every status code maps to exactly one member-facing status, every entry has both languages, and no text looks like an internal code.

### EOB document

| Field | Type | Where | Rules |
|---|---|---|---|
| `availability` | `available`, `notReadyYet`, `notApplicable` | Returned | `available` or `notReadyYet` for Processed, Denied and Adjusted claims; `notApplicable` before processing (FR-014). |
| `url`, `expiresAt` | link, timestamp | Returned | Only from the EOB operation. One document, expires after 5 minutes, never logged. |
| `alternateFormatHelp` | string | Returned | How to ask for another format or language through Contoso's existing process. |

### Privacy restriction

Not stored by this service. Derived on each request from the claim's `sensitiveService` marking and the dependent's `confidentialCommunicationRequest`, and applied through the visibility decision table below. The Privacy Office owns the rules (Clarification 3).

### Audit event

| Field | Type | Rules |
|---|---|---|
| `eventId` | UUID | |
| `occurredAt` | timestamp (UTC) | |
| `viewerMemberId` | string | The signed-in member. |
| `subjectMemberId` | string | Whose claims were requested. |
| `relationship` | `self`, `dependent` | |
| `action` | `listViewed`, `detailViewed`, `eobLinkIssued` | |
| `claimNumbers` | list of strings | Claims shown (list) or requested (detail, EOB). Empty for a reference that matches no claim. |
| `outcome` | `shown`, `notFound`, `unavailable`, `eobNotReady` | `notFound` attempts on hidden claims support privacy monitoring and the SC-003 audit sample. |
| `channel` | `memberPortal` | |
| `correlationId` | UUID | Links to PHI-free telemetry. |

Audit events go to the existing enterprise audit store (covered platform, access-controlled), never to application logs. They hold no clinical detail, amounts or reasons. Retention follows Contoso's records-retention schedule; this feature sets none.

## Validation rules

1. **24-month window**: `dateOfService` is on or after the viewing date minus 24 months, checked on every request.
2. **Order**: `dateOfService` newest first; ties by `claimNumber`, highest first.
3. **Adjusted claims**: only the latest version is used, and its status is `adjusted`.
4. **Amounts**: `planPaid` and `youMayOwe` are empty until processed; after that, `planPaid + youMayOwe ≤ amountBilled`.
5. **Freshness**: a view whose `updatedAt` is more than 24 hours old is never returned.
6. **Text**: every member-facing string comes from the mapping or the portal's content files; internal codes never reach a response.
7. **Visibility**: the policy runs after fetch, cache and freshness and before anything is counted, sorted or returned.
8. **References**: an unknown, malformed or hidden `memberRef` or `claimId` gets the standard `404`.

## Status mapping: internal code to member-facing status

Internal codes are synthetic examples. The live mapping is Claims Operations' data file.

| Internal code | Meaning in the claims system | Member-facing status | Waiting on | Next-step text (English) |
|---|---|---|---|---|
| `RCV-01` | Received, not yet reviewed | Received | | We got this claim. Most claims are processed within 30 days. |
| `PND-10` | Pended for internal review | In review | | We're reviewing this claim. You don't need to do anything right now. |
| `PND-20` | Pended: information requested from the provider | Waiting for information | provider | We've asked your provider for more information. You don't need to do anything. |
| `PND-30` | Pended: other-insurance details requested from the member | Waiting for information | member | Tell us whether you have other health insurance. Answer the letter we sent you, or call the number on your member ID card. |
| `FIN-PD` | Finalized: paid, or applied to the deductible | Processed | | Here's what we paid and what you may owe. Your provider may bill you for what you owe. |
| `FIN-DN` | Finalized: all lines denied | Denied | | See why below. You can appeal until {appealDeadline}. |
| `FIN-AJ` | Finalized: adjustment of an earlier version | Adjusted | | We changed how we processed this claim. Your updated Explanation of Benefits shows what changed. |
| Any other code | Not in the mapping | In review | | Generic message (below); raises `unmapped_code`. |

Reason codes (synthetic):

| Reason code | English reason | Spanish reason |
|---|---|---|
| `R-AUTH` | This service needed our approval before you got it, and we didn't receive a request. | Este servicio necesitaba nuestra aprobación antes de recibirlo y no recibimos una solicitud. |
| `R-NCOV` | Your plan doesn't cover this service. | Su plan no cubre este servicio. |
| `R-DUP` | This is a copy of a claim we already received. You don't need to do anything. | Esta es una copia de una reclamación que ya recibimos. No tiene que hacer nada. |
| `ZZ-999` | Deliberately unmapped; test fixtures only. | |

Fixed member-facing text:

| Use | English | Spanish |
|---|---|---|
| Generic (unmapped code) | We're reviewing this claim. Please contact us. Call the number on your member ID card. | Estamos revisando esta reclamación. Comuníquese con nosotros al número que aparece en su tarjeta de miembro. |
| Other plan paid first | Processed by your other plan first. | Procesada primero por su otro plan. |
| EOB not ready | Your Explanation of Benefits isn't ready yet. It's usually ready within 3 business days after we process your claim. | Su Explicación de Beneficios aún no está lista. Por lo general, está lista dentro de los 3 días hábiles después de que procesamos su reclamación. |
| Freshness | Updated {date and time} | Actualizado: {fecha y hora} |

## Visibility decision table

Applies when the subscriber views a dependent on their coverage. A member always sees their own claims. Any other viewer, such as a spouse who is not the subscriber, sees no one else's claims: `listHousehold` returns only `self`, and any other `memberRef` gets the standard `404`.

| Rule | Dependent's age band (viewing day) | Sensitive-service claim | Confidential communication request on file | Visible to subscriber? | What the subscriber sees |
|---|---|---|---|---|---|
| V01 | Under 13 | No | No | Yes | The claim |
| V02 | Under 13 | Yes | No | Yes | The claim |
| V03 | Under 13 | No | Yes | No | The same page as for a dependent with no claims |
| V04 | Under 13 | Yes | Yes | No | The same page as for a dependent with no claims |
| V05 | 13–17 | No | No | Yes | The claim |
| V06 | 13–17 | Yes | No | No | Nothing: no trace in lists, counts, totals or messages |
| V07 | 13–17 | No | Yes | No | The same page as for a dependent with no claims |
| V08 | 13–17 | Yes | Yes | No | The same page as for a dependent with no claims |
| V09 | 18 and over | No | No | No | The adult-dependent privacy message |
| V10 | 18 and over | Yes | No | No | The adult-dependent privacy message |
| V11 | 18 and over | No | Yes | No | The adult-dependent privacy message |
| V12 | 18 and over | Yes | Yes | No | The adult-dependent privacy message |
| V13 | Unknown (age or request can't be read) | Any | Any | No | "We can't show these claims right now", the same message as an outage |

Notes:

- Granting access to adult dependents' claims is a separate feature. Until it ships, V09 to V12 are always No.
- Every row is one test case in `VisibilityPolicyTests`, named by rule, such as `V06_13_to_17_sensitive_no_request_hidden`.
- Every dependent page shows the same privacy note, whatever the rows above decide (FR-013).

## Claim status lifecycle

Received → In review → (Waiting for information ⇄ In review) → Processed or Denied → Adjusted (when a processed or denied claim is reprocessed). Only the latest version of an adjusted claim is shown.
