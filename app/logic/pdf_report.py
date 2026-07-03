"""
PDF Chain-of-Custody Report Generator
Category B - Third-Party Service (ReportLab).

Produces a printable, court-style chain-of-custody report for a single
evidence item (proposal 2B.7 / Increment 3 deliverable). Document layout
and PDF serialisation are handled entirely by the ReportLab library; this
module only assembles the content:

  - Case and evidence identification block
  - Cryptographic integrity summary (SHA-256 hashes, lifecycle state)
  - Fresh result of the Graph Integrity Verification Algorithm (2C.1)
  - Full custody chain table (event, from, to, timestamp, location, reason)
  - Generation footer (who generated it and when)
"""
import io
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (Paragraph, SimpleDocTemplate, Spacer, Table,
                                TableStyle)

from app.utils import now_local


def _styles():
    base = getSampleStyleSheet()
    return {
        'title': ParagraphStyle(
            'DeicmsTitle', parent=base['Title'], fontSize=16, spaceAfter=2),
        'subtitle': ParagraphStyle(
            'DeicmsSubtitle', parent=base['Normal'], fontSize=9,
            textColor=colors.grey, spaceAfter=10),
        'heading': ParagraphStyle(
            'DeicmsHeading', parent=base['Heading2'], fontSize=11,
            spaceBefore=10, spaceAfter=4),
        'body': ParagraphStyle(
            'DeicmsBody', parent=base['Normal'], fontSize=8.5, leading=11),
        'mono': ParagraphStyle(
            'DeicmsMono', parent=base['Normal'], fontSize=7,
            fontName='Courier', leading=9),
    }


def _kv_table(rows, col_widths=(45 * mm, 125 * mm)):
    """Two-column key/value table with a light grid."""
    table = Table(rows, colWidths=list(col_widths))
    table.setStyle(TableStyle([
        ('FONTSIZE', (0, 0), (-1, -1), 8.5),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.4, colors.HexColor('#cccccc')),
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f2f2f2')),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    return table


def build_custody_report_pdf(evidence, case, custody_logs, integrity_report,
                             generated_by) -> bytes:
    """
    Assembles the chain-of-custody PDF and returns it as bytes.

    Args:
        evidence:         EvidenceItem record
        case:             parent Case record
        custody_logs:     list of CustodyLog, oldest first
        integrity_report: IntegrityReport from the GraphIntegrityEngine
        generated_by:     Investigator generating the report
    """
    s = _styles()
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        leftMargin=18 * mm, rightMargin=18 * mm,
        topMargin=16 * mm, bottomMargin=16 * mm,
        title=f"Chain of Custody - {evidence.evidence_number}")

    story = [
        Paragraph('Chain-of-Custody Report', s['title']),
        Paragraph(
            'DEICMS - Digital Evidence Integrity &amp; Chain-of-Custody '
            'Management System', s['subtitle']),
    ]

    # 1. Identification
    story.append(Paragraph('1. Evidence Identification', s['heading']))
    story.append(_kv_table([
        ['Case number', case.case_number],
        ['Case title', case.title],
        ['Evidence number', evidence.evidence_number],
        ['Evidence title', evidence.title],
        ['Category', evidence.category or 'Other'],
        ['File name', evidence.file_name or 'N/A'],
        ['Lifecycle state', evidence.lifecycle_state],
        ['Risk level', f"{evidence.risk_level or 'N/A'} "
                       f"(score: {evidence.risk_score if evidence.risk_score is not None else 'N/A'})"],
    ]))

    # 2. Cryptographic integrity
    story.append(Paragraph('2. Cryptographic Integrity', s['heading']))
    story.append(_kv_table([
        ['Original SHA-256', Paragraph(evidence.original_hash or 'N/A', s['mono'])],
        ['Current SHA-256', Paragraph(evidence.current_hash or 'N/A', s['mono'])],
        ['Hashes match', 'Yes' if evidence.original_hash == evidence.current_hash else 'NO - INVESTIGATE'],
        ['Chain verdict', integrity_report.verdict],
        ['Chain completeness', f"{integrity_report.completeness_score:.1f}%"],
        ['Failures found', str(len(integrity_report.failures))],
    ]))

    if integrity_report.failures:
        story.append(Spacer(1, 4))
        story.append(Paragraph(
            'Verification failures detected by the Graph Integrity '
            'Verification Algorithm:', s['body']))
        for f in integrity_report.failures:
            story.append(Paragraph(
                f"&bull; Node {getattr(f, 'node_id', '?')} "
                f"({getattr(f, 'event_type', '?')}): "
                f"{getattr(f, 'failure_type', '?')} - "
                f"{getattr(f, 'detail', '')}", s['body']))

    # 3. Custody chain table
    story.append(Paragraph('3. Custody Chain', s['heading']))
    header = ['#', 'Event', 'From', 'To', 'Timestamp', 'Location', 'Reason', 'Signed']
    rows = [header]
    for i, log in enumerate(custody_logs, start=1):
        rows.append([
            str(i),
            log.event_type,
            (log.from_investigator.full_name if log.from_investigator else '-'),
            (log.to_investigator.full_name if log.to_investigator else '-'),
            log.timestamp.strftime('%Y-%m-%d %H:%M'),
            log.location or '-',
            Paragraph((log.reason or '-')[:200], s['body']),
            'Yes' if log.digital_signature else 'No',
        ])
    chain = Table(
        rows,
        colWidths=[7 * mm, 20 * mm, 27 * mm, 27 * mm, 25 * mm, 22 * mm, 34 * mm, 12 * mm],
        repeatRows=1)
    chain.setStyle(TableStyle([
        ('FONTSIZE', (0, 0), (-1, -1), 7.5),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.4, colors.HexColor('#cccccc')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f7f7f7')]),
        ('LEFTPADDING', (0, 0), (-1, -1), 3),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
    ]))
    story.append(chain)
    if not custody_logs:
        story.append(Paragraph('No custody events recorded.', s['body']))

    # 4. Generation footer
    story.append(Spacer(1, 10))
    story.append(Paragraph('4. Report Generation', s['heading']))
    story.append(_kv_table([
        ['Generated by', f"{generated_by.full_name} ({generated_by.role})"],
        ['Generated at', now_local().strftime('%Y-%m-%d %H:%M:%S')],
        ['Disclaimer', 'This report reflects the database state at generation '
                       'time. Verify the Ed25519 signatures and SHA-256 hashes '
                       'against the live system before relying on it in court.'],
    ]))

    doc.build(story)
    buffer.seek(0)
    return buffer.read()
