#!/usr/bin/env python3
"""
Compile the revised DEICMS report.

    python build_report_v3.py

Produces DEICMS_Project_Report_v3.docx from docs/report_v3/*.md, embedding:
  - the 26 UML diagrams rendered from diagrams_v3/*.puml
  - the 6 burndown charts from diagrams_v3/charts/
  - the 33 screenshots recovered from the previous report

Figure placeholders of the form [FIGURE n.m - caption] are replaced by the
image the FIGURES map names. Screenshots in Chapter 16 are already written as
markdown image references and need no substitution.
"""
import os
import re
import subprocess
import sys
import shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, 'docs', 'report_v3')
DIAGRAMS = os.path.join(ROOT, 'diagrams_v3')
CHARTS = os.path.join(DIAGRAMS, 'charts')
OUT = os.path.join(ROOT, 'DEICMS_Project_Report_v4.docx')
REFERENCE = os.path.join(ROOT, 'reference_v2.docx')

CHAPTERS = [
    'ch00_front_matter.md', 'ch01_introduction.md', 'ch02_categorization.md',
    'ch03_requirements.md', 'ch04_process.md', 'ch05_architecture.md',
    'ch06_sprint1.md', 'ch07_sprint2.md', 'ch08_sprint3.md',
    'ch09_sprints45.md', 'ch10_sprint6.md', 'ch11_complex_logic.md',
    'ch12_verification.md', 'ch13_conclusion.md', 'ch16_demonstration.md',
    'ch14_references.md', 'ch15_appendices.md',
]

# Burndown placeholders written as [FIGURE n.m - ...] in the sprint chapters
FIGURE_PLACEHOLDERS = {
    '6.1':  os.path.join(CHARTS, 'burndown_sprint1.png'),
    '7.1':  os.path.join(CHARTS, 'burndown_sprint2.png'),
    '8.1':  os.path.join(CHARTS, 'burndown_sprint3.png'),
    '9.1':  os.path.join(CHARTS, 'burndown_sprint4.png'),
    '9.2':  os.path.join(CHARTS, 'burndown_sprint5.png'),
    '10.1': os.path.join(CHARTS, 'burndown_sprint6.png'),
}

def render_diagrams(jar):
    """Render every .puml to .png. Skips silently if the jar is absent."""
    if not jar or not os.path.exists(jar):
        print('  plantuml.jar not found - using existing .png files')
        return
    pumls = [f for f in sorted(os.listdir(DIAGRAMS)) if f.endswith('.puml')]
    subprocess.run(['java', '-jar', jar, '-tpng', '-o', DIAGRAMS]
                   + [os.path.join(DIAGRAMS, f) for f in pumls],
                   check=False, capture_output=True)
    print(f'  rendered {len(pumls)} diagrams')


def balance_table_widths(text):
    """
    Resize pipe-table separator rows by MEAN cell content width.

    pandoc sizes a column from the width of its separator dashes, and a naive
    table makes every column equal. Long prose columns then wrap to nothing
    while short ones waste the page.
    """
    lines = text.split('\n')
    out = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if (re.match(r'^\s*\|[\s:|-]+\|\s*$', line) and '-' in line
                and i > 0 and lines[i - 1].strip().startswith('|')):
            # collect the table body
            j = i + 1
            body = []
            while j < len(lines) and lines[j].strip().startswith('|'):
                body.append(lines[j])
                j += 1
            header = [c.strip() for c in lines[i - 1].strip().strip('|').split('|')]
            ncol = len(header)
            widths = []
            for c in range(ncol):
                vals = [len(header[c])]
                for row in body:
                    cells = [x.strip() for x in row.strip().strip('|').split('|')]
                    if c < len(cells):
                        vals.append(len(cells[c]))
                widths.append(max(3, int(sum(vals) / len(vals))))
            total = sum(widths) or 1
            scaled = [max(3, int(72 * w / total)) for w in widths]
            out.append('|' + '|'.join('-' * w for w in scaled) + '|')
            i += 1
            continue
        out.append(line)
        i += 1
    return '\n'.join(out)


def substitute_figures(text):
    """Replace [FIGURE n.m - caption] with the image plus a caption line."""
    def repl(m):
        num, caption = m.group(1), m.group(2).strip()
        path = FIGURE_PLACEHOLDERS.get(num)
        if not path or not os.path.exists(path):
            return f'*[Figure {num} - {caption}: image not found]*'
        rel = os.path.relpath(path, SRC).replace('\\', '/')
        return f'![]({rel})\n\n**Figure {num} - {caption}.**'
    return re.sub(r'\*\*\[FIGURE ([\d.]+) - ([^\]]+)\]\*\*', repl, text)


def set_table_column_widths(docx_path, usable_twips=9180):
    """
    Give every table an explicit grid, with column widths PROPORTIONAL to the
    text each column actually carries.

    Two problems are fixed here. pandoc emits an empty <w:tblGrid> when a
    table's longest content line is under --columns, which Word renders as one
    collapsed column. And dividing the width evenly makes a prose column wrap
    into a thin ribbon beside seven short ones, which turns a one-line row
    into half a page.
    """
    try:
        from docx import Document
        from docx.oxml.ns import qn
        from docx.oxml import OxmlElement
    except ImportError:
        print('  python-docx not installed - skipping column widths')
        return
    doc = Document(docx_path)
    for table in doc.tables:
        ncol = len(table.columns) or 1

        # mean characters per column, with the header counted once
        means = []
        for c in range(ncol):
            lengths = []
            for r, row in enumerate(table.rows):
                cells = row.cells
                if c < len(cells):
                    lengths.append(len(cells[c].text.strip()))
            means.append(max(4.0, sum(lengths) / max(1, len(lengths))))

        # damp the spread so one huge column cannot starve the rest
        weights = [m ** 0.6 for m in means]
        total_w = sum(weights)
        min_tw = int(usable_twips * 0.075)          # ~7.5% floor per column
        widths = [max(min_tw, int(usable_twips * w / total_w)) for w in weights]
        # rescale so the row still sums to the usable width
        scale = usable_twips / sum(widths)
        widths = [int(w * scale) for w in widths]
        widths[-1] += usable_twips - sum(widths)

        tblPr = table._tbl.tblPr
        for tag in ('tblW', 'tblLayout'):
            for el in tblPr.findall(qn('w:' + tag)):
                tblPr.remove(el)
        w = OxmlElement('w:tblW'); w.set(qn('w:w'), '5000'); w.set(qn('w:type'), 'pct')
        tblPr.append(w)
        lay = OxmlElement('w:tblLayout'); lay.set(qn('w:type'), 'fixed')
        tblPr.append(lay)

        for g in table._tbl.findall(qn('w:tblGrid')):
            table._tbl.remove(g)
        grid = OxmlElement('w:tblGrid')
        for tw in widths:
            gc = OxmlElement('w:gridCol'); gc.set(qn('w:w'), str(tw)); grid.append(gc)
        table._tbl.insert(1, grid)

        for row in table.rows:
            for i, cell in enumerate(row.cells):
                if i >= ncol:
                    continue
                tcPr = cell._tc.get_or_add_tcPr()
                for el in tcPr.findall(qn('w:tcW')):
                    tcPr.remove(el)
                tcW = OxmlElement('w:tcW')
                tcW.set(qn('w:w'), str(widths[i])); tcW.set(qn('w:type'), 'dxa')
                tcPr.append(tcW)
    doc.save(docx_path)
    print(f'  proportional widths on {len(doc.tables)} tables')


def format_title_page(docx_path, logo=None):
    """
    Centre everything before the first page break and strip heading styles
    so the title page does not list itself in the table of contents.
    """
    from docx import Document
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml.ns import qn
    doc = Document(docx_path)
    for p in doc.paragraphs:
        if p._p.findall('.//' + qn('w:br')):
            if any(b.get(qn('w:type')) == 'page' for b in p._p.findall('.//' + qn('w:br'))):
                break
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        if p.style.name.startswith('Heading') or p.style.name == 'Title':
            p.style = doc.styles['Normal']
    doc.save(docx_path)
    print('  title page centred')


def justify_body(docx_path):
    """
    Justify body paragraphs. Headings, captions, figures and code keep their
    own alignment - justifying a one-line caption stretches it across the page.
    """
    from docx import Document
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml.ns import qn
    doc = Document(docx_path)
    seen_break = False
    n = 0
    for p in doc.paragraphs:
        if not seen_break:
            if any(b.get(qn('w:type')) == 'page'
                   for b in p._p.findall('.//' + qn('w:br'))):
                seen_break = True
            continue
        style = p.style.name
        text = p.text.strip()
        if style.startswith('Heading') or style in ('Title', 'Subtitle'):
            continue
        if style in ('Source Code', 'Verbatim Char', 'Code', 'HTML Preformatted'):
            continue
        if p._p.findall('.//' + qn('w:drawing')):          # a figure
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            continue
        if text.startswith('Figure ') or text.startswith('Table ') \
           or text.startswith('Listing '):                 # captions
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            continue
        if len(text) < 60:
            continue
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        n += 1
    doc.save(docx_path)
    print(f'  justified {n} body paragraphs')


def add_table_borders(docx_path):
    """Single hairline borders on every cell of every table."""
    from docx import Document
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement
    doc = Document(docx_path)
    for table in doc.tables:
        tblPr = table._tbl.tblPr
        for el in tblPr.findall(qn('w:tblBorders')):
            tblPr.remove(el)
        borders = OxmlElement('w:tblBorders')
        for edge in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
            e = OxmlElement('w:' + edge)
            e.set(qn('w:val'), 'single')
            e.set(qn('w:sz'), '4')          # 0.5pt
            e.set(qn('w:space'), '0')
            e.set(qn('w:color'), '000000')
            borders.append(e)
        tblPr.append(borders)
        # header row repeats across pages, and no row splits across a page
        for i, row in enumerate(table.rows):
            trPr = row._tr.get_or_add_trPr()
            for tag in ('cantSplit', 'tblHeader'):
                for el in trPr.findall(qn('w:' + tag)):
                    trPr.remove(el)
            cant = OxmlElement('w:cantSplit'); trPr.append(cant)
            if i == 0:
                hdr = OxmlElement('w:tblHeader'); trPr.append(hdr)
    doc.save(docx_path)
    print(f'  bordered {len(doc.tables)} tables')


def main():
    jar = (os.environ.get('PLANTUML_JAR')
           or shutil.which('plantuml')
           or os.path.join(ROOT, 'plantuml.jar'))
    print('Rendering diagrams...')
    render_diagrams(jar if jar.endswith('.jar') else None)

    print('Assembling chapters...')
    merged = []
    for name in CHAPTERS:
        path = os.path.join(SRC, name)
        if not os.path.exists(path):
            print(f'  MISSING: {name}')
            continue
        text = open(path, encoding='utf-8').read()
        text = substitute_figures(text)
        text = balance_table_widths(text)
        text = text.replace('—', '-').replace('–', '-')
        # \newpage is LaTeX and is silently dropped for docx; emit a real
        # Word page break so each chapter starts on a fresh page.
        text = text.replace(
            '\\newpage',
            '```{=openxml}\n<w:p><w:r><w:br w:type="page"/></w:r></w:p>\n```')
        merged.append(text)
        print(f'  {name:28s} {len(text.split()):6,} words')

    combined = os.path.join(SRC, '_combined.md')
    open(combined, 'w', encoding='utf-8').write('\n\n'.join(merged))
    words = sum(len(m.split()) for m in merged)
    print(f'  total {words:,} words')

    print('Converting with pandoc...')
    cmd = ['pandoc', combined, '-o', OUT, '--columns=72',
           '--resource-path', SRC, '--toc-depth=2']
    if os.path.exists(REFERENCE):
        cmd += ['--reference-doc', REFERENCE]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print('pandoc failed:\n' + r.stderr)
        return 1

    print('Post-processing...')
    set_table_column_widths(OUT)
    add_table_borders(OUT)
    justify_body(OUT)
    format_title_page(OUT)
    size = os.path.getsize(OUT) / 1024 / 1024
    print(f'\nWrote {OUT}  ({size:.1f} MB)')
    print('\nIn Word: select all (Ctrl+A), press F9, choose "Update entire table"')
    print('to build the table of contents.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
