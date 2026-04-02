---
description: >
  Creative research brainstorming — generate ideas researchers within a single field
  would miss. Cross-field connections, assumption challenges, alternative framings,
  and wild cards. Produces bold, specific, surprising ideas rather than safe incremental ones.
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

# /brainstorm — Creative Research Idea Generation

Read `agents/brainstormer.md` and execute a brainstorming session for the given topic.

The user provides a research topic, problem space, or question. Generate:
- Nugget candidates (2-3 one-sentence key insight attempts)
- Cross-field connections (specific structural analogies, not vague)
- Assumptions worth challenging (what everyone assumes but might be wrong)
- Alternative framings (different ways to view the problem)
- Big ideas with feasibility/novelty assessment
- Wild cards (labeled speculative)
- The skeptical reader test (ideal reader, hook, current weakness)

**$ARGUMENTS**
