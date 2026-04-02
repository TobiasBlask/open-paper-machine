---
description: >
  Scooping risk assessment — is someone else working on your research idea? Identifies
  competing groups, assesses pace of publication, evaluates whether the core insight is
  "in the air", and provides a watch list with search terms, key researchers, and venues
  to monitor.
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
  - mcp__academic-search__academic_search_openalex
  - mcp__academic-search__academic_snowball
user_invocable: true
---

# /scooping-check — Is Someone Else Working on This?

Read `agents/research-strategist.md` and execute **Mode 5: Scooping Risk Assessment**.

The user provides a research idea or topic. Assess:
- Number of capable and motivated groups working on similar problems
- Pace of recent publication in this area (search academic databases)
- Whether the core insight is "in the air" (multiple independent discoveries likely)
- Time to completion for the user vs. competitors

Provide:
1. **Risk level**: Low / Medium / High scooping risk
2. **Competing groups**: Names, affiliations, recent publications
3. **Mitigation strategies**: How to differentiate, accelerate, or pivot
4. **Watch list**:
   - Search terms to monitor
   - Key researchers to track
   - Key venues where competing work would appear
   - Recommended review frequency (weekly/monthly)

Use academic search tools to ground the assessment in actual recent publications and preprints.

**$ARGUMENTS**
