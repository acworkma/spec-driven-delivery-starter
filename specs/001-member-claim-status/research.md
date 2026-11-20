# Research: Member claim status

**Feature**: [spec.md](./spec.md) | **Plan**: [plan.md](./plan.md) | **Date**: 2026-11-18

Phase 0 decisions. Each one answers a design question the plan raised; none changes the spec. Technology names are this example's assumptions.

## Decision 1: The status mapping is data owned by Claims Operations

**Decision**: Keep the mapping from internal status and reason codes to member-facing status, reason text and next-step text, in English and Spanish, in one versioned data file: `services/claim-status/config/status-mapping.json`. Claims Operations owns it. Changes arrive by pull request; CODEOWNERS requires a Claims Operations approver, and Language Services reviews Spanish text. A CI check fails the build unless every status code maps to exactly one of the six member-facing statuses, every entry has English and Spanish text, and no text contains anything that looks like an internal code. At runtime, a code missing from the mapping gets the generic message ("We're reviewing this claim. Please contact us.") and raises a PHI-free `unmapped_code` event (code, language, count) that feeds Claims Operations' content backlog and the SC-006 measure.

**Rationale**: The people accountable for the wording can change it without an engineering change, and reviewers see exactly which sentence changed. Validation in CI stops a broken mapping from shipping, and the runtime fallback means a missing entry never shows a raw code (FR-009). Unmapped-code counts tell Claims Operations which entries to write next.

**Alternatives considered**:

- **Hard-code the mapping in the service**: every wording change becomes a code change, a deployment and an engineering queue.
- **Keep member-facing text in the claims system**: its release cycle is quarterly, and member-facing wording does not belong in the system of record.
- **A content management system**: a better long-term home, but it adds a new system and integration for launch. Revisit once SC-006 data shows how often the text changes.

## Decision 2: Visibility is decided server-side, in one policy component

**Decision**: One component, `VisibilityPolicy`, decides whether the caller may see each claim, using the decision table in [data-model.md](./data-model.md). Every operation (list, detail, EOB link) calls it. Hidden claims go through the same fetch, cache and freshness steps as visible ones and are removed just before the response is built, so `updatedAt`, freshness, errors and timing are the same as for a member with no claims. Nothing is counted, sorted or returned before the policy runs, and the portal never receives a hidden claim or holds any privacy logic. Privacy inputs (age band, confidential communication request) are read fresh on every request and never cached; if they can't be read, the policy fails closed (FR-011). A table-driven test covers every row of the decision table, and households HH-05, HH-06, HH-07 and HH-08 exercise the boundaries end to end. The Privacy Office is a required reviewer for the component and its tests.

**Rationale**: One component means one place to review, test and audit. Filtering before the response is built is the only reliable way to keep hidden claims out of lists, counts, totals and messages (FR-012). Running hidden claims through the same pipeline closes side channels such as a different `updatedAt` or a faster response. Fresh inputs mean a new confidential communication request applies on the next request, not when a cache entry expires.

**Alternatives considered**:

- **Filter in the portal**: hidden claims would reach the member's device and browser memory. Rejected outright.
- **Check the rules separately in each endpoint**: the rules drift; the EOB path is where such checks are usually missed.
- **Ask the claims system to filter**: its read interface has no caller-based filtering, and Privacy Office changes would wait for its release cycle.

## Decision 3: Freshness through a read-through cache with a 24-hour maximum age

**Decision**: The service reads claims through a read-through cache keyed by an internal member reference. An entry older than 15 minutes is refreshed from the claims system on the next request. If the claims system is unavailable, an entry up to 24 hours old is served with `freshness: delayed` and its `updatedAt` time (US1-AS3). An entry older than 24 hours is never served: the service returns `503 CLAIMS_TEMPORARILY_UNAVAILABLE` and the portal shows the plain-language message with how to get help (US1-AS4). The 24-month window is applied at request time, not when the entry was cached. The cache holds member-facing claim views only, plus the sensitive-service marking the policy needs; it never holds diagnosis codes, clinical notes, dates of birth or confidential communication requests.

**Rationale**: Members see status that is usually minutes old, a clear and honest message during outages, and never information more than 24 hours behind the claims system (FR-003, SC-004). The cache also keeps peak load inside the read interface's rate limit.

**Alternatives considered**:

- **Live calls only**: any claims-system outage leaves members with nothing, and peak load exceeds the rate limit.
- **Nightly copy into a portal database**: up to 24 hours stale every day, and it becomes a second system of record.
- **Change events from the claims system**: it does not publish them today. Revisit if it does; the cache would then refresh on events instead of on a timer.

## Decision 4: EOBs through short-lived, single-document links

**Decision**: The EOB operation looks up the claim through the same path as `getClaim`, so visibility is checked first and a hidden claim gets the standard `404` (FR-012). For a visible claim with an EOB, the service asks the document service for a link to that one document that expires after 5 minutes, and the browser downloads it directly from the document service. The service audit-logs the request (FR-015) and never logs the link. If the claim is processed but its EOB has not been generated, the operation returns `409 EOB_NOT_READY` and the portal says EOBs are usually ready within 3 business days after processing (FR-014).

**Rationale**: The service never handles document content, links can't be reused or shared for long, and the visibility check lives in the same policy component as everything else.

**Alternatives considered**:

- **Stream the document through the service**: more PHI passing through the service and more load, with no benefit to the member.
- **Permanent links**: shareable, and impossible to revoke after a confidential communication request is added.
- **Email EOBs to members**: notifications are out of scope.
