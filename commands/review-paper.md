---
description: >
  Simulate a double-blind peer review of the current paper. Generates 2 independent
  reviewer reports in the style of top IS/CS conferences (ICIS, ECIS, MISQ level).
  Each report includes Summary, Strengths, Weaknesses, Minor Comments, and Overall
  Recommendation. Output is saved as simulated_reviews.md and can be fed directly
  into /respond-reviewers for systematic revision.
---

# Review Paper: **$ARGUMENTS**

Activate the **peer-review-engine** skill. Read `skills/peer-review-engine/SKILL.md` in full.

Execute the complete 6-step simulated peer review workflow:

1. **LOCATE & READ** the paper (draft.md or paper.tex — use the most recent version)
2. **ASSESS** against 7 evaluation dimensions (contribution, theory, method, literature, argumentation, writing, relevance)
3. **GENERATE Reviewer 1** — "The Methodologist" (focus: research design, rigor, validity, replicability)
4. **GENERATE Reviewer 2** — "The Theorist" (focus: contribution, positioning, theoretical depth, novelty)
5. **CALIBRATE** recommendations independently (do not harmonize reviewers)
6. **COMPILE & SAVE** to `simulated_reviews.md` with meta-reviewer summary and priority revision checklist

## Input

`$ARGUMENTS` can be:
- **Empty** — reviews the most recent draft (draft.md or paper.tex, whichever is newer)
- **File path** to a specific manuscript (e.g., `@draft_v2.md`, `@latex/paper.tex`)
- **Venue name** to calibrate review criteria (e.g., `ICIS`, `MISQ`, `ECIS`, `NeurIPS`)
- **"journal"** or **"conference"** to adjust review depth and tone accordingly

## Output

- `simulated_reviews.md` — 2 complete reviewer reports + meta-reviewer synthesis
- Each review: Summary, Strengths, Weaknesses, Minor Comments, Questions, Recommendation
- Priority revision checklist (ordered by impact)
- Ready for `/respond-reviewers simulated_reviews.md` to process feedback systematically
