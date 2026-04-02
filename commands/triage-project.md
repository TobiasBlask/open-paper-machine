---
description: >
  Strategic project triage — should you continue, pivot, or kill your current research
  project? Evaluates 5 signals (results, competition, impact, effort, motivation) and
  delivers a clear Continue/Pivot/Kill recommendation. For Pivot: suggests concrete new
  framing. For Kill: suggests what to salvage.
allowed_tools:
  - Agent
  - Read
  - Write
  - Glob
  - Grep
  - Bash
  - WebSearch
  - WebFetch
  - mcp__academic-search__academic_search_all
  - mcp__academic-search__academic_search_semantic_scholar
  - mcp__academic-search__academic_search_arxiv
user_invocable: true
---

# /triage-project — Should You Continue This Project?

Read `agents/research-strategist.md` and execute **Mode 1: Project Triage**.

The user describes their current research project and its state. Evaluate using 5 signals:

| Signal | Continue | Pivot | Kill |
|--------|----------|-------|------|
| Results | Core hypothesis validated | Interesting side results | Core assumption disproven |
| Competition | Still ahead or unique angle | Others approaching differently | Scooped on main contribution |
| Impact | Conclusion-first test passes | Original framing weak, results support different framing | Can't write compelling conclusion |
| Effort remaining | Manageable, clear path | Moderate, toward a different goal | Large, success still uncertain |
| Motivation | Engaged, believes in the work | Curious about pivot direction | Dreading the work |

Deliver a clear **Continue / Pivot / Kill** verdict with reasoning.
- For **Pivot**: suggest a concrete new framing — not just "consider pivoting."
- For **Kill**: suggest what to salvage (workshop paper, blog post, dataset release).

Always flag the sunk cost fallacy explicitly. Respect the work done, then recommend based on forward-looking expected value only.

**$ARGUMENTS**
