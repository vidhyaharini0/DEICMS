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
        rel = (PNG / name).as_posix()
        return ("![](%s){width=6.2in}\n\n"
                "*Figure %s — %s*" % (rel, num, title))

    text = re.sub(r'\*\*\[FIGURE ([\d.]+) [—-] (.+?)\]\*\*', fig, text)

    def shot(m):
        stats["screenshots"] += 1
        return ("> ### PLACE SCREENSHOT HERE\n"
                "> **%s**\n>\n"
                "> *(delete this box once the image is inserted)*" % m.group(1).strip())

    text = re.sub(r'\*\*\[SCREENSHOT (.+?)\]\*\*', shot, text)

    def listing(m):
        stats["listings"] += 1
        return ("> ### PASTE CODE LISTING HERE\n"
                "> **%s**\n>\n"
                "> *(delete this box once the code is inserted)*" % m.group(1).strip())

    text = re.sub(r'\*\*\[CODE LISTING (.+?)\]\*\*', listing, text)
    return text, stats

def main():
    parts, totals = [], {"figures": 0, "screenshots": 0, "listings": 0, "missing": []}
    for p in chapters():
        body, st = substitute(p.read_text(encoding="utf-8"))
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
           "--toc-depth=3", "--resource-path=%s" % ROOT]
    subprocess.run(cmd, check=True)
    tmp.unlink()

    print("Wrote %s (%.1f MB)" % (OUT.name, OUT.stat().st_size / 1e6))
    print("  diagrams embedded : %d" % totals["figures"])
    print("  screenshot slots  : %d" % totals["screenshots"])
    print("  code listing slots: %d" % totals["listings"])
    if totals["missing"]:
        print("  MISSING FIGURES   : %s" % ", ".join(totals["missing"]))

if __name__ == "__main__":
    sys.exit(main())
