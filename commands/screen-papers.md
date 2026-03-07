---
description: >
  Systematically screen papers for a Systematic Literature Review (SLR).
  Applies PRISMA-compliant title/abstract and full-text screening with documented
  inclusion/exclusion criteria. Takes literature_base.csv from Phase 1 and produces
  a filtered, auditable set of included studies with PRISMA flow diagram.
---

# Screen Papers: **$ARGUMENTS**

Activate the **screening-engine** skill. Read `skills/screening-engine/SKILL.md` in full.

Execute the complete 6-step screening workflow:

1. **DEFINE** inclusion/exclusion criteria (present for approval before screening)
2. **SCREEN** title/abstract for all papers in literature_base.csv
3. **SCREEN** full-text for included and uncertain papers
4. **ASSESS** quality of included papers (Q1-Q8 checklist)
5. **GENERATE** PRISMA flow diagram (text + visual via figure-engine)
6. **SAVE** all screening artifacts and update literature_base_screened.csv

## Input

`$ARGUMENTS` can be:
- **Empty** — screens all papers in `literature_base.csv` using default criteria
- **File path** to a specific CSV (e.g., `@literature_base_v2.csv`)
- **Criteria description** (e.g., `"only empirical papers 2020-2025 in enterprise context"`)
- **"resume"** — continue a previously started screening session

## Output

- `screening/screening_protocol.md` — documented criteria and process
- `screening/title_abstract_screening.csv` — all T/A screening decisions with reasons
- `screening/full_text_screening.csv` — full-text screening decisions
- `screening/quality_assessment.csv` — quality scores for included papers
- `screening/screening_summary.md` — PRISMA counts and summary statistics
- `literature_base_screened.csv` — final set of included papers
- `figures/fig_prisma_flow.png` — visual PRISMA diagram
