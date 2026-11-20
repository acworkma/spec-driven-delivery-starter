# Measures: is spec-driven delivery working?

Baseline first, using the last three to six months of similar work. Then measure the pilot the same way. Measure the whole flow, not AI output.

| Measure | Definition | GitHub | Azure DevOps |
|---|---|---|---|
| Clarification loops | Times a story or request goes back to the product owner for missing or wrong information after it was called ready | Count `needs-clarification` label events per issue | Count transitions back to a "Needs clarification" state, or a tag, per work item (Analytics view or query) |
| First-pass acceptance | Share of stories accepted without being reopened or failing acceptance | Issues closed and not reopened within 30 days | Work items that reach Closed without returning to Active |
| Rework | Bugs or reopened work linked to a story within 30 days of done | Issues labeled `bug` that link to the story | Bugs with a parent or related link to the story |
| Waiting time | Time in a state with no one working on it, e.g. waiting for review, a vendor or an environment | Project board status durations | Cycle-time and time-in-state from Analytics |
| Gaps found before build | Clarifications answered and checklist items fixed before Spec Ready | Count the `- Q:` lines plus checklist fixes in the spec PR | Same, from the spec PR in Azure Repos |
| Gaps found late (baseline) | Gaps from the retro-spec drill that surfaced in UAT or production | `retro-spec/*/gap-log.md` | Same |
| Spec review time | Spec PR opened → both approvals | PR timeline | PR timeline |
| Outcome | The feature's own success criteria (`SC-###`) | Production telemetry | Production telemetry |

## Rules of thumb

- **Pick two measures for a pilot.** Clarification loops and first-pass acceptance are the usual pair.
- **Compare like with like:** similar size, similar team, a similar time of year.
- **Never set a target on one throughput number.** It will be gamed.
- **Don't measure prompts, AI suggestions accepted or lines generated as outcomes.** They are activity, not value.
