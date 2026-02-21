#!/usr/bin/env python3
"""
Markdown-to-LaTeX converter for the Academic Research Plugin.

Converts draft.md (with (Author, Year) citations) into a production-ready
.tex file using the arxiv-style template. Handles:
  - Section/subsection hierarchy (# → \\section, ## → \\subsection, etc.)
  - (Author, Year) citations → \\citep{key} or \\citet{key}
  - Inline **bold** and *italic* → \\textbf{} and \\textit{}
  - Figure references preserved
  - Markdown images → LaTeX figure environments
  - Markdown tables → LaTeX booktabs tables
  - Bullet/numbered lists → itemize/enumerate
  - Abstract extraction
  - Keywords extraction
  - [CITE], [DATA], [TODO] markers → LaTeX comments

Usage:
    python md_to_latex.py draft.md references.bib --output paper.tex
    python md_to_latex.py draft.md references.bib --output paper.tex \\
        --title "My Paper" --author "Name;;Affiliation;;email"
    python md_to_latex.py draft.md references.bib --output paper.tex --compile
"""

import re
import sys
import argparse
from pathlib import Path
from typing import Optional


# ---------------------------------------------------------------------------
# BibTeX Parsing
# ---------------------------------------------------------------------------

def parse_bibtex_keys(bib_path: str) -> dict:
    """Extract all BibTeX keys and their author/year info for citation matching."""
    bib_text = Path(bib_path).read_text(encoding="utf-8")
    entries = {}

    # Match @type{key, then look for author and year fields
    entry_pattern = re.compile(r"@\w+\{([^,]+),", re.IGNORECASE)
    author_pattern = re.compile(r"author\s*=\s*[{\"]([^}\"]+)[}\"]", re.IGNORECASE)
    year_pattern = re.compile(r"year\s*=\s*[{\"](\d{4})[}\"]", re.IGNORECASE)

    # Split into entry blocks
    blocks = re.split(r"(?=@\w+\{)", bib_text)

    for block in blocks:
        entry_match = entry_pattern.search(block)
        if not entry_match:
            continue

        key = entry_match.group(1).strip()
        author_match = author_pattern.search(block)
        year_match = year_pattern.search(block)

        author_raw = author_match.group(1) if author_match else ""
        year = year_match.group(1) if year_match else ""

        # Extract last name of first author
        if author_raw:
            first_author = author_raw.split(" and ")[0].strip()
            if "," in first_author:
                last_name = first_author.split(",")[0].strip()
            else:
                parts = first_author.split()
                last_name = parts[-1] if parts else first_author
        else:
            last_name = ""

        entries[key] = {"author": last_name, "year": year, "full_author": author_raw}

    return entries


def build_citation_index(bib_entries: dict) -> dict:
    """Build a lookup from (AuthorLastName, Year) → BibTeX key."""
    index = {}
    for key, info in bib_entries.items():
        if info["author"] and info["year"]:
            lookup = (info["author"].lower(), info["year"])
            if lookup not in index:
                index[lookup] = key
            # Also store without accents/special chars for fuzzy matching
            clean = re.sub(r"[^a-z]", "", info["author"].lower())
            if clean and (clean, info["year"]) not in index:
                index[(clean, info["year"])] = key
    return index


def resolve_citation(author_text: str, year: str, citation_index: dict) -> str:
    """Resolve an (Author, Year) citation to a BibTeX key."""
    author_clean = author_text.strip().rstrip(",").strip()
    yr = year.strip()

    # Try exact match
    lookup = (author_clean.lower(), yr)
    if lookup in citation_index:
        return citation_index[lookup]

    # Try without special characters
    clean = re.sub(r"[^a-z]", "", author_clean.lower())
    if (clean, yr) in citation_index:
        return citation_index[(clean, yr)]

    # For "Author & Author" or "Author and Author", try just the first author
    first_author = re.split(r"\s+(?:&|and)\s+", author_clean)[0].strip()
    first_clean = re.sub(r"[^a-z]", "", first_author.lower())
    if (first_clean, yr) in citation_index:
        return citation_index[(first_clean, yr)]

    # For "Author et al.", strip the "et al." and try
    et_al_stripped = re.sub(r"\s+et\s+al\.?$", "", author_clean, flags=re.IGNORECASE).strip()
    et_al_clean = re.sub(r"[^a-z]", "", et_al_stripped.lower())
    if (et_al_clean, yr) in citation_index:
        return citation_index[(et_al_clean, yr)]

    # Try partial match (first word of author)
    first_word = author_clean.split()[0].lower() if author_clean else ""
    clean_first = re.sub(r"[^a-z]", "", first_word)
    for (a, y), key in citation_index.items():
        if y == yr and (a.startswith(clean_first) or clean_first.startswith(a)):
            return key

    # Fallback: generate a plausible key from first author word + year
    fallback = re.sub(r"[^a-zA-Z]", "", first_author.split()[0]) if first_author else "unknown"
    return f"{fallback.lower()}{yr}"


# ---------------------------------------------------------------------------
# Citation Conversion
# ---------------------------------------------------------------------------

def convert_citations(text: str, citation_index: dict) -> str:
    """Convert (Author, Year) and Author (Year) citations to LaTeX \\citep/\\citet."""

    # Pattern 1: Parenthetical — (Author, Year) including multi-citations with ;
    def replace_parens_citation(match):
        inner = match.group(1)
        if ";" in inner:
            parts = inner.split(";")
            keys = []
            for part in parts:
                part = part.strip()
                m = re.match(r"(.+?),?\s*(\d{4}[a-z]?)", part)
                if m:
                    keys.append(resolve_citation(m.group(1), m.group(2), citation_index))
                else:
                    return match.group(0)
            return "\\citep{" + ", ".join(keys) + "}"
        else:
            m = re.match(r"(.+?),?\s*(\d{4}[a-z]?)\s*", inner)
            if m:
                key = resolve_citation(m.group(1), m.group(2), citation_index)
                return "\\citep{" + key + "}"
            return match.group(0)

    text = re.sub(
        r"\(([A-Z][a-zA-ZÀ-ÿ\s&.,]+(?:et\s+al\.?)?,?\s*\d{4}[a-z]?"
        r"(?:\s*;\s*[A-Z][a-zA-ZÀ-ÿ\s&.,]+(?:et\s+al\.?)?,?\s*\d{4}[a-z]?)*)\)",
        replace_parens_citation,
        text,
    )

    # Pattern 2: Narrative — Author (Year), Author & Author (Year), Author et al. (Year)
    def replace_narrative_citation(match):
        author = match.group(1).strip()
        year = match.group(2).strip()
        key = resolve_citation(author, year, citation_index)
        return "\\citet{" + key + "}"

    text = re.sub(
        r"([A-Z][a-zA-ZÀ-ÿ]+"
        r"(?:\s+(?:et\s+al\.?"
        r"|&\s+[A-Z][a-zA-ZÀ-ÿ]+"
        r"|and\s+[A-Z][a-zA-ZÀ-ÿ]+))?)"
        r"\s+\((\d{4}[a-z]?)\)",
        replace_narrative_citation,
        text,
    )

    return text


# ---------------------------------------------------------------------------
# Text Conversion Utilities
# ---------------------------------------------------------------------------

def convert_markers(text: str) -> str:
    """Convert [CITE], [DATA], [TODO] markers to LaTeX comments."""
    text = re.sub(r"\[CITE\]", r"% TODO: CITATION NEEDED", text)
    text = re.sub(r"\[DATA\]", r"% TODO: DATA NEEDED", text)
    text = re.sub(r"\[TODO(?::?\s*([^\]]*))?\]", r"% TODO: \1", text)
    return text


def escape_latex(text: str) -> str:
    """Escape special LaTeX characters in running text (carefully)."""
    # Only escape characters that aren't part of LaTeX commands
    text = re.sub(r"(?<!\\)&(?!\\)", r"\\&", text)
    text = re.sub(r"(?<!\\)%", r"\\%", text)
    text = re.sub(r"(?<!\\)#(?!{)", r"\\#", text)
    return text


def convert_inline_formatting(text: str) -> str:
    """Convert markdown inline formatting to LaTeX."""
    # Bold: **text** → \textbf{text}
    text = re.sub(r"\*\*(.+?)\*\*", r"\\textbf{\1}", text)
    # Italic: *text* → \textit{text}
    text = re.sub(r"(?<!\*)\*([^*]+?)\*(?!\*)", r"\\textit{\1}", text)
    # Inline code: `text` → \texttt{text}
    text = re.sub(r"`([^`]+)`", r"\\texttt{\1}", text)
    # Em-dash / en-dash
    text = text.replace(" --- ", " --- ")
    text = text.replace(" -- ", " -- ")
    text = re.sub(r" - ", " -- ", text)
    # Escape special chars
    text = escape_latex(text)
    return text


# ---------------------------------------------------------------------------
# Structure Extraction
# ---------------------------------------------------------------------------

def extract_abstract(lines: list) -> tuple:
    """Extract abstract section. Returns (abstract_text, remaining_lines).

    NOTE: Keywords lines found inside the abstract section are moved to
    the remaining lines so that extract_keywords() can pick them up.
    """
    abstract_lines = []
    keyword_lines = []
    in_abstract = False
    remaining = []

    kw_pattern = re.compile(
        r"^[\*_]{0,2}Keywords[\*_]{0,2}\s*:", re.IGNORECASE
    )

    for line in lines:
        if re.match(r"^#{1,2}\s+Abstract", line, re.IGNORECASE):
            in_abstract = True
            continue
        elif in_abstract and re.match(r"^#{1,3}\s+", line):
            in_abstract = False
            remaining.append(line)
            continue

        if in_abstract:
            # Check if this line is actually a keywords line
            stripped = line.strip()
            clean = re.sub(r"\*{1,2}", "", stripped)
            if re.match(r"^Keywords\s*:", clean, re.IGNORECASE):
                keyword_lines.append(line)
            else:
                abstract_lines.append(line)
        else:
            remaining.append(line)

    # Put keyword lines back into remaining so extract_keywords picks them up
    return "\n".join(abstract_lines).strip(), keyword_lines + remaining


def extract_keywords(lines: list) -> tuple:
    """Extract keywords. Returns (keywords_list, remaining_lines)."""
    keywords = []
    remaining = []

    for line in lines:
        stripped = line.strip()
        # Strip all markdown bold/italic from the line for matching
        # e.g. "**Keywords:** Deep Learning, ..." → "Keywords: Deep Learning, ..."
        clean = re.sub(r"\*{1,2}", "", stripped)
        clean = re.sub(r"_{1,2}", "", clean)
        m = re.match(r"^Keywords\s*:\s*(.+)", clean, re.IGNORECASE)
        if m:
            kw_text = m.group(1).strip()
            keywords = [
                k.strip().strip("*").strip("_").strip()
                for k in re.split(r"[,;·]", kw_text)
                if k.strip()
            ]
            continue
        remaining.append(line)

    return keywords, remaining


# ---------------------------------------------------------------------------
# Table Conversion
# ---------------------------------------------------------------------------

def convert_table(table_lines: list) -> str:
    """Convert a markdown table to LaTeX booktabs table."""
    if len(table_lines) < 2:
        return "\n".join(table_lines)

    header = [cell.strip() for cell in table_lines[0].strip("|").split("|")]
    ncols = len(header)

    data_lines = []
    for line in table_lines[2:]:
        if line.strip():
            cells = [cell.strip() for cell in line.strip("|").split("|")]
            data_lines.append(cells)

    col_spec = "l" * ncols
    tex = []
    tex.append("\\begin{table}[htbp]")
    tex.append("\\centering")
    tex.append(f"\\begin{{tabular}}{{{col_spec}}}")
    tex.append("\\toprule")
    tex.append(" & ".join(f"\\textbf{{{escape_latex(h)}}}" for h in header) + " \\\\")
    tex.append("\\midrule")
    for row in data_lines:
        while len(row) < ncols:
            row.append("")
        tex.append(" & ".join(convert_inline_formatting(c) for c in row[:ncols]) + " \\\\")
    tex.append("\\bottomrule")
    tex.append("\\end{tabular}")
    tex.append("\\end{table}")

    return "\n".join(tex)


# ---------------------------------------------------------------------------
# Body Conversion
# ---------------------------------------------------------------------------

def convert_body(lines: list, citation_index: dict) -> str:
    """Convert the body of the markdown to LaTeX."""
    output = []
    i = 0
    in_list = False
    list_type = None

    while i < len(lines):
        line = lines[i]

        # Skip standalone title (# Title at start)
        if i == 0 and re.match(r"^#\s+", line) and not re.match(r"^##", line):
            i += 1
            continue

        # Section headings
        m = re.match(r"^(#{1,4})\s+(.+)", line)
        if m:
            if in_list:
                output.append(f"\\end{{{list_type}}}")
                in_list = False

            level = len(m.group(1))
            heading = m.group(2).strip()

            if re.match(r"Abstract", heading, re.IGNORECASE):
                i += 1
                continue

            label = re.sub(r"[^a-zA-Z0-9]+", "_", heading.lower()).strip("_")
            heading_tex = convert_inline_formatting(heading)

            cmd = {1: "section", 2: "subsection", 3: "subsubsection", 4: "paragraph"}[level]
            output.append(f"\n\\{cmd}{{{heading_tex}}}")
            if level <= 3:
                output.append(f"\\label{{sec:{label}}}")

            i += 1
            continue

        # Table detection
        if "|" in line and i + 1 < len(lines) and re.match(r"^\|[\s\-:|]+\|", lines[i + 1]):
            if in_list:
                output.append(f"\\end{{{list_type}}}")
                in_list = False

            table_lines_block = []
            while i < len(lines) and "|" in lines[i]:
                table_lines_block.append(lines[i])
                i += 1
            output.append(convert_table(table_lines_block))
            continue

        # LaTeX figure environments (passed through from figure-engine)
        if re.match(r"\\begin\{figure\}", line.strip()):
            if in_list:
                output.append(f"\\end{{{list_type}}}")
                in_list = False

            fig_lines = [line]
            i += 1
            while i < len(lines) and "\\end{figure}" not in lines[i]:
                fig_lines.append(lines[i])
                i += 1
            if i < len(lines):
                fig_lines.append(lines[i])
                i += 1
            output.append("\n".join(fig_lines))
            continue

        # Markdown image → LaTeX figure
        img_match = re.match(r"!\[([^\]]*)\]\(([^)]+)\)", line.strip())
        if img_match:
            if in_list:
                output.append(f"\\end{{{list_type}}}")
                in_list = False

            caption = img_match.group(1)
            img_path = img_match.group(2)
            label = re.sub(r"[^a-zA-Z0-9]+", "_", caption.lower()).strip("_")
            output.append("\\begin{figure}[htbp]")
            output.append("\\centering")
            output.append(f"\\includegraphics[width=\\linewidth]{{{img_path}}}")
            output.append(f"\\caption{{{escape_latex(caption)}}}")
            output.append(f"\\label{{fig:{label}}}")
            output.append("\\end{figure}")
            i += 1
            continue

        # Bullet list
        bullet_match = re.match(r"^(\s*)[-*]\s+(.+)", line)
        if bullet_match:
            content = bullet_match.group(2)
            content = convert_citations(content, citation_index)
            content = convert_inline_formatting(content)
            content = convert_markers(content)

            if not in_list or list_type != "itemize":
                if in_list:
                    output.append(f"\\end{{{list_type}}}")
                output.append("\\begin{itemize}")
                in_list = True
                list_type = "itemize"

            output.append(f"  \\item {content}")
            i += 1
            continue

        # Numbered list
        num_match = re.match(r"^(\s*)\d+[.)]\s+(.+)", line)
        if num_match:
            content = num_match.group(2)
            content = convert_citations(content, citation_index)
            content = convert_inline_formatting(content)
            content = convert_markers(content)

            if not in_list or list_type != "enumerate":
                if in_list:
                    output.append(f"\\end{{{list_type}}}")
                output.append("\\begin{enumerate}")
                in_list = True
                list_type = "enumerate"

            output.append(f"  \\item {content}")
            i += 1
            continue

        # Close list on non-list content
        if in_list and line.strip() and not re.match(r"^\s*[-*]\s+", line) and not re.match(r"^\s*\d+[.)]\s+", line):
            output.append(f"\\end{{{list_type}}}")
            in_list = False

        # Empty line
        if not line.strip():
            output.append("")
            i += 1
            continue

        # Regular paragraph text — citations BEFORE inline formatting
        # (escape_latex in convert_inline_formatting would break & in author names)
        text = convert_citations(line, citation_index)
        text = convert_inline_formatting(text)
        text = convert_markers(text)
        output.append(text)

        i += 1

    if in_list:
        output.append(f"\\end{{{list_type}}}")

    return "\n".join(output)


# ---------------------------------------------------------------------------
# Author Block
# ---------------------------------------------------------------------------

def build_author_block(authors: list) -> str:
    """Build LaTeX author block from 'Name;;Affiliation;;Email' strings."""
    parts = []
    for author_str in authors:
        fields = author_str.split(";;")
        name = fields[0].strip() if len(fields) > 0 else "Author"
        affiliation = fields[1].strip() if len(fields) > 1 else ""
        email = fields[2].strip() if len(fields) > 2 else ""

        block = name
        if affiliation:
            block += f" \\\\\n\t{affiliation}"
        if email:
            block += f" \\\\\n\t\\texttt{{{email}}}"

        parts.append(block)

    return "\\author{" + " \\And\n\t".join(parts) + "}"


# ---------------------------------------------------------------------------
# Document Assembly
# ---------------------------------------------------------------------------

def assemble_document(
    title: str,
    author_block: str,
    abstract: str,
    keywords: list,
    body: str,
    bib_file: str,
    header_right: str = "A Preprint",
) -> str:
    """Assemble the complete LaTeX document."""

    abstract_tex = convert_inline_formatting(abstract) if abstract else "% TODO: Write abstract"
    keywords_tex = " \\and ".join(keywords) if keywords else "% TODO: Add keywords"
    title_tex = escape_latex(title)

    doc = f"""\\documentclass{{article}}

\\usepackage{{arxiv}}

\\usepackage[utf8]{{inputenc}}
\\usepackage[T1]{{fontenc}}
\\usepackage{{hyperref}}
\\usepackage{{url}}
\\usepackage{{booktabs}}
\\usepackage{{amsfonts}}
\\usepackage{{nicefrac}}
\\usepackage{{microtype}}
\\usepackage{{cleveref}}
\\usepackage{{graphicx}}
\\usepackage{{natbib}}
\\usepackage{{doi}}
\\usepackage{{multirow}}
\\usepackage{{adjustbox}}

\\renewcommand{{\\headeright}}{{{header_right}}}
\\renewcommand{{\\undertitle}}{{{header_right}}}
\\renewcommand{{\\shorttitle}}{{{title_tex}}}

\\title{{{title_tex}}}

{author_block}

\\hypersetup{{
  pdftitle={{{title_tex}}},
  pdfkeywords={{{", ".join(keywords) if keywords else ""}}},
}}

\\begin{{document}}
\\maketitle

\\begin{{abstract}}
{abstract_tex}
\\end{{abstract}}

\\keywords{{{keywords_tex}}}

{body}

\\bibliographystyle{{unsrtnat}}
\\bibliography{{{bib_file}}}

\\end{{document}}
"""
    return doc


# ---------------------------------------------------------------------------
# Main Conversion Function
# ---------------------------------------------------------------------------

def md_to_latex(
    md_path: str,
    bib_path: str,
    title: Optional[str] = None,
    authors: Optional[list] = None,
    keywords_override: Optional[list] = None,
    header_right: str = "A Preprint",
) -> str:
    """
    Convert a markdown draft to a complete LaTeX document using arxiv-style.

    Args:
        md_path: Path to draft.md
        bib_path: Path to references.bib
        title: Paper title (extracted from md if not provided)
        authors: List of "Name;;Affiliation;;Email" strings
        keywords_override: Override keywords from markdown
        header_right: Text for the right header

    Returns:
        Complete LaTeX document as string
    """
    md_text = Path(md_path).read_text(encoding="utf-8")
    lines = md_text.split("\n")

    # Parse BibTeX
    bib_entries = parse_bibtex_keys(bib_path)
    citation_index = build_citation_index(bib_entries)

    # Extract title
    if not title:
        for line in lines:
            m = re.match(r"^#\s+(.+)", line)
            if m:
                title = m.group(1).strip()
                break
        if not title:
            title = "Untitled Paper"

    # Extract abstract and keywords
    abstract_text, lines = extract_abstract(lines)
    keywords, lines = extract_keywords(lines)
    if keywords_override:
        keywords = keywords_override

    # Author block
    if authors:
        author_block = build_author_block(authors)
    else:
        author_block = (
            "% TODO: Add authors\n"
            "\\author{Author Name \\\\\nAffiliation \\\\\n\\texttt{email@example.com}}"
        )

    # Convert body
    body = convert_body(lines, citation_index)

    # Assemble
    return assemble_document(
        title=title,
        author_block=author_block,
        abstract=abstract_text,
        keywords=keywords,
        body=body,
        bib_file=Path(bib_path).stem,
        header_right=header_right,
    )


# ---------------------------------------------------------------------------
# PDF Compilation
# ---------------------------------------------------------------------------

def compile_pdf(tex_path: str, output_dir: str = None) -> Optional[str]:
    """Compile .tex to PDF using pdflatex + bibtex."""
    import subprocess

    tex_file = Path(tex_path)
    work_dir = Path(output_dir) if output_dir else tex_file.parent
    tex_name = tex_file.stem

    # pdflatex → bibtex → pdflatex → pdflatex
    commands = [
        ["pdflatex", "-interaction=nonstopmode", "-output-directory", str(work_dir), str(tex_file)],
        ["bibtex", str(work_dir / tex_name)],
        ["pdflatex", "-interaction=nonstopmode", "-output-directory", str(work_dir), str(tex_file)],
        ["pdflatex", "-interaction=nonstopmode", "-output-directory", str(work_dir), str(tex_file)],
    ]

    for cmd in commands:
        result = subprocess.run(
            cmd, capture_output=True, text=True, cwd=str(tex_file.parent), timeout=120
        )
        if result.returncode != 0 and "bibtex" not in cmd[0]:
            print(f"Warning: {cmd[0]} returned {result.returncode}", file=sys.stderr)

    pdf_path = work_dir / f"{tex_name}.pdf"
    if pdf_path.exists():
        print(f"PDF generated: {pdf_path}")
        return str(pdf_path)
    else:
        print("PDF generation failed. Check the .log file for errors.", file=sys.stderr)
        return None


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Convert academic markdown draft to arxiv-style LaTeX"
    )
    parser.add_argument("md_file", help="Path to draft.md")
    parser.add_argument("bib_file", help="Path to references.bib")
    parser.add_argument("--output", "-o", default="paper.tex", help="Output .tex file")
    parser.add_argument("--title", "-t", help="Paper title (auto-detected if omitted)")
    parser.add_argument(
        "--author", "-a", action="append",
        help='Author: "Name;;Affiliation;;Email" (repeatable)',
    )
    parser.add_argument("--keywords", "-k", help="Comma-separated keywords")
    parser.add_argument("--header", default="A Preprint", help="Header text")
    parser.add_argument("--compile", action="store_true", help="Also compile to PDF")
    parser.add_argument("--figures-dir", default="figures", help="Figures directory")

    args = parser.parse_args()

    keywords = [k.strip() for k in args.keywords.split(",")] if args.keywords else None

    tex_content = md_to_latex(
        md_path=args.md_file,
        bib_path=args.bib_file,
        title=args.title,
        authors=args.author,
        keywords_override=keywords,
        header_right=args.header,
    )

    output_path = Path(args.output)
    output_path.write_text(tex_content, encoding="utf-8")
    print(f"LaTeX file written: {output_path}")

    if args.compile:
        compile_pdf(str(output_path))


if __name__ == "__main__":
    main()
