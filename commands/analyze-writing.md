---
description: >
  Analyze academic writing quality of the current draft. Checks for passive voice
  overuse, weak openings, hedging balance, readability, sentence length variation,
  and word repetitions. Produces a writing quality report with specific improvement
  suggestions per section.
---

# Analyze Writing: **$ARGUMENTS**

Activate the **writing-engine** skill. Read `skills/writing-engine/SKILL.md` in full,
then execute a **style analysis** (not a drafting task):

1. **READ** the paper (draft.md or paper.tex)
2. **ANALYZE** each section for writing quality indicators:
   - Passive voice ratio (target: <30% of sentences)
   - Weak openings ("It is important...", "There are...", "In today's world...")
   - Hedging balance (under-hedging vs. over-hedging)
   - Average sentence length and variation (target: 15-25 words, varied)
   - Word/phrase repetitions in consecutive sentences
   - Paragraph length consistency (target: 4-8 sentences per paragraph)
   - Transition quality between paragraphs
   - Citation integration style (parenthetical vs. narrative balance)
3. **SCORE** each section (Strong / Adequate / Needs Work)
4. **LIST** specific improvements with line/section references
5. **SAVE** to `writing_analysis.md`

## Input

`$ARGUMENTS` can be:
- **Empty** — analyzes the entire paper
- **Section name** (e.g., `"Introduction"`, `"Discussion"`) — analyzes one section
- **File path** to a specific file

## Output

- `writing_analysis.md` — section-by-section quality scores + specific improvement suggestions
- Each suggestion includes the problematic text and a concrete rewrite option
