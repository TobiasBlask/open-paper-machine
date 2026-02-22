---
description: Verify all citations by fetching source abstracts/full-text and checking claims against actual content
---

# Verify Citations: **$ARGUMENTS**

Activate the **verification-engine** skill. Read `skills/verification-engine/SKILL.md` in full.

Execute the complete 5-step verification workflow:
1. Extract all citation claims from paper.tex (or draft.md)
2. Match to BibTeX entries and DOIs
3. Fetch source abstracts (Tier A) and full text for open-access papers (Tier B)
4. Verify each claim against source content
5. Generate `verification_report.md`

If $ARGUMENTS specifies a scope (e.g., "tier 1 only", "Section 2", "just the hallucination section"), verify only that scope. Otherwise verify the entire paper, processing Tier 1 (load-bearing) citations first.
