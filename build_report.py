#!/usr/bin/env python3
"""
build_report.py - assemble docs/report_v2/*.md into DEICMS_Project_Report_v2.docx

- concatenates the chapters in order
- replaces [FIGURE n.n - ...] markers with the rendered PNG plus a caption
- replaces [SCREENSHOT ...] and [CODE LISTING ...] markers with visible
  placeholder blocks telling you exactly what to paste where
- inserts a Word field so the table of contents can be updated with F9
"""
import pathlib, re, subprocess, sys

ROOT = pathlib.Path(__file__).parent
SRC  = ROOT / "docs" / "report_v2"
PNG  = ROOT / "diagrams_png"
OUT  = ROOT / "DEICMS_Project_Report_v2.docx"

FIGURES = {
    "5.1":  "burndown_increment1.png",
    "5.2":  "burndown_increment2.png",
    "5.3":  "burndown_increment3.png",
    "8.1":  "01_use_case_core.png",
    "8.2":  "02_use_case_analysis.png",
    "8.3":  "02_class.png",
    "8.4":  "03_er.png",
    "8.5":  "05_sequence_integrity.png",
    "8.6":  "06_sequence_ai.png",
    "8.7":  "07_activity_risk.png",
    "8.8":  "08_activity_reconstruction.png",
    "8.9":  "04_state_lifecycle.png",
    "8.10": "09_component.png",
    "8.11": "10_deployment.png",
}


def balance_table_widths(text):
    """
    Pandoc sizes pipe-table columns from the dash count in the separator row.
    Left to itself that follows the *header* width, which squeezes a long
    prose column into a sliver. Recompute each separator from the actual
    content width of the column instead.
    """
    out, block = [], []

    def flush():
        if not block:
            return
        rows = [r for r in block]
        cells = [[c.strip() for c in r.strip().strip("|").split("|")] for r in rows]
        ncol = len(cells[0])
        if any(len(c) != ncol for c in cells) or ncol < 2:
            out.extend(block); block.clear(); return
        # mean cell length per column, ignoring the separator row
        body = [c for i, c in enumerate(cells) if i != 1]
        widths = []
        for j in range(ncol):
            lens = [len(r[j]) for r in body]
            widths.append(max(3, int(sum(lens) / len(lens)) + 2))
        total = sum(widths)
        # scale to ~110 dashes overall so pandoc gets clean proportions
        scaled = [max(3, round(w * 110 / total)) for w in widths]
        sep = "|" + "|".join("-" * w for w in scaled) + "|"
        out.append(rows[0]); out.append(sep); out.extend(rows[2:])
        block.clear()

    for line in text.split("\n"):
        s = line.strip()
        if s.startswith("|") and s.endswith("|") and s.count("|") >= 3:
            block.append(line)
        else:
            flush(); out.append(line)
    flush()
    return "\n".join(out)

def chapters():
    return sorted(SRC.glob("ch*.md"), key=lambda p: p.name)

def substitute(text):
    stats = {"figures": 0, "screenshots": 0, "listings": 0, "missing": []}

    def fig(m):
        num, title = m.group(1), m.group(2).strip()
        name = FIGURES.get(num)
        if not name or not (PNG / name).exists():
            stats["missing"].append(num)
            return ("> **[FIGURE %s MISSING — %s]**\n>\n"
                    "> Render `diagrams_plantuml/` to PNG and rebuild." % (num, title))
        stats["figures"] += 1
        path = PNG / name
        rel = path.as_posix()
        # fit inside the printable area, preserving aspect ratio, so that
        # wide diagrams are not shrunk to illegibility by a fixed width
        MAX_W, MAX_H = 6.3, 8.0          # inches
        try:
            from PIL import Image
            w, h = Image.open(path).size
            scale = min(MAX_W / w, MAX_H / h)
            dims = "width=%.2fin height=%.2fin" % (w * scale, h * scale)
        except Exception:
            dims = "width=%.2fin" % MAX_W
        landscape = ""
        return ("%s![](%s){%s}\n\n"
                "*Figure %s — %s*" % (landscape, rel, dims, num, title))

    text = re.sub(r'\*\*\[FIGURE ([\d.]+) [—-] (.+?)\]\*\*', fig, text)

    def shot(m):
        stats["screenshots"] += 1
        return ("> **PLACE SCREENSHOT HERE — %s**  *(delete this line once "
                "the image is inserted)*" % m.group(1).strip())

    text = re.sub(r'\*\*\[SCREENSHOT (.+?)\]\*\*', shot, text)

    def listing(m):
        stats["listings"] += 1
        return ("> **PASTE CODE LISTING HERE — %s**  *(delete this line once "
                "the code is inserted)*" % m.group(1).strip())

    text = re.sub(r'\*\*\[CODE LISTING (.+?)\]\*\*', listing, text)
    return text, stats

def main():
    parts, totals = [], {"figures": 0, "screenshots": 0, "listings": 0, "missing": []}
    for p in chapters():
        body, st = substitute(p.read_text(encoding="utf-8"))
        body = balance_table_widths(body)
        for k in ("figures", "screenshots", "listings"):
            totals[k] += st[k]
        totals["missing"] += st["missing"]
        parts.append(body)

    doc = "\n\n".join(parts)

    # Word TOC field: select the TOC and press F9 in Word to populate it.
    toc_field = (
        '\n\n```{=openxml}\n'
        '<w:p><w:r><w:fldChar w:fldCharType="begin" w:dirty="true"/></w:r>'
        '<w:r><w:instrText xml:space="preserve"> TOC \\o "1-3" \\h \\z \\u </w:instrText></w:r>'
        '<w:r><w:fldChar w:fldCharType="separate"/></w:r>'
        '<w:r><w:t>Right-click here and choose "Update Field", or press F9, '
        'to generate the table of contents.</w:t></w:r>'
        '<w:r><w:fldChar w:fldCharType="end"/></w:r></w:p>\n```\n\n'
    )
    doc = doc.replace("## Table of Contents\n", "## Table of Contents\n" + toc_field, 1)

    tmp = ROOT / ".report_v2_combined.md"
    tmp.write_text(doc, encoding="utf-8")

    cmd = ["pandoc", str(tmp), "-o", str(OUT),
           "--from", "markdown+pipe_tables+raw_attribute",
           "--reference-doc=%s" % (ROOT / "reference_v2.docx"),
           "--toc-depth=3", "--resource-path=%s" % ROOT]
    subprocess.run(cmd, check=True)
    tmp.unlink()

    print("Wrote %s (%.1f MB)" % (OUT.name, OUT.stat().st_size / 1e6))
    print("  diagrams embedded : %d" % totals["figures"])
    print("  screenshot slots  : %d" % totals["screenshots"])
    print("  code listing slots: %d" % totals["listings"])

    # ---- page budget -------------------------------------------------
    # Hard limit set by the submission: 150 pages. The placeholders are one
    # line each now but become roughly a third of a page once filled, so the
    # projected final length is estimated here rather than after the fact.
    PAGE_LIMIT = 150
    growth = totals["screenshots"] * 0.35 + totals["listings"] * 0.40
    print("  projected growth once images are pasted: ~%.0f pages" % growth)
    print("  -> convert to PDF and check: current + ~%.0f must stay under %d"
          % (growth, PAGE_LIMIT))
    if totals["missing"]:
        print("  MISSING FIGURES   : %s" % ", ".join(totals["missing"]))

if __name__ == "__main__":
    sys.exit(main())
