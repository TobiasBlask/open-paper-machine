# Open Academic Paper Machine

> A Claude Code plugin that autonomously writes academic papers — from literature search to production-ready LaTeX/PDF.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Plugin Version](https://img.shields.io/badge/plugin-v5.0.0-green)]()
[![Template](https://img.shields.io/badge/template-arxiv--style-orange)](https://github.com/kourgeorge/arxiv-style)

Give it a title, topic, or research question. The agent runs the complete pipeline — from literature search to compiled PDF — with you steering at checkpoints.

```
/write-paper The impact of generative AI on organizational decision-making:
  A systematic literature review
```

**Paper that built this tool:** [From Creator to Orchestrator](https://github.com/ProfDrT/From_Creator_to_Orchestrator) — a self-referential paper written entirely by this system.

---

## How It Works

The machine runs autonomously through **6 phases**:

| Phase | What Happens | Your Job |
|-------|-------------|----------|
| **1. Reconnaissance** | 4-6 search queries across 4 academic APIs, snowballing, deduplication | Check scope, redirect if needed |
| **2. Framing** | Theory selection, gap formulation, research questions, contribution statement | Confirm direction |
| **3. Architecture** | Concept matrix, paper structure, word budget | Approve structure |
| **4. Production** | Write every section as complete paragraphs + generate figures | Read along, adjust |
| **5. Assembly** | Compile all sections, quality self-assessment, status report | Start review |
| **6. LaTeX & PDF** | Convert to arxiv-style LaTeX, resolve citations, compile PDF | Download and submit |

**Core principle:** The machine makes decisions and presents results. You steer at checkpoints.

---

## Installation

### Prerequisites

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) or Cowork
- Python 3.10+ (for PaperBanana figure generation)
- LaTeX distribution (for PDF compilation)

### Step 1: Install the Plugin

Install via the Claude Code plugin manager, or clone this repository into your plugins directory.

### Step 2: Install PaperBanana (Figure Generation)

```bash
pip install paperbanana[mcp,google]
```

### Step 3: Configure API Key

PaperBanana uses Google Gemini for AI figure generation. Get a free API key:

1. Go to [Google AI Studio](https://aistudio.google.com/apikey)
2. Create a new API key
3. Create a `.env` file **in your project root** (where you run Claude Code):

```bash
# .env
GOOGLE_API_KEY="your-api-key-here"
```

> **Important:** The `.env` file must be in your project's working directory. The PaperBanana MCP server loads it automatically on startup. Never commit `.env` to version control.

See `.env.example` for a template.

### Step 4: Install LaTeX

```bash
# macOS
brew install --cask mactex-no-gui

# Ubuntu/Debian
sudo apt-get install texlive-full

# Arch
sudo pacman -S texlive-most
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
| `/write-paper [title]` | **Full pipeline** — all 6 phases, start to finish |
| `/export-latex` | Convert finished draft to arxiv-style LaTeX + compiled PDF |
| `/search-papers [topic]` | Phase 1 only: systematic literature search across 4 APIs |
| `/draft-section [section]` | Write one specific section as complete paragraphs |
| `/respond-reviewers` | Draft point-by-point R&R response letter |
| `/generate-figure [description]` | AI-generated academic diagram from text |
| `/generate-plot [datafile] [intent]` | Statistical plot from CSV/JSON data |

---

## Architecture

### Skill Engines

The plugin contains 6 specialized skill engines that the paper-machine agent orchestrates:

| Engine | Responsibility | Key Capabilities |
|--------|---------------|-----------------|
| **writing-engine** | Paragraph-level text production | Section templates, sentence formulas, academic register for IS/WI/BWL |
| **literature-engine** | Systematic literature discovery | 4 academic APIs, snowballing, PRISMA screening, concept matrix |
| **theory-engine** | Theoretical framing | Theory matching, gap formulation, hypothesis/design principle derivation |
| **method-engine** | Research design | SLR, case study, Gioia, Mayring, grounded theory, PLS-SEM, DSR templates |
| **figure-engine** | Visual production | PaperBanana AI diagrams (Gemini) with matplotlib/seaborn fallback |
| **latex-engine** | Document compilation | arxiv-style conversion, `\citep`/`\citet` citation resolution, PDF build |

### MCP Servers

| Server | APIs | Purpose |
|--------|------|---------|
| `academic-search` | Semantic Scholar, OpenAlex, CrossRef, arXiv | Literature search, snowballing, BibTeX/CSV export |
| `paperbanana` | Google Gemini | AI diagram generation, statistical plots, diagram evaluation |

### Pipeline Agent

The `paper-machine` agent (`agents/paper-machine.md`) is a ~3,200-line autonomous agent prompt that orchestrates all 6 skill engines through the pipeline phases. Operating principles:

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
| `paper_structure.md` | Paper architecture with word budget |
| `figures/` | Generated diagrams and plots (PNG, 300 DPI) |
| `status_report.md` | Completion status and open items |
| `latex/paper.tex` | arxiv-style LaTeX source |
| `latex/paper.pdf` | Compiled PDF, ready for submission |

---

## Repository Structure

```
.
├── .claude-plugin/
│   └── plugin.json             # Plugin manifest + MCP server config
├── agents/
│   └── paper-machine.md        # Autonomous 6-phase pipeline agent
├── commands/
│   ├── write-paper.md          # Full pipeline command
│   ├── export-latex.md         # LaTeX export command
│   ├── search-papers.md        # Literature search command
│   ├── draft-section.md        # Single section drafting
│   ├── generate-figure.md      # AI figure generation
│   ├── generate-plot.md        # Statistical plot generation
│   └── respond-reviewers.md    # R&R response drafting
├── skills/
│   ├── writing-engine/         # Academic writing templates
│   ├── literature-engine/      # Systematic literature search
│   ├── theory-engine/          # Theoretical framing
│   ├── method-engine/          # Research methodology
│   ├── figure-engine/          # Figure generation (PaperBanana)
│   └── latex-engine/           # LaTeX conversion + compilation
├── scripts/
│   └── md_to_latex.py          # Markdown-to-LaTeX converter
├── templates/
│   └── arxiv.sty               # arxiv-style LaTeX template
├── .env.example                # API key template
├── .gitignore
├── LICENSE
└── README.md
```

---

## Figure Generation

### With PaperBanana (Claude Code)

PaperBanana uses a multi-agent pipeline powered by Google Gemini:

```
Planner → Stylist → Visualizer → Critic (×3 iterations) → Final PNG
```

The MCP server starts automatically when Claude Code loads the plugin. It reads `GOOGLE_API_KEY` from `.env` in your project directory.

| Environment | Engine | Quality |
|---|---|---|
| Claude Code | PaperBanana + Gemini | AI-generated, publication-quality |
| Cowork | matplotlib / seaborn | Clean statistical plots |

### Fallback

If PaperBanana is unavailable (no API key, network issues), the figure-engine falls back to Python-based generation using matplotlib and seaborn with academic styling presets.

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

If you use this tool in your research, please cite:

```bibtex
@article{blask2025creator,
  title={From Creator to Orchestrator: How an {LLM} Agent Wrote This Paper
         and What That Means for Science},
  author={Blask, Tobias-Benedikt},
  year={2025},
  note={Available at \url{https://github.com/ProfDrT/From_Creator_to_Orchestrator}}
}
```

---

## License

MIT License. See [LICENSE](LICENSE) for details.

**Author:** Prof. Dr. Tobias Blask — [Harz University of Applied Sciences](https://www.hs-harz.de)
