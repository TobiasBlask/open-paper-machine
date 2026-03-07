---
description: >
  Generate conference presentation slides from a completed paper. Extracts key
  content, builds a slide structure, generates content with speaker notes, and
  produces a Marp-compatible markdown slide deck.
---

# Generate Slides: **$ARGUMENTS**

Activate the **presentation-engine** skill. Read `skills/presentation-engine/SKILL.md` in full.

Execute the complete 5-step presentation workflow:

1. **EXTRACT** key content from each paper section
2. **DESIGN** slide structure (15-18 slides for conference, 10-12 for short talk)
3. **GENERATE** slide content with speaker notes for every slide
4. **INTEGRATE** figures from `figures/` directory where appropriate
5. **SAVE** to `presentation/presentation.md` + `presentation/speaker_notes.md`

## Input

`$ARGUMENTS` can be:
- **Empty** — generates a standard 15-18 slide conference presentation
- **Format** (e.g., `"short talk"`, `"workshop"`, `"seminar"`, `"poster"`)
- **Time constraint** (e.g., `"10 minutes"`, `"20 minutes"`, `"45 minutes"`)
- **Venue** (e.g., `"ICIS 2026"`) — adapts to venue presentation norms

## Output

- `presentation/presentation.md` — Marp-compatible slide deck with speaker notes
- `presentation/speaker_notes.md` — standalone speaker notes for rehearsal
- `presentation/slide_outline.md` — quick reference outline
- Render with: `marp presentation/presentation.md --pdf`
