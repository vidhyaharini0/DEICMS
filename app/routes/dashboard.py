"""
Role-scoped dashboard.

Every query is filtered through CaseAccess.accessible_case_ids() so that
non-Admin users only ever see aggregates over cases they are members of
(the same rule the case list enforces). On top of the scoped data, each
role gets a tailored set of panels:

  Admin             - full system view + security alerts panel
  Lead Investigator - own-cases view + pending-actions panel
  Analyst           - own-work view + workbench panel (items they hold)
  Read-Only         - review view + recently-updated custody activity

All roles always have a "Your recent activity" panel (their own audit
records), so no dashboard is ever completely empty.
"""
from collections import OrderedDict, defaultdict
from datetime import timedelta

from flask import Blueprint, render_template
from flask_login import login_required, current_user

from app.models.case import Case
from app.models.evidence import EvidenceItem
from app.models.custody_log import CustodyLog
from app.models.audit_record import AuditRecord
from app.models.case_access import CaseAccess
from app.models.investigator import Investigator
from app.logic.risk_scoring import EvidenceRiskScorer
from app.utils import now_local

dashboard_bp = Blueprint('dashboard', __name__)


def _scoped_queries(case_ids):
    """
    Base queries filtered to the accessible cases.
    case_ids is None for Admins (no restriction) or a list of case IDs.
    """
    case_q, ev_q, audit_q = Case.query, EvidenceItem.query, AuditRecord.query
    custody_q = CustodyLog.query
    if case_ids is not None:
        ids = case_ids or [-1]  # empty access list matches nothing
        case_q = case_q.filter(Case.id.in_(ids))
        ev_q = ev_q.filter(EvidenceItem.case_id.in_(ids))
        audit_q = audit_q.filter(AuditRecord.case_id.in_(ids))
        custody_q = (custody_q
                     .join(EvidenceItem, CustodyLog.evidence_id == EvidenceItem.id)
                     .filter(EvidenceItem.case_id.in_(ids)))
    return case_q, ev_q, custody_q, audit_q


@dashboard_bp.route('/dashboard')
@login_required
def index():
    role = current_user.role
    is_admin = current_user.is_admin()
    is_lead = role == 'Lead Investigator'
    is_analyst = role == 'Analyst'
    is_readonly = role == 'Read-Only'

    case_ids = CaseAccess.accessible_case_ids(current_user)
    case_q, ev_q, custody_q, audit_q = _scoped_queries(case_ids)

    # Which panels this role sees (least privilege: monitoring charts are
    # for people whose job is monitoring; ranking is operational).
    panels = {
        'risk_chart':      is_admin or is_lead or is_analyst,
        'lifecycle_chart': True,
        'activity_chart':  is_admin or is_lead,
        'audit_chart':     is_admin or is_lead,
        'top_risk':        is_admin or is_lead or is_analyst,
        'integrity':       True,
        'recent_audits':   is_admin or is_lead or is_readonly,
        'security_alerts': is_admin,
        'pending_actions': is_lead,
        'workbench':       is_analyst,
        'review_queue':    is_readonly,
    }

    scope_word = 'Total' if is_admin else ('Shared' if is_readonly else 'My')

    #  Scoped stat cards 
    total_cases     = case_q.count()
    total_evidence  = ev_q.count()
    total_transfers = custody_q.count()
    # Non-admins additionally see audit rows about themselves (logins etc.)
    if is_admin:
        total_audits = AuditRecord.query.count()
    else:
        total_audits = audit_q.count()

    #  Recent cases (scoped, 5 most recent) 
    recent_cases = case_q.order_by(Case.created_at.desc()).limit(5).all()

    #  Risk scoring over the scoped evidence 
    scoped_evidence = ev_q.all()
    scored_evidence = []
    if panels['risk_chart'] or panels['top_risk']:
        scorer = EvidenceRiskScorer()
        for ev in scoped_evidence:
            try:
                report = scorer.score(ev)
                scored_evidence.append({
                    'evidence': ev,
                    'score':    report.final_score,
                    'level':    report.risk_level})
            except Exception:
                scored_evidence.append(
                    {'evidence': ev, 'score': 0.0, 'level': 'UNKNOWN'})
        scored_evidence.sort(key=lambda x: x['score'], reverse=True)
    top_risk_evidence = scored_evidence[:5]

    #  Integrity summary (scoped) 
    integrity_counts = {'VERIFIED': 0, 'NOT_CHECKED': 0, 'FAILED': 0}
    for ev in scoped_evidence:
        status = (getattr(ev, 'integrity_status', None) or 'NOT_CHECKED').upper()
        integrity_counts[status if status in integrity_counts else 'NOT_CHECKED'] += 1

    #  Recent audit records 
    recent_audits = []
    if panels['recent_audits']:
        source = AuditRecord.query if is_admin else audit_q
        recent_audits = source.order_by(AuditRecord.timestamp.desc()).limit(5).all()

    #  Chart datasets 
    charts = {}

    if panels['risk_chart']:
        risk_level_counts = OrderedDict(
            (lvl, 0) for lvl in ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL'])
        for item in scored_evidence:
            lvl = (item['level'] or '').upper()
            if lvl in risk_level_counts:
                risk_level_counts[lvl] += 1
        charts['risk_labels'] = list(risk_level_counts.keys())
        charts['risk_values'] = list(risk_level_counts.values())

    if panels['lifecycle_chart']:
        lifecycle_order = ['Collected', 'Submitted', 'Under Analysis',
                           'Transferred', 'Archived', 'Flagged']
        lifecycle_counts = OrderedDict((s, 0) for s in lifecycle_order)
        for ev in scoped_evidence:
            if ev.lifecycle_state in lifecycle_counts:
                lifecycle_counts[ev.lifecycle_state] += 1
        charts['lifecycle_labels'] = list(lifecycle_counts.keys())
        charts['lifecycle_values'] = list(lifecycle_counts.values())

    chart_audits = []
    if panels['audit_chart'] or panels['activity_chart']:
        chart_audits = (AuditRecord.query if is_admin else audit_q).all()

    if panels['audit_chart']:
        audit_type_order = ['Login', 'Logout', 'File Access', 'Data Modification',
                            'Integrity Check', 'State Change', 'Failed Attempt',
                            'Role Change', 'Key Generation']
        _counts = OrderedDict((t, 0) for t in audit_type_order)
        for rec in chart_audits:
            if rec.event_type in _counts:
                _counts[rec.event_type] += 1
        audit_type_counts = OrderedDict((k, v) for k, v in _counts.items() if v > 0)
        charts['audit_labels'] = list(audit_type_counts.keys())
        charts['audit_values'] = list(audit_type_counts.values())

    if panels['activity_chart']:
        window_days = 30
        today = now_local().date()
        date_axis = [today - timedelta(days=i) for i in range(window_days - 1, -1, -1)]
        succ, alert = defaultdict(int), defaultdict(int)
        since = now_local() - timedelta(days=window_days)
        for rec in chart_audits:
            if rec.timestamp and rec.timestamp >= since:
                d = rec.timestamp.date()
                if rec.result == 'Success':
                    succ[d] += 1
                else:
                    alert[d] += 1
        charts['activity_labels']  = [d.strftime('%d %b') for d in date_axis]
        charts['activity_success'] = [succ[d] for d in date_axis]
        charts['activity_alerts']  = [alert[d] for d in date_axis]
        charts['activity_title'] = ('Security Activity - Last 30 Days' if is_admin
                                    else 'My Cases Activity - Last 30 Days')

    #  Role-specific panel data 
    security_alerts = None
    if panels['security_alerts']:
        now = now_local()
        locked = [inv for inv in Investigator.query.all()
                  if inv.locked_until and inv.locked_until > now]
        failed_24h = (AuditRecord.query
                      .filter(AuditRecord.event_type == 'Failed Attempt',
                              AuditRecord.timestamp >= now - timedelta(hours=24))
                      .count())
        security_alerts = {'locked_accounts': locked, 'failed_24h': failed_24h}

    pending_actions = None
    if panels['pending_actions']:
        pending_actions = {
            'flagged': (ev_q.filter(EvidenceItem.lifecycle_state == 'Flagged')
                        .order_by(EvidenceItem.updated_at.desc()).limit(5).all()),
            'in_transfer': (ev_q.filter(EvidenceItem.lifecycle_state == 'Transferred')
                            .order_by(EvidenceItem.updated_at.desc()).limit(5).all()),
        }

    workbench = None
    if panels['workbench']:
        workbench = (ev_q.filter(EvidenceItem.current_holder_id == current_user.id)
                     .order_by(EvidenceItem.updated_at.desc()).limit(8).all())

    review_queue = None
    if panels['review_queue']:
        review_queue = (ev_q.order_by(EvidenceItem.updated_at.desc())
                        .limit(8).all())

    #  "Your recent activity" - every role, always available 
    my_activity = (AuditRecord.query
                   .filter_by(investigator_id=current_user.id)
                   .order_by(AuditRecord.timestamp.desc())
                   .limit(5).all())

    has_case_access = is_admin or bool(case_ids)

    return render_template(
        'dashboard/index.html',
        panels=panels,
        scope_word=scope_word,
        has_case_access=has_case_access,
        total_cases=total_cases,
        total_evidence=total_evidence,
        total_transfers=total_transfers,
        total_audits=total_audits,
        recent_cases=recent_cases,
        top_risk_evidence=top_risk_evidence,
        integrity_counts=integrity_counts,
        recent_audits=recent_audits,
        charts=charts,
        security_alerts=security_alerts,
        pending_actions=pending_actions,
        workbench=workbench,
        review_queue=review_queue,
        my_activity=my_activity)
