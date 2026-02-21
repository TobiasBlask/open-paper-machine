---
description: Generate an academic diagram from a text description using PaperBanana. Provide a section of your paper or a methodology description and get a publication-quality figure.
---

# Generate Figure: **$ARGUMENTS**

Read the figure-engine skill first.

## Steps
1. Parse `$ARGUMENTS` — extract the source text or file reference and optional caption
2. If a file path is given, read it. If inline text, use it directly.
3. Write the source context to a temp file
4. If PaperBanana MCP is available: call `paperbanana_generate_diagram`
5. If not: generate using Python (matplotlib + graphviz/networkx) as fallback
6. Save output PNG to `figures/` in the workspace
7. Provide the LaTeX `\begin{figure}` snippet ready for inclusion
8. Show the user the generated figure
