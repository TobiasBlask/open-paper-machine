---
description: >
  Export the current paper draft to production-ready LaTeX (.tex) and PDF using
  the arxiv-style template. Converts draft.md + references.bib + figures/ into a
  complete LaTeX project with resolved citations, tables, and figures. Compiles
  to PDF automatically.
---

# Export LaTeX: **$ARGUMENTS**

Activate the **latex-engine** skill. Read `skills/latex-engine/SKILL.md` in full.
Then execute the full export pipeline:

1. **Verify prerequisites**: Check that `draft.md` and `references.bib` exist in the working directory.
   If they don't exist, inform the user they need to run `/write-paper` first.

2. **Install LaTeX if needed**: Check if `pdflatex` is available. If not, install:
   ```bash
   apt-get update && apt-get install -y texlive-latex-base texlive-latex-extra texlive-fonts-recommended texlive-bibtex-extra
   ```

3. **Set up the latex/ directory**: Create `latex/` with arxiv.sty, references.bib, and figures/.

4. **Run the converter**: Use `scripts/md_to_latex.py` to generate `paper.tex`.
   - If $ARGUMENTS includes author info, pass it through.
   - If $ARGUMENTS includes a title override, use it.

5. **Compile to PDF**: Run pdflatex → bibtex → pdflatex → pdflatex.

6. **Validate**: Check for undefined citations, missing figures, and remaining TODOs.

7. **Report results**: Present the final package with file list and any issues found.

Do not ask for confirmation to start — execute immediately.
