"""
Risk and anomaly views.

All aggregated views are scoped through CaseAccess.accessible_case_ids()
so investigators only ever see evidence from cases they are members of;
per-item views enforce the same case-level access check as the evidence
routes.
"""
from flask import Blueprint, render_template, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.evidence import EvidenceItem
from app.models.case_access import CaseAccess
from app.logic.risk_scoring import EvidenceRiskScorer

risk_bp = Blueprint('risk', __name__, url_prefix='/risk')


def _deny_if_no_access(evidence):
    """Redirect helper for per-item views."""
    if not CaseAccess.can_access(evidence.case_id, current_user):
        flash('You do not have access to this case.', 'danger')
        return redirect(url_for('cases.list_cases'))
    return None


@risk_bp.route('/dashboard')
@login_required
def risk_dashboard():
    """Scores the accessible evidence items and shows them ranked by risk."""
    case_ids = CaseAccess.accessible_case_ids(current_user)

    query = EvidenceItem.query
    if case_ids is not None:
        query = query.filter(EvidenceItem.case_id.in_(case_ids or [-1]))
    items = query.all()

    from app.logic.anomaly_detection import AnomalyDetectionPipeline
    pipeline = AnomalyDetectionPipeline()
    anomaly_records = pipeline.run(case_ids=case_ids)
    anomaly_map = {rec.evidence_id: rec for rec in anomaly_records}

    scorer = EvidenceRiskScorer()
    scored = []
    for ev in items:
        report = scorer.score(ev)
        rec = anomaly_map.get(ev.id)
        anomaly_score = rec.anomaly_score if rec else 0.0
        unified_score = round(0.6 * report.final_score + 0.4 * anomaly_score, 4)
        unified_level = scorer._classify(unified_score)
        scored.append({
            'evidence': ev,
            'report': report,
            'anomaly_score': anomaly_score,
            'is_anomaly': rec.is_anomaly if rec else False,
            'unified_score': unified_score,
            'unified_level': unified_level})
    # Sort by final_score descending (highest risk first)
    scored.sort(key=lambda x: x['report'].final_score, reverse=True)
    return render_template('risk/risk_dashboard.html', scored=scored)


@risk_bp.route('/evidence/<int:evidence_id>')
@login_required
def evidence_risk(evidence_id):
    """Full risk report for one evidence item (case access required)."""
    evidence = EvidenceItem.query.get_or_404(evidence_id)
    denied = _deny_if_no_access(evidence)
    if denied:
        return denied

    scorer = EvidenceRiskScorer()
    report = scorer.score(evidence)

    from app.logic.anomaly_detection import AnomalyDetectionPipeline
    pipeline = AnomalyDetectionPipeline()
    case_ids = CaseAccess.accessible_case_ids(current_user)
    anomaly_records = pipeline.run(case_ids=case_ids)
    rec = next((r for r in anomaly_records if r.evidence_id == evidence.id), None)

    anomaly_score = rec.anomaly_score if rec else 0.0
    is_anomaly = rec.is_anomaly if rec else False
    unified_score = round(0.6 * report.final_score + 0.4 * anomaly_score, 4)
    unified_level = scorer._classify(unified_score)

    return render_template('risk/evidence_risk.html', report=report, evidence=evidence, anomaly_score=anomaly_score, is_anomaly=is_anomaly, unified_score=unified_score, unified_level=unified_level)


@risk_bp.route('/evidence/<int:evidence_id>/json')
@login_required
def evidence_risk_json(evidence_id):
    """JSON endpoint for the risk report (case access required)."""
    evidence = EvidenceItem.query.get_or_404(evidence_id)
    if not CaseAccess.can_access(evidence.case_id, current_user):
        return jsonify({'error': 'You do not have access to this case.'}), 403

    scorer = EvidenceRiskScorer()
    report = scorer.score(evidence)
    return jsonify({
        'evidence_id':      report.evidence_id,
        'evidence_title':   report.evidence_title,
        'base_score':       report.base_score,
        'interaction_bonus': report.interaction_bonus,
        'final_score':      report.final_score,
        'risk_level':       report.risk_level,
        'factors': [
            {
                'name':             f.name,
                'raw_value':        f.raw_value,
                'normalised_score': f.normalised_score,
                'weight':           f.weight,
                'contribution':     f.contribution,
                'explanation':      f.explanation} for f in report.factors],
        'interactions': [
            {
                'factor_names': i.factor_names,
                'multiplier':   i.multiplier,
                'explanation':  i.explanation,} for i in report.interactions],
        'recommendations': report.recommendations,
        'computed_at':     report.computed_at.isoformat()})


@risk_bp.route('/anomaly')
@login_required
def anomaly_dashboard():
    """Runs the Isolation Forest pipeline over the accessible evidence."""
    from app.logic.anomaly_detection import AnomalyDetectionPipeline
    case_ids = CaseAccess.accessible_case_ids(current_user)
    pipeline = AnomalyDetectionPipeline()
    records = pipeline.run(case_ids=case_ids)
    return render_template('risk/anomaly_dashboard.html', records=records)
