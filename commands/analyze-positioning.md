---
description: >
  Analyze how the paper positions itself relative to the closest existing work.
  Identifies the 5-10 most similar papers, builds a differentiation matrix, and
  generates a positioning statement that strengthens the contribution argumentation.
---

# Analyze Positioning: **$ARGUMENTS**

Activate the **positioning-engine** skill. Read `skills/positioning-engine/SKILL.md` in full.

Execute the complete 5-step positioning analysis:

1. **IDENTIFY** the 5-10 closest competitor papers (from references + literature base)
2. **BUILD** differentiation matrix across 6-10 key dimensions
3. **ANALYZE** unique positioning, gaps, and potential reviewer challenges
4. **GENERATE** draft positioning paragraph + refined contribution statement
5. **SAVE** to `positioning_analysis.md`

## Input

`$ARGUMENTS` can be:
- **Empty** — analyzes the current draft against its own references
- **Paper references** (e.g., `"compare against Wang2024, Smith2023, Chen2024"`)
- **Aspect to focus on** (e.g., `"focus on methodological differentiation"`)

## Output

- `positioning_analysis.md` — full analysis with differentiation matrix, positioning
  assessment, draft paragraph, and refined contribution statement
- Ready-to-insert positioning paragraph for Introduction / Related Work
