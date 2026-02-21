---
name: figure-engine
description: >
  Activate when the user needs to generate, refine, or evaluate academic figures,
  diagrams, or statistical plots. Uses PaperBanana (paperbanana MCP server) to
  transform text descriptions or data files into publication-quality illustrations.
  Supports methodology diagrams, statistical plots, and comparative evaluation.
---

# Figure Engine

## Core Principle
Academic papers need professional figures. This skill eliminates manual design work
by using PaperBanana to generate publication-quality diagrams and plots from text
descriptions or data files. Claude should produce ACTUAL FIGURES, not describe what
to draw.

## Prerequisites

The **paperbanana MCP server** must be running. It requires:
- `pip install paperbanana[mcp,google]`
- A `GOOGLE_API_KEY` in a `.env` file in the project root (get a free key at https://aistudio.google.com/apikey)

The MCP server is configured in `plugin.json` and starts automatically. It loads the Google API key from `.env` in the project's working directory.

If the MCP server is NOT available, fall back to generating figures with Python
(matplotlib, seaborn, plotly) directly.

---

## When the User Says "Make Me a Figure" — What to Do

1. **Determine figure type**: diagram (methodology, framework, process) or plot (bar, line, scatter, etc.)
2. **Gather input**: text description for diagrams, data file for plots
3. **Generate using PaperBanana MCP tools** if available, otherwise Python fallback
4. **Save to figures/ directory** in the working folder
5. **Provide LaTeX include snippet** ready for copy-paste

---

## Tool 1: Generate Diagram

**Use for:** Methodology overviews, theoretical frameworks, process flows,
architecture diagrams, research design figures.

**MCP Tool:** `paperbanana_generate_diagram` (if paperbanana MCP is connected)

**Workflow:**
1. Write the source context to a temporary .txt file (the methodology description,
   framework explanation, or process narrative)
2. Call the MCP tool with the file path and a caption
3. Save the resulting PNG to `figures/`
4. Return LaTeX snippet:
   ```latex
   \begin{figure}[htbp]
   \centering
   \includegraphics[width=\linewidth]{figures/filename.png}
   \caption{Your caption here}
   \label{fig:label}
   \end{figure}
   ```

**Fallback (no MCP):** Use Python with matplotlib + networkx or graphviz to generate
the diagram programmatically.

### Diagram Prompting Guide

Good source context for PaperBanana includes:
- **What the diagram shows**: "This figure illustrates the three-phase research design"
- **Key components**: "Phase 1: Literature Search, Phase 2: Screening, Phase 3: Analysis"
- **Relationships**: "Phase 1 feeds into Phase 2, which filters down to Phase 3"
- **Style hints**: "PRISMA-style flow diagram" or "layered architecture diagram"

Example:
```
Source: "The research follows a systematic literature review methodology with three
stages: (1) database search across Scopus, Web of Science, IEEE Xplore, and AIS
eLibrary using predefined search strings, (2) two-stage screening with title/abstract
review followed by full-text assessment against inclusion/exclusion criteria, and
(3) thematic synthesis using a concept matrix approach."

Caption: "Systematic Literature Review Process"
```

---

## Tool 2: Generate Plot

**Use for:** Bar charts, line charts, scatter plots, heatmaps, box plots,
distribution plots — any statistical visualization from data.

**MCP Tool:** `paperbanana_generate_plot` (if paperbanana MCP is connected)

**Workflow:**
1. Prepare data as CSV or JSON file
2. Call the MCP tool with the data file path and an intent description
3. Save the resulting PNG to `figures/`
4. Return LaTeX snippet

**Intent examples:**
- "Bar chart comparing adoption rates across industries"
- "Timeline showing publication counts by year"
- "Heatmap of technology capability vs. organizational maturity"
- "Stacked bar chart of implementation challenges by category"

**Fallback (no MCP):** Use Python with matplotlib/seaborn:
```python
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import seaborn as sns

# Set academic style
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams.update({
    'font.family': 'serif',
    'font.size': 11,
    'axes.titlesize': 13,
    'axes.labelsize': 12,
    'figure.figsize': (10, 6),
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox_inches': 'tight',
})
```

---

## Tool 3: Evaluate Diagram

**Use for:** Quality checking a generated figure against a reference or expected output.

**MCP Tool:** `paperbanana_evaluate_diagram` (if paperbanana MCP is connected)

**Workflow:**
1. Provide the generated image path and a reference image path
2. The tool returns a quality score and improvement suggestions
3. If score is low, re-generate with refined input

---

## Academic Figure Standards

### General Rules
- **Resolution:** Minimum 300 DPI for print
- **Width:** Match journal column width (single column ~8.5cm, double column ~17.5cm)
- **Font:** Serif fonts (Times, Computer Modern) matching paper body
- **Colors:** Use colorblind-friendly palettes (e.g., Okabe-Ito, viridis)
- **Labels:** All axes labeled with units, legend if multiple series
- **Caption:** Descriptive, can stand alone without reading the text

### LaTeX Integration
Always provide the complete figure environment:
```latex
\begin{figure}[htbp]
\centering
\includegraphics[width=\linewidth]{figures/FILENAME.png}
\caption{DESCRIPTIVE CAPTION}
\label{fig:SHORT_LABEL}
\end{figure}
```

For side-by-side figures:
```latex
\begin{figure}[htbp]
\centering
\begin{minipage}{0.48\textwidth}
  \centering
  \includegraphics[width=\linewidth]{figures/LEFT.png}
  \caption{Left caption}
  \label{fig:left}
\end{minipage}
\hfill
\begin{minipage}{0.48\textwidth}
  \centering
  \includegraphics[width=\linewidth]{figures/RIGHT.png}
  \caption{Right caption}
  \label{fig:right}
\end{minipage}
\end{figure}
```

### File Naming Convention
`fig_SECTION_DESCRIPTION.png`
- `fig_method_prisma_flow.png`
- `fig_results_adoption_by_year.png`
- `fig_framework_sociotechnical.png`

---

## Integration with Paper Machine

When used inside the `/write-paper` pipeline (Phase 4: Production), the figure-engine
should be called automatically for sections that need visual support:

| Section | Typical Figures |
|---------|----------------|
| Methodology | Research design overview, PRISMA flow, sampling diagram |
| Results | Distribution plots, frequency charts, concept maps |
| Discussion | Framework diagram, comparison matrix, implications model |

The writing-engine should reference generated figures with `\ref{fig:label}` in the text.
