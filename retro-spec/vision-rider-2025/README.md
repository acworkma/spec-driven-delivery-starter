# Retro-spec drill: Vision rider (2025)

A worked example of the **retro-spec drill**: rewrite an epic already delivered the old way as a spec, then log the gaps the spec would have surfaced before build. It pairs with [002-group-dental-rider-setup](../../specs/002-group-dental-rider-setup/spec.md), which applies the lessons to dental riders.

Everything here is fictional: companies, groups and identifiers are synthetic, and every cost is illustrative.

| File | What it is |
|---|---|
| [original-epic.md](original-epic.md) | The 2025 epic as written, gaps and all |
| [spec.md](spec.md) | Our retro-spec of that epic |
| [gap-log.md](gap-log.md) | Each gap, when 2025 found it, and the cost |

## Run the drill (40 minutes, in pairs)

Pair a product owner with an engineer. Don't open `spec.md` or `gap-log.md` until step 3.

1. **Read (5 min).** Read `original-epic.md`; note what you would ask before building.
2. **Re-spec (15 min).** Paste the epic into `/speckit-specify`, then run `/speckit-clarify`. Answer from experience or mark a question unknown. Give every story an exception scenario.
3. **Compare (10 min).** Put your spec beside `spec.md`. Which questions did each of you miss? Our Clarifications note when the 2025 team learned each answer.
4. **Log (10 min).** Fill in a copy of the gap-log table, one row per gap, and a three-line summary.

Next, run the [same drill](../../workshop/retro-spec-drill.md) on your own delivered epic, after removing customer names, people and member data.

## How to read the gap log

Each row is a question or rule the spec forces into the open before build.

- **Where it surfaced in 2025**: the stage (build, UAT or production) and week the team found out. The later, the costlier.
- **Illustrative cost**: invented, order-of-magnitude figures that show the pattern, not real data.
- **Move that catches it**: the first move that would have raised the gap: **Clarify** (move 3, `/speckit-clarify`), **Make it testable** (move 4, Given/When/Then with an exception path), **Quality checklist** (move 5, the checklist and spec gate) or **Plan** (move 7, dependencies and contracts in `/speckit-plan`).

Read down the last column to choose which move to practice first.
