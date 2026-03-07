---
description: >
  Prepare a paper for submission to a specific venue. Runs anonymization checks
  for double-blind review, generates a cover letter, identifies suggested reviewers,
  validates venue-specific formatting, and produces a complete submission checklist.
  Creates a submission-ready package.
---

# Prepare Submission: **$ARGUMENTS**

Activate the **submission-engine** skill. Read `skills/submission-engine/SKILL.md` in full.

Execute the complete 7-step submission preparation workflow:

1. **IDENTIFY** target venue and load formatting requirements
2. **CHECK** anonymization for double-blind review (self-citations, author names, metadata)
3. **GENERATE** cover letter tailored to the venue
4. **SUGGEST** reviewers based on the paper's reference list
5. **VALIDATE** formatting against venue requirements (pages, abstract, references)
6. **CREATE** submission checklist
7. **COMPILE** complete submission package

## Input

`$ARGUMENTS` should specify:
- **Venue name** (e.g., `ICIS 2026`, `MISQ`, `ECIS`, `BISE`)
- Optional: **track name** (e.g., `"ICIS 2026 Human-AI Interaction track"`)
- Optional: **"R&R"** to generate a revision cover letter instead

## Output

- `submission/paper_anonymous.pdf` — anonymized manuscript
- `submission/cover_letter.md` — venue-specific cover letter
- `submission/suggested_reviewers.md` — 3-5 reviewer suggestions with justification
- `submission/anonymization_report.md` — detailed anonymization check results
- `submission/formatting_report.md` — formatting validation results
- `submission/submission_checklist.md` — comprehensive checklist for the venue
