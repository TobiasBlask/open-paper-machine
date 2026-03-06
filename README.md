# Open Academic Paper Machine

> A Claude Code plugin that autonomously writes academic papers — from literature search to production-ready LaTeX/PDF.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Plugin Version](https://img.shields.io/badge/plugin-v5.4.0-green)]()
[![Template](https://img.shields.io/badge/template-arxiv--style-orange)](https://github.com/kourgeorge/arxiv-style)

## Quick Start

```bash
# 1. Install the plugin
/plugin marketplace add TobiasBlask/open-paper-machine
/plugin install open-academic-paper-machine@open-paper-machine

# 2. Install dependencies
pip install paperbanana[mcp,google] academic-search-mcp

# 3. Set up your API key (free — https://aistudio.google.com/apikey)
echo 'GOOGLE_API_KEY="your-key"' > .env

# 4. Go
/write-paper The impact of generative AI on organizational decision-making
```

That's it. The plugin ships both MCP servers (`academic-search` and `paperbanana`), all 8 skill engines, 8 slash commands, and the autonomous pipeline agent. Everything starts automatically.

**Technical paper:** [The Open Academic Paper Machine: An Autonomous LLM Plugin for End-to-End Academic Paper Production](paper/paper.pdf) (Blask, 2026) — describes the system architecture, design principles, and evaluation. LaTeX source in [`paper/`](paper/).

**Position paper:** [From Creator to Orchestrator? How an LLM Agent Wrote This Paper and What That Means for Science](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6358578) (Blask & Funk, 2026) — a position paper on AI-augmented knowledge production, orchestrated through human-AI interaction using this system. [GitHub repo](https://github.com/TobiasBlask/From_Creator_to_Orchestrator).

---

## How It Works

<p align="center">
  <img src="paper/figures/fig2_pipeline_flow.png" alt="Pipeline Flow" width="700">
</p>

The machine runs autonomously through **8 phases**:

| Phase | What Happens | Your Job |
|-------|-------------|----------|
| **1. Reconnaissance** | 4-6 search queries across 4 academic APIs, snowballing, deduplication | Check scope, redirect if needed |
| **2. Framing** | Theory selection, gap formulation, research questions, contribution statement | Confirm direction |
| **3. Structure** | Concept matrix, paper structure, word budget | Approve structure |
| **4. Production** | Write every section as complete paragraphs + generate figures | Read along, adjust |
| **5. Assembly** | Compile all sections, quality self-assessment, status report | Start review |
| **6. LaTeX & PDF** | Convert to arxiv-style LaTeX, resolve citations, compile PDF | Download and submit |
| **7. Verification** *(opt.)* | Fetch source abstracts/PDFs, verify each citation claim | Review flagged mismatches |
| **8. Revision** *(repeatable)* | Extract reviewer/co-author feedback, classify, implement changes, recompile + latexdiff | Approve change plan |

**Core principle:** The machine makes decisions and presents results. You steer at checkpoints.

Phase 8 closes the loop: send an annotated PDF from your co-author or paste reviewer comments, and the review-engine extracts, classifies, and implements all changes — then recompiles and generates a visual diff. The cycle repeats (Round 1 → 2 → 3 → ...) until acceptance.

---

## Installation

### What Gets Installed

The plugin bundles two MCP servers that start automatically:

| MCP Server | pip package | What it does |
|---|---|---|
| `academic-search` | [`academic-search-mcp`](https://pypi.org/project/academic-search-mcp/) | Searches Semantic Scholar, OpenAlex, CrossRef, arXiv. Snowballing, BibTeX/CSV export. |
| `paperbanana` | [`paperbanana`](https://pypi.org/project/paperbanana/) | AI figure generation via Google Gemini. Multi-agent pipeline with iterative refinement. Based on [Zhu et al. (2026)](https://arxiv.org/abs/2601.23265). |

Both are configured in `plugin.json` and start when Claude Code loads the plugin. No manual MCP setup needed.

> **Academic foundation:** The figure generation pipeline implements the methodology from [PaperBanana: Automating Academic Illustration for AI Scientists](https://arxiv.org/abs/2601.23265) (Zhu et al., 2026). The MCP integration uses the community implementation at [`llmsresearch/paperbanana`](https://github.com/llmsresearch/paperbanana). See also the [official research repo](https://github.com/dwzhu-pku/PaperBanana).

### Step-by-Step

**1. Add the marketplace and install the plugin:**

```bash
/plugin marketplace add TobiasBlask/open-paper-machine
/plugin install open-academic-paper-machine@open-paper-machine
```

**2. Install Python dependencies:**

```bash
pip install paperbanana[mcp,google] academic-search-mcp
```

**3. Configure your Google API key** (needed for AI figure generation):

Get a free key at [Google AI Studio](https://aistudio.google.com/apikey), then create a `.env` file in your **project root** (where you run Claude Code):

```bash
GOOGLE_API_KEY="your-api-key-here"
```

The PaperBanana MCP server loads `.env` automatically on startup. Never commit `.env` to version control. See `.env.example` for a template.

**4. Install LaTeX** (for PDF compilation):

```bash
# macOS
brew install --cask mactex-no-gui

# Ubuntu/Debian
sudo apt-get install texlive-full
```

**5. Start writing:**

```bash
/write-paper Your Paper Title Here
```

### Cowork Setup

1. Download this repo as ZIP
2. Upload via Plugins panel ("+" button)
3. Set `GOOGLE_API_KEY` in plugin settings (optional — only needed for AI figures)
4. `/write-paper Your Paper Title`

---

## Commands

| Command | Description |
|---------|-------------|
| `/write-paper [title]` | **Full pipeline** — all 8 phases, start to finish |
| `/export-latex` | Convert finished draft to arxiv-style LaTeX + compiled PDF |
| `/search-papers [topic]` | Phase 1 only: systematic literature search across 4 APIs |
| `/draft-section [section]` | Write one specific section as complete paragraphs |
| `/respond-reviewers [pdf or comments]` | **Full revision loop** — extract feedback, classify, implement, recompile, latexdiff |
| `/generate-figure [description]` | AI-generated academic diagram from text |
| `/generate-plot [datafile] [intent]` | Statistical plot from CSV/JSON data |
| `/verify-citations` | **Verify all citations** against actual source content |

---

## Architecture

<p align="center">
  <img src="paper/figures/fig1_system_architecture.png" alt="System Architecture" width="700">
</p>

### Skill Engines

The plugin contains 8 specialized skill engines that the paper-machine agent orchestrates:

| Engine | Responsibility | Key Capabilities |
|--------|---------------|-----------------|
| **writing-engine** | Paragraph-level text production | Section templates, sentence formulas, academic register for IS/WI/BWL |
| **literature-engine** | Systematic literature discovery | 4 academic APIs, snowballing, PRISMA screening, concept matrix |
| **theory-engine** | Theoretical framing | Theory matching, gap formulation, hypothesis/design principle derivation |
| **method-engine** | Research design | SLR, case study, Gioia, Mayring, grounded theory, PLS-SEM, DSR templates |
| **figure-engine** | Visual production | PaperBanana AI diagrams (Gemini) with matplotlib/seaborn fallback |
| **latex-engine** | Document compilation | arxiv-style conversion, `\citep`/`\citet` citation resolution, PDF build |
| **verification-engine** | Citation verification | Source retrieval (abstract + full-text), claim-source comparison, verification report |
| **review-engine** | Revision automation | PDF annotation extraction, comment classification, change planning, latexdiff generation |

### MCP Servers (Bundled)

<p align="center">
  <img src="paper/figures/fig3_mcp_integration.png" alt="MCP Integration" width="700">
</p>

Both servers are declared in `plugin.json` and start automatically with the plugin:

| Server | Package | APIs | Purpose |
|--------|---------|------|---------|
| `academic-search` | `academic-search-mcp` | Semantic Scholar, OpenAlex, CrossRef, arXiv | Literature search, snowballing, multi-query, BibTeX/CSV export |
| `paperbanana` | `paperbanana[mcp,google]` | Google Gemini | AI diagram generation, statistical plots, diagram evaluation |

### Pipeline Agent

The `paper-machine` agent (`agents/paper-machine.md`) is an autonomous agent prompt that orchestrates all 8 skill engines through the pipeline phases. Operating principles:

1. **DO, don't ask.** Make decisions and present results.
2. **Produce text, not plans.** Every phase yields deliverable output.
3. **Checkpoint, don't block.** Present work, then continue.
4. **Be explicit about decisions.** State what was chosen and why.
5. **Save everything to files.** Every phase produces artifacts.

### Markdown-to-LaTeX Converter

`scripts/md_to_latex.py` (733 lines) converts the draft into production-ready LaTeX:

- `(Author, Year)` citations to `\citep{key}` / `\citet{key}` with BibTeX key matching
- Markdown tables to `booktabs` LaTeX tables
- Markdown images to LaTeX figure environments
- Section hierarchy mapping (`#` to `\section`, `##` to `\subsection`, etc.)
- Abstract and keyword extraction
- `[CITE]`, `[DATA]`, `[TODO]` markers to LaTeX comments

```bash
# Standalone usage
python scripts/md_to_latex.py draft.md references.bib --output paper.tex --compile
```

---

## Output Files

After `/write-paper` + `/export-latex`, your project directory contains:

| File | Description |
|------|-------------|
| `draft.md` | Complete paper draft with all sections |
| `references.bib` | BibTeX entries for all cited papers |
| `literature_base.csv` | Full literature database from search phase |
| `concept_matrix.md` | Webster & Watson concept matrix |
| `framing.md` | Theoretical framing (gap, RQs, contribution) |
| `paper_structure.md` | Paper structure with word budget |
| `figures/` | Generated diagrams and plots (PNG, 300 DPI) |
| `status_report.md` | Completion status and open items |
| `latex/paper.tex` | arxiv-style LaTeX source |
| `latex/paper.pdf` | Compiled PDF, ready for submission |
| `verification_report.md` | Citation verification results *(after `/verify-citations`)* |
| `latex/paper_diff.pdf` | Visual change tracking via latexdiff *(after `/respond-reviewers`)* |
| `orchestration_log.md` | Audit trail: timestamps, actors, decisions, quality gate outcomes *(v5.2.0+)* |
| `outputs/revision_log_rN.md` | Detailed change log per revision round *(after `/respond-reviewers`)* |

---

## Repository Structure

```
.
├── .claude-plugin/
│   ├── plugin.json             # Plugin manifest + MCP server config
│   └── marketplace.json        # Marketplace definition for install
├── agents/
│   └── paper-machine.md        # Autonomous 6-phase pipeline agent (~3,200 lines)
├── commands/
│   ├── write-paper.md          # Full pipeline command
│   ├── export-latex.md         # LaTeX export command
│   ├── search-papers.md        # Literature search command
│   ├── draft-section.md        # Single section drafting
│   ├── generate-figure.md      # AI figure generation
│   ├── generate-plot.md        # Statistical plot generation
│   ├── respond-reviewers.md    # R&R response drafting
│   └── verify-citations.md    # Citation verification command
├── skills/
│   ├── writing-engine/         # Academic writing templates
│   ├── literature-engine/      # Systematic literature search
│   ├── theory-engine/          # Theoretical framing
│   ├── method-engine/          # Research methodology
│   ├── figure-engine/          # Figure generation (PaperBanana)
│   ├── latex-engine/           # LaTeX conversion + compilation
│   ├── verification-engine/   # Citation verification against sources
│   └── review-engine/         # Revision automation (PDF annotation → implement → latexdiff)
├── scripts/
│   ├── md_to_latex.py          # Markdown-to-LaTeX converter (733 lines)
│   └── extract_annotations.py  # PDF annotation extraction (PyMuPDF)
├── templates/
│   └── arxiv.sty               # arxiv-style LaTeX template
├── paper/                          # Technical paper (Blask, 2026)
│   ├── paper.tex               # LaTeX source
│   ├── paper.pdf               # Compiled PDF
│   ├── references.bib          # Bibliography
│   └── figures/                # PaperBanana-generated diagrams
├── .env.example                # API key template
├── .gitignore
├── LICENSE
└── README.md
```

---

## Figure Generation

PaperBanana implements the multi-agent pipeline from [Zhu et al. (2026)](https://arxiv.org/abs/2601.23265), powered by Google Gemini:

```
Retriever → Planner → Stylist → Visualizer → Critic (×3 iterations) → Final PNG
```

The 5-agent, 2-phase architecture uses in-context learning with curated reference examples (Phase 1: planning) and iterative VLM-as-Judge refinement (Phase 2: generation). The MCP server starts automatically when Claude Code loads the plugin and reads `GOOGLE_API_KEY` from `.env` in your project directory.

| Environment | Engine | Quality |
|---|---|---|
| Claude Code | PaperBanana + Gemini | AI-generated, publication-quality |
| Cowork | matplotlib / seaborn | Clean statistical plots |

If PaperBanana is unavailable (no API key, network issues), the figure-engine falls back to Python-based generation using matplotlib and seaborn with academic styling presets.

> **References:** [Official research repo](https://github.com/dwzhu-pku/PaperBanana) · [Community MCP implementation](https://github.com/llmsresearch/paperbanana) · [arXiv:2601.23265](https://arxiv.org/abs/2601.23265)

---

## Citation Verification

The verification-engine checks whether cited papers actually support the claims attributed to them:

```bash
/verify-citations
```

**How it works:**
1. Extracts all `\citep{}`/`\citet{}` citations from `paper.tex` (or `(Author, Year)` from `draft.md`) with surrounding context
2. Matches to BibTeX entries and DOIs in `references.bib`
3. Fetches source material via academic-search MCP:
   - **Tier A:** Abstracts + TLDRs from Semantic Scholar, OpenAlex, CrossRef (always)
   - **Tier B:** Full-text PDFs for open-access papers — arXiv, DOAJ, etc. (when available)
4. Compares each attributed claim against actual source content
5. Classifies as: VERIFIED, PLAUSIBLE, MISMATCH, UNVERIFIABLE, or NOT FOUND
6. Generates `verification_report.md` with priority issues and fix recommendations

**Prioritized processing:** Load-bearing citations (gap statement, key statistics) are verified first, then methodology/theory citations, then background references. Results after each tier so you can act on critical mismatches immediately.

---

## Revision Automation (Phase 8)

The review-engine automates the co-author/reviewer revision loop — derived from 4 actual revision rounds on the paper that built this tool:

```bash
/respond-reviewers @annotated_review.pdf
```

**How it works:**

```
📄 Annotated PDF ──→ EXTRACT ──→ MAP ──→ CLASSIFY ──→ PLAN (Quality Gate)
                                                            │
                                              IMPLEMENT ──→ VERIFY ──→ DOCUMENT
                                                                         │
                     New Round ◄─────────────────────────────────────────┘
```

1. **EXTRACT** — Parses PDF annotations (highlights, sticky notes, strikeouts) via PyMuPDF, or parses pasted reviewer comments
2. **MAP** — Locates each comment's corresponding position in `paper.tex` (line number, section, context)
3. **CLASSIFY** — Determines action type (DELETE, REPLACE, MOVE, RESTRUCTURE, FIX, FIGURE, SHORTEN, APPROVE, QUESTION) and priority
4. **PLAN** — Presents a structured change plan table for your approval (**quality gate** — nothing executes without your OK)
5. **IMPLEMENT** — Executes changes in dependency order, invoking figure-engine or writing-engine as needed
6. **VERIFY** — Recompiles LaTeX (0 errors target), generates `latexdiff` for visual change tracking
7. **DOCUMENT** — Creates change log, optional R&R letter, updates orchestration log, commits

**Supports:** Co-author annotated PDFs, journal R&R decision letters, self-review output. Handles multilingual comments (German/English). Repeats for Round 1 → 2 → 3 → ... until acceptance.

---

## Supported Research Methods

The method-engine provides complete section templates for:

- **Systematic Literature Review (SLR)** — PRISMA flow, inclusion/exclusion criteria
- **Case Study** — Yin methodology, cross-case analysis
- **Gioia Method** — 1st/2nd order coding, aggregate dimensions
- **Mayring Content Analysis** — Category system, coding rules
- **Grounded Theory** — Open/axial/selective coding
- **PLS-SEM** — Measurement model, structural model
- **Design Science Research (DSR)** — Hevner framework, evaluation cycles
- **Mixed Methods** — Sequential/concurrent designs

---

## Citation

If you use this tool in your research, please cite the technical paper:

```bibtex
@article{blask2026opm,
  title={The Open Academic Paper Machine: An Autonomous {LLM} Plugin for
         End-to-End Academic Paper Production},
  author={Blask, Tobias-Benedikt},
  year={2026},
  note={Working paper}
}
```

The position paper (orchestrated through human-AI interaction using this system):

```bibtex
@article{blask2026creator,
  title={From Creator to Orchestrator? How an {LLM} Agent Wrote This Paper
         and What That Means for Science},
  author={Blask, Tobias-Benedikt and Funk, Burkhardt},
  journal={SSRN Electronic Journal},
  year={2026},
  note={Available at \url{https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6358578}}
}
```

The figure generation pipeline is based on:

```bibtex
@article{zhu2026paperbanana,
  title={PaperBanana: Automating Academic Illustration for {AI} Scientists},
  author={Zhu, Dawei and Meng, Rui and Song, Yale and Wei, Xiyu and Li, Sujian
          and Pfister, Tomas and Yoon, Jinsung},
  journal={arXiv preprint arXiv:2601.23265},
  year={2026}
}
```

---

## License

MIT License. See [LICENSE](LICENSE) for details.

**Author:** Prof. Dr. Tobias-Benedikt Blask — [Harz University of Applied Sciences](https://www.hs-harz.de)
