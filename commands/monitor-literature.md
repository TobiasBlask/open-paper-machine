---
description: >
  Re-run literature search queries to find newly published papers since the last
  search. Compares new results against the existing literature_base.csv and
  highlights papers that appeared after the initial search date.
---

# Monitor Literature: **$ARGUMENTS**

Activate the **literature-engine** skill. Read `skills/literature-engine/SKILL.md` in full.

Execute a monitoring search:

1. **LOAD** the original search queries from `literature_base.csv` metadata or `framing.md`
2. **RE-RUN** all queries with `date_from` set to the last search date
3. **DEDUPLICATE** against existing `literature_base.csv`
4. **PRESENT** only NEW papers not in the current literature base
5. **OFFER** to add relevant new papers to `literature_base.csv` and `references.bib`

## Input

`$ARGUMENTS` can be:
- **Empty** — re-runs all original queries, shows papers since last search
- **Specific query** (e.g., `"generative AI agents 2025"`) — runs a targeted update search
- **"since YYYY-MM-DD"** — overrides the date filter

## Output

- Summary of newly found papers (count, titles, venues)
- Updated `literature_base.csv` (if user approves additions)
- Updated `references.bib` (if user approves additions)
