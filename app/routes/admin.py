"""
Admin-only routes for user management and system settings.
Only investigators with the 'Admin' role can access these.
"""
import json
import os
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from app import db
from app.models.investigator import Investigator
from app.models.audit_record import AuditRecord
from app.logic.crypto import generate_key_pair, encrypt_private_key
from app.logic.validators import validate_password_strength

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def _admin_guard():
    """Returns a redirect response if the current user is not an Admin, else None."""
    if not current_user.is_authenticated or not current_user.is_admin():
        flash('Access denied. Admin role required.', 'danger')
        return redirect(url_for('dashboard.index'))
    return None

@admin_bp.route('/users')
@login_required
def list_users():
    """Show all investigator accounts. Admin only."""
    guard = _admin_guard()
    if guard:
        return guard

    investigators = Investigator.query.order_by(Investigator.created_at.desc()).all()
    return render_template('admin/users.html', investigators=investigators)

@admin_bp.route('/users/new', methods=['GET', 'POST'])
@login_required
def create_user():
    """Create a new investigator account. Admin only."""
    guard = _admin_guard()
    if guard:
        return guard

    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        role = request.form.get('role', 'Analyst')

        # Validation
        if not full_name or not email or not password:
            flash('All fields are required.', 'danger')
            return render_template('admin/create_user.html')

        pw_errors = validate_password_strength(password)
        if pw_errors:
            flash('Password must ' + '; '.join(pw_errors) + '.', 'danger')
            return render_template('admin/create_user.html')

        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('admin/create_user.html')

        if Investigator.query.filter_by(email=email).first():
            flash('An account with this email already exists.', 'danger')
            return render_template('admin/create_user.html')

        # Valid roles only
        valid_roles = ['Admin', 'Lead Investigator', 'Analyst', 'Read-Only']
        if role not in valid_roles:
            flash('Invalid role selected.', 'danger')
            return render_template('admin/create_user.html')

        # Create with key pair
        private_pem, public_pem = generate_key_pair()
        investigator = Investigator(
            full_name=full_name,
            email=email,
            role=role,
            public_key=public_pem,
            private_key_encrypted=encrypt_private_key(private_pem))
        investigator.set_password(password)

        db.session.add(investigator)
        db.session.commit()

        audit = AuditRecord(
            event_type='Data Modification',
            investigator_id=current_user.id,
            description=f'Admin {current_user.full_name} created account: {email} [{role}]',
            ip_address=request.remote_addr,
            result='Success')
        db.session.add(audit)
        db.session.commit()

        flash(f'Account for {full_name} created successfully.', 'success')
        return redirect(url_for('admin.list_users'))

    return render_template('admin/create_user.html')


@admin_bp.route('/users/<int:user_id>/toggle-active', methods=['POST'])
@login_required
def toggle_active(user_id):
    """Activate or deactivate an investigator account. Admin only."""
    guard = _admin_guard()
    if guard:
        return guard

    if user_id == current_user.id:
        flash('You cannot deactivate your own account.', 'danger')
        return redirect(url_for('admin.list_users'))

    investigator = Investigator.query.get_or_404(user_id)
    investigator.is_active = not investigator.is_active
    action = 'activated' if investigator.is_active else 'deactivated'

    # Clear lockout when admin re-activates an account
    if investigator.is_active:
        investigator.reset_login_attempts()

    audit = AuditRecord(
        event_type='Role Change',
        investigator_id=current_user.id,
        description=f'Admin {current_user.full_name} {action} account: {investigator.email}',
        ip_address=request.remote_addr,
        result='Success')
    db.session.add(audit)
    db.session.commit()

    flash(f'Account for {investigator.full_name} has been {action}.', 'success')
    return redirect(url_for('admin.list_users'))


@admin_bp.route('/users/<int:user_id>/unlock', methods=['POST'])
@login_required
def unlock_account(user_id):
    """Manually unlock a locked-out account. Admin only."""
    guard = _admin_guard()
    if guard:
        return guard

    investigator = Investigator.query.get_or_404(user_id)
    investigator.reset_login_attempts()

    audit = AuditRecord(
        event_type='Role Change',
        investigator_id=current_user.id,
        description=f'Admin {current_user.full_name} manually unlocked account: {investigator.email}',
        ip_address=request.remote_addr,
        result='Success')
    db.session.add(audit)
    db.session.commit()

    flash(f'Account for {investigator.full_name} has been unlocked.', 'success')
    return redirect(url_for('admin.list_users'))


@admin_bp.route('/users/<int:user_id>/change-role', methods=['POST'])
@login_required
def change_role(user_id):
    """Change an investigator's role. Admin only."""
    guard = _admin_guard()
    if guard:
        return guard

    if user_id == current_user.id:
        flash('You cannot change your own role.', 'danger')
        return redirect(url_for('admin.list_users'))

    investigator = Investigator.query.get_or_404(user_id)
    new_role = request.form.get('role', '')
    valid_roles = ['Admin', 'Lead Investigator', 'Analyst', 'Read-Only']
    if new_role not in valid_roles:
        flash('Invalid role.', 'danger')
        return redirect(url_for('admin.list_users'))

    old_role = investigator.role
    investigator.role = new_role

    audit = AuditRecord(
        event_type='Role Change',
        investigator_id=current_user.id,
        description=(
            f'Admin {current_user.full_name} changed role of {investigator.email}: '
            f'{old_role} -> {new_role}'
        ),
        ip_address=request.remote_addr,
        result='Success')
    db.session.add(audit)
    db.session.commit()

    flash(f"Role for {investigator.full_name} changed to '{new_role}'.", 'success')
    return redirect(url_for('admin.list_users'))


#  Risk scoring configuration
def risk_settings_path():
    """Path of the JSON file that persists admin risk-scoring overrides."""
    return os.path.join(os.path.dirname(current_app.root_path), 'risk_settings.json')


@admin_bp.route('/risk-settings', methods=['GET', 'POST'])
@login_required
def risk_settings():
    """
    View and edit the risk-scoring factor weights and classification
    thresholds (proposal 2C.2: 'the weights are configurable by
    administrators'). Overrides are persisted to risk_settings.json and
    re-loaded on application startup; weights are re-normalised to sum
    to 1.0 before use, so admins can enter any relative importance.
    """
    guard = _admin_guard()
    if guard:
        return guard

    from app.logic.risk_scoring import _WEIGHTS, _THRESHOLDS, get_weights, get_thresholds

    if request.method == 'POST':
        new_weights = {}
        new_thresholds = {}
        errors = []

        for name in _WEIGHTS:
            raw = request.form.get(f'weight_{name}', '').strip()
            try:
                value = float(raw)
                if value < 0:
                    raise ValueError
                new_weights[name] = value
            except ValueError:
                errors.append(f"Weight for '{name}' must be a non-negative number.")

        for level in _THRESHOLDS:
            raw = request.form.get(f'threshold_{level}', '').strip()
            try:
                value = float(raw)
                if not 0.0 < value < 1.0:
                    raise ValueError
                new_thresholds[level] = value
            except ValueError:
                errors.append(f"Threshold '{level}' must be a number between 0 and 1.")

        if not errors and sum(new_weights.values()) <= 0:
            errors.append('At least one weight must be greater than zero.')
        if not errors and not (new_thresholds['LOW'] < new_thresholds['MEDIUM'] < new_thresholds['HIGH']):
            errors.append('Thresholds must be strictly increasing: LOW < MEDIUM < HIGH.')

        if errors:
            for e in errors:
                flash(e, 'danger')
        else:
            # Apply to the running app and persist to disk
            current_app.config['RISK_WEIGHTS'] = new_weights
            current_app.config['RISK_THRESHOLDS'] = new_thresholds
            with open(risk_settings_path(), 'w') as fh:
                json.dump({'weights': new_weights, 'thresholds': new_thresholds}, fh, indent=2)

            audit = AuditRecord(
                event_type='Data Modification',
                investigator_id=current_user.id,
                description=(
                    f'Admin {current_user.full_name} updated risk-scoring settings: '
                    f'weights={new_weights}, thresholds={new_thresholds}'),
                ip_address=request.remote_addr,
                result='Success')
            db.session.add(audit)
            db.session.commit()
            flash('Risk scoring settings saved. New scores will use the updated weights.', 'success')
            return redirect(url_for('admin.risk_settings'))

    return render_template(
        'admin/risk_settings.html',
        weights=get_weights(),
        thresholds=get_thresholds(),
        default_weights=_WEIGHTS,
        default_thresholds=_THRESHOLDS)
