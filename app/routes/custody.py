"""
Custody routes - Increment 2
Now includes:
  - Digital signature on every custody transfer (Ed25519)
  - State machine transition on transfer
  - Graph Integrity Verification endpoint
  - Chain Reconstruction endpoint
  - Evidence state change endpoint
"""
import json
from datetime import datetime, timezone, timedelta
from flask import (Blueprint, render_template, redirect, url_for,
                   flash, request, jsonify)
from flask_login import login_required, current_user
from app import db, limiter
from app.models.evidence import EvidenceItem
from app.models.investigator import Investigator
from app.models.custody_log import CustodyLog
from app.models.audit_record import AuditRecord
from app.models.case_access import CaseAccess
from app.utils import now_local

custody_bp = Blueprint('custody', __name__)

def _deny_if_no_case_access(evidence):
    """
    Return a redirect response if the current user lacks access to the
    evidence's parent case, else None. Admins always pass.
    """
    if not CaseAccess.can_access(evidence.case_id, current_user):
        flash('You do not have access to this case.', 'danger')
        return redirect(url_for('cases.list_cases'))
    return None


def _build_transfer_payload(evidence_id: int, event_type: str,
                             timestamp: datetime, from_id, to_id,
                             file_hash: str) -> bytes:
    """
    Build the canonical byte payload that gets signed for a custody event.
    Must match exactly what GraphIntegrityEngine._build_payload() reconstructs.
    """
    payload_dict = {
        'evidence_id': evidence_id,
        'event_type': event_type,
        'timestamp': timestamp.isoformat(),
        'from_investigator_id': from_id,
        'to_investigator_id': to_id,
        'file_hash': file_hash
    }
    return json.dumps(payload_dict, sort_keys=True).encode('utf-8')

@custody_bp.route('/evidence/<int:evidence_id>/transfer', methods=['GET', 'POST'])
@login_required
def transfer_evidence(evidence_id):
    """
    Record a custody transfer with:
    - State machine validation (only valid transitions allowed)
    - Ed25519 digital signature by the outgoing investigator
    - Audit log entry
    """
    evidence = EvidenceItem.query.get_or_404(evidence_id)
    _denied = _deny_if_no_case_access(evidence)
    if _denied:
        return _denied

    if evidence.current_holder_id != current_user.id and not current_user.is_admin():
        flash('Only the current holder can transfer this evidence item.', 'danger')
        return redirect(url_for('evidence.view_evidence',
                                case_id=evidence.case_id,
                                evidence_id=evidence_id))

    investigators = (Investigator.query
                     .filter_by(is_active=True)
                     .filter(Investigator.id != current_user.id)
                     .all())

    if request.method == 'POST':
        to_investigator_id = request.form.get('to_investigator_id', type=int)
        reason = request.form.get('reason', '').strip()
        location = request.form.get('location', '').strip()
        justification = request.form.get('justification', '').strip()

        if not to_investigator_id:
            flash('Please select a recipient investigator.', 'danger')
            return render_template('custody/transfer.html',
                                   evidence=evidence,
                                   investigators=investigators)

        to_investigator = Investigator.query.get(to_investigator_id)
        if not to_investigator:
            flash('Selected investigator not found.', 'danger')
            return render_template('custody/transfer.html',
                                   evidence=evidence,
                                   investigators=investigators)

        transfer_time = now_local()

        payload = _build_transfer_payload(
            evidence_id=evidence.id,
            event_type='Transfer',
            timestamp=transfer_time,
            from_id=current_user.id,
            to_id=to_investigator_id,
            file_hash=evidence.current_hash)

        signature_hex = None
        if current_user.private_key_encrypted:
            from app.logic.crypto import sign_payload
            try:
                signature_hex = sign_payload(
                    current_user.private_key_encrypted, payload)
            except Exception as e:
                flash(f'Warning: Could not sign transfer: {e}', 'warning')

        # The digital_signature column is NOT NULL by design (every custody
        # record must carry a signature slot). When signing is unavailable or
        # fails, store the 'UNSIGNED' sentinel - the graph verifier treats an
        # unsigned link as unverified rather than crashing the transfer.
        signed_ok = signature_hex is not None
        if signature_hex is None:
            signature_hex = 'UNSIGNED'

        from app.logic.state_machine import EvidenceStateMachine
        sm = EvidenceStateMachine(evidence, current_user)
        result = sm.transition_to('Transferred', justification=justification or reason)

        if not result:
            db.session.commit()
            flash(f'Transfer rejected: {result.message}', 'danger')
            return redirect(url_for('evidence.view_evidence', case_id=evidence.case_id, evidence_id=evidence_id))

        evidence.current_holder_id = to_investigator_id

        custody_entry = CustodyLog(
            evidence_id=evidence.id,
            event_type='Transfer',
            from_investigator_id=current_user.id,
            to_investigator_id=to_investigator_id,
            timestamp=transfer_time,
            location=location,
            reason=reason,
            file_hash_at_event=evidence.current_hash,
            digital_signature=signature_hex,
            notes=f'Signed transfer from {current_user.full_name} to {to_investigator.full_name}')
        db.session.add(custody_entry)

        audit = AuditRecord(
            event_type='Data Modification',
            investigator_id=current_user.id,
            evidence_id=evidence.id,
            case_id=evidence.case_id,
            description=(
                f'Evidence {evidence.evidence_number} transferred '
                f'from {current_user.full_name} to {to_investigator.full_name}. '
                f'Signed: {"Yes" if signed_ok else "No"}'),
            ip_address=request.remote_addr,
            result='Success')
        db.session.add(audit)
        db.session.commit()

        flash(
            f'Evidence {evidence.evidence_number} transferred to '
            f'{to_investigator.full_name} successfully. '
            f'{"Transfer digitally signed." if signed_ok else "Transfer stored UNSIGNED."}',
            'success')
        return redirect(url_for('evidence.view_evidence',
                                case_id=evidence.case_id,
                                evidence_id=evidence_id))

    return render_template('custody/transfer.html',
                           evidence=evidence,
                           investigators=investigators)

@custody_bp.route('/evidence/<int:evidence_id>/custody-log')
@login_required
def view_custody_log(evidence_id):
    """View the full custody log for an evidence item."""
    evidence = EvidenceItem.query.get_or_404(evidence_id)
    _denied = _deny_if_no_case_access(evidence)
    if _denied:
        return _denied
    custody_logs = (evidence.custody_logs
                    .order_by(CustodyLog.timestamp.asc())
                    .all())
    return render_template('custody/log.html',
                           evidence=evidence,
                           custody_logs=custody_logs)

@custody_bp.route('/evidence/<int:evidence_id>/verify')
@login_required
@limiter.limit('30 per minute')  # graph verification re-hashes the file
def verify_integrity(evidence_id):
    """
    Run the Graph Integrity Verification Algorithm for an evidence item.
    Returns an HTML report page showing the full verification result.
    """
    evidence = EvidenceItem.query.get_or_404(evidence_id)
    _denied = _deny_if_no_case_access(evidence)
    if _denied:
        return _denied

    from app.logic.graph_integrity import GraphIntegrityEngine
    engine = GraphIntegrityEngine(evidence)
    report = engine.verify()

    # Persist the verdict onto the evidence row so the risk-scoring integrity
    # factor (its highest-weighted signal) reflects the latest check.
    # Intact -> VERIFIED, Broken -> FAILED, anything else -> NOT_CHECKED.
    if report.verdict == 'Intact':
        evidence.integrity_status = 'VERIFIED'
    elif report.verdict == 'Broken':
        evidence.integrity_status = 'FAILED'
    else:
        evidence.integrity_status = 'NOT_CHECKED'

    audit = AuditRecord(
        event_type='Integrity Check',
        investigator_id=current_user.id,
        evidence_id=evidence.id,
        case_id=evidence.case_id,
        description=(
            f'Graph integrity verification run on {evidence.evidence_number}. '
            f'Verdict: {report.verdict}. '
            f'Completeness: {report.completeness_score}%.'),
        ip_address=request.remote_addr,
        result='Success' if report.verdict == 'Intact' else 'Warning',
        integrity_check_result=json.dumps(report.to_dict()))
    db.session.add(audit)

    if report.verdict == 'Broken' and evidence.lifecycle_state != 'Flagged':
        from app.logic.state_machine import EvidenceStateMachine
        sm = EvidenceStateMachine(evidence, current_user)
        # Automated safety action: flag regardless of the triggering user's role
        # (an Analyst running a check on a broken item must still get it flagged,
        # and we must not write a misleading "rejected transition" audit row).
        sm.transition_to(
            'Flagged',
            justification='Auto-flagged: integrity verification failed.',
            system=True)
    db.session.commit()

    return render_template('custody/integrity_report.html', evidence=evidence, report=report)

@custody_bp.route('/evidence/<int:evidence_id>/verify/json')
@login_required
def verify_integrity_json(evidence_id):
    """Return the integrity verification result as JSON."""
    evidence = EvidenceItem.query.get_or_404(evidence_id)
    _denied = _deny_if_no_case_access(evidence)
    if _denied:
        return _denied
    from app.logic.graph_integrity import GraphIntegrityEngine
    engine = GraphIntegrityEngine(evidence)
    report = engine.verify()
    return jsonify(report.to_dict())

@custody_bp.route('/evidence/<int:evidence_id>/reconstruct')
@login_required
@limiter.limit('30 per minute')  # heuristic search over the custody graph
def reconstruct_chain(evidence_id):
    """Run the Custody Chain Reconstruction Algorithm."""
    evidence = EvidenceItem.query.get_or_404(evidence_id)
    _denied = _deny_if_no_case_access(evidence)
    if _denied:
        return _denied

    from app.logic.chain_reconstruction import ChainReconstructionEngine
    engine = ChainReconstructionEngine(evidence)
    report = engine.reconstruct()

    audit = AuditRecord(
        event_type='Integrity Check',
        investigator_id=current_user.id,
        evidence_id=evidence.id,
        case_id=evidence.case_id,
        description=(
            f'Chain reconstruction run on {evidence.evidence_number}. '
            f'Confidence: {report.chain_confidence_score}%. '
            f'Unresolved gaps: {report.unresolved_gaps}.'),
        ip_address=request.remote_addr,
        result='Success' if report.unresolved_gaps == 0 else 'Warning')
    db.session.add(audit)
    db.session.commit()

    return render_template('custody/reconstruction_report.html', evidence=evidence, report=report)

@custody_bp.route('/evidence/<int:evidence_id>/change-state', methods=['GET', 'POST'])
@login_required
def change_state(evidence_id):
    """Manually trigger a lifecycle state transition via the state machine."""
    evidence = EvidenceItem.query.get_or_404(evidence_id)
    _denied = _deny_if_no_case_access(evidence)
    if _denied:
        return _denied

    from app.logic.state_machine import EvidenceStateMachine
    sm = EvidenceStateMachine(evidence, current_user)
    available = sm.get_available_transitions()

    if request.method == 'POST':
        target_state = request.form.get('target_state', '')
        justification = request.form.get('justification', '').strip()

        result = sm.transition_to(target_state, justification=justification)

        # transition_to() makes no changes to the evidence on the failure path -
        # it only appends a rejection audit record. Commit either way so the
        # rejected-transition attempt is preserved in the audit trail (the
        # proposal requires rejections to be logged); a rollback here would
        # silently discard that audit row.
        db.session.commit()
        flash(result.message, 'success' if result else 'danger')

        return redirect(url_for('evidence.view_evidence', case_id=evidence.case_id, evidence_id=evidence_id))

    return render_template('custody/change_state.html', evidence=evidence, available_transitions=available)