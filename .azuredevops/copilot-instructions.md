# Copilot code review instructions

When reviewing a pull request in this repository:

- **Traceability:** check that the description cites the FR, scenario and task IDs it implements, and that they exist in the feature's `spec.md` and `tasks.md`.
- **Flow-forward:** if behavior changes but `specs/**/spec.md` doesn't, flag it.
- **Tests:** test names should match the scenarios they prove, e.g. `US1_AS3_...`. Flag exception scenarios (`(exception)` in the spec) that have no test.
- **Data:** flag anything that looks like PHI, real member data, real names or secrets, including in test fixtures and logs.
- **Constitution:** flag direct database access to systems of record, missing audit events on member-data access, and member-facing text without plain-language or accessibility consideration.
- **Tone:** findings are suggestions for a person to accept. Never approve on anyone's behalf.
