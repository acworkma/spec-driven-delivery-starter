# Pair worksheet: your first spec

**Team**: ____________  **Product owner**: ____________  **Engineer**: ____________
**Epic**: ______________________________________________

> **Synthetic examples only.** No PHI, member data or real names on this sheet or in the tools.

## The four-box canvas (move 1, 10 minutes, product owner leads)

| 1. Problem and outcome | 2. Spec and acceptance |
|---|---|
| Who is affected? What should change? What's out of scope? | Rules and assumptions. One happy path and one exception in Given/When/Then. |
| | |
| **3. Handoffs and evidence** | **4. Improvements and unknowns** |
| Systems, people, dependencies, test data. What proves it works? | What would catch a gap earlier? Open questions. Measures to baseline. |
| | |

## The moves

| ✓ | Move | Timebox | Done when |
|---|---|---|---|
| ☐ | 1. Frame the intent (canvas above) | 10 min | The engineer can restate it |
| ☐ | 2. Draft the spec: `/speckit-specify` | 10 min | No tech stack in the spec |
| ☐ | 3. Clarify together: `/speckit-clarify` | 20 min | No open clarification on P1 stories |
| ☐ | 4. Make it testable: Given/When/Then, IDs, one exception per story | 20 min | QA can name the tests |
| ☐ | 5. Check the quality: `/speckit-checklist` + `python tools/spec_lint.py specs/<yours>` | 10 min | Checklist passes, or gaps are logged |
| ☐ | 6. Review it like code: pull request, two approvals | 10 min | Approved PR means Ready |
| ☐ | 7. Plan and slice | Later | Tasks exported; each PR cites its IDs |

## Spec smells: tick any you find, then fix them

- ☐ Technology choices in the spec
- ☐ More than five user stories
- ☐ Words a tester can't check (fast, easy, appropriate)
- ☐ A story with no exception path
- ☐ Privacy, visibility or audit rules left implicit
- ☐ Anything that looks like real data

## For the readout

- **What the spec surfaced** that we'd normally find late:
- **Still open, and who owns it:**
- **What blocked us:**
- **Will we use this next sprint?** Yes / No / Why:
