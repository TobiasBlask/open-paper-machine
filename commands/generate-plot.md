---
description: Generate a statistical plot from CSV/JSON data using PaperBanana. Provide a data file and describe the visualization intent.
---

# Generate Plot: **$ARGUMENTS**

Read the figure-engine skill first.

## Steps
1. Parse `$ARGUMENTS` — extract the data file path and visualization intent
2. Read and validate the data file (CSV or JSON)
3. If PaperBanana MCP is available: call `paperbanana_generate_plot`
4. If not: generate using Python (matplotlib/seaborn) as fallback with academic styling
5. Save output PNG to `figures/` in the workspace (300 DPI, tight layout)
6. Provide the LaTeX `\begin{figure}` snippet ready for inclusion
7. Show the user the generated figure
