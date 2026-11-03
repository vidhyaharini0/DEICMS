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
OUT = os.path.join(ROOT, 'DEICMS_Project_Report_v3.docx')
REFERENCE = os.path.join(ROOT, 'reference_v2.docx')

CHAPTERS = [
    'ch00_front_matter.md', 'ch01_introduction.md', 'ch02_categorisation.md',
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

# "Figure N" in the text refers to these diagrams, appended as a plate section
DIAGRAM_ORDER = [
    ('1',  '01_usecase_overview',        'Use Case Diagram - system overview'),
    ('2',  '02_usecase_case_evidence',   'Use Case Diagram - cases and evidence'),
    ('3',  '03_usecase_reading',         'Use Case Diagram - the Read-Only Viewer'),
    ('4',  '04_usecase_analysis',        'Use Case Diagram - what each role adds'),
    ('5',  '05_class_domain',            'Class Diagram - domain model with behaviour'),
    ('6',  '06_class_persistent',        'Class Diagram - the schema as stereotyped classes'),
    ('7',  '07_object_snapshot',         'Object Diagram - a flagged exhibit'),
    ('8',  '08_package_layers',          'Package Diagram - layered architecture'),
    ('9',  '09_component',               'Component Diagram - components and interfaces'),
    ('10', '10_composite_verifier',      'Composite Structure - the integrity engine'),
    ('11', '11_deployment',              'Deployment Diagram'),
    ('12', '12_sequence_integrity',      'Sequence Diagram - integrity verification'),
    ('13', '13_sequence_assistant',      'Sequence Diagram - assistant orchestration'),
    ('14', '14_communication_risk',      'Communication Diagram - risk assessment'),
    ('15', '15_state_evidence',          'State Machine - evidence lifecycle'),
    ('16', '16_state_account',           'State Machine - account access'),
    ('17', '17_activity_risk',           'Activity Diagram - risk assessment'),
    ('18', '18_activity_reconstruction', 'Activity Diagram - chain reconstruction'),
    ('19', '19_activity_upload',         'Activity Diagram - registration, with partitions'),
    ('20', '20_timing_assistant',        'Timing Diagram - bounded waiting'),
    ('21', '21_profile_stereotypes',     'Profile Diagram - stereotype declarations'),
    ('22', '22_class_traceability',      'Class Diagram - traceability metamodel'),
    ('23', '23_activity_integrity',      'Activity Diagram - integrity verification'),
    ('24', '24_activity_state_machine',  'Activity Diagram - transition validation'),
    ('25', '25_sequence_reconstruction', 'Sequence Diagram - chain reconstruction'),
    ('26', '26_activity_assistant',      'Activity Diagram - assistant, six stages'),
]


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


def diagram_plates():
    """A plate section carrying the 26 UML figures, each with its caption."""
    parts = ['# Appendix F - UML Diagram Plates\n',
             '\nEvery diagram referenced as "Figure N" in the text. All are generated\n'
             'from versioned PlantUML source in `diagrams_v3/`, so a diagram cannot\n'
             'drift from the description it illustrates.\n\n']
    missing = []
    for num, stem, caption in DIAGRAM_ORDER:
        png = os.path.join(DIAGRAMS, stem + '.png')
        if not os.path.exists(png):
            missing.append(stem)
            continue
        rel = os.path.relpath(png, SRC).replace('\\', '/')
        parts.append(f'![]({rel})\n\n**Figure {num} - {caption}.**\n\n')
    if missing:
        print(f'  WARNING: {len(missing)} diagrams missing: {missing}')
    return ''.join(parts)


def set_table_column_widths(docx_path, usable_twips=9180):
    """
    Write an explicit grid for every table.

    pandoc emits an empty <w:tblGrid> when a table's longest content line is
    under --columns, which Word renders as a single collapsed column.
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
        each = int(usable_twips / ncol)
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
        for _ in range(ncol):
            gc = OxmlElement('w:gridCol'); gc.set(qn('w:w'), str(each)); grid.append(gc)
        table._tbl.insert(1, grid)
        for row in table.rows:
            for cell in row.cells:
                tcPr = cell._tc.get_or_add_tcPr()
                for el in tcPr.findall(qn('w:tcW')):
                    tcPr.remove(el)
                tcW = OxmlElement('w:tcW')
                tcW.set(qn('w:w'), str(each)); tcW.set(qn('w:type'), 'dxa')
                tcPr.append(tcW)
    doc.save(docx_path)
    print(f'  set explicit widths on {len(doc.tables)} tables')


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
    merged.append(diagram_plates())

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
    size = os.path.getsize(OUT) / 1024 / 1024
    print(f'\nWrote {OUT}  ({size:.1f} MB)')
    print('\nIn Word: select all (Ctrl+A), press F9, choose "Update entire table"')
    print('to build the table of contents.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
