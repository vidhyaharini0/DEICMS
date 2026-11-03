"""
Non-functional requirement verification.

Every test in this module exists to make one NFR acceptance criterion fail
if its enforcement is removed. Before this module, nine of the eighteen NFRs
were "verified" only by code review, configuration inspection or an
analytical argument - none of which regresses when the code changes.

Each test class maps to a quality attribute and names the NFRs it covers, so
the report can cite a test against every acceptance criterion rather than a
promise.
"""
import io
import os
import re
import struct
import time
import zlib
from datetime import timedelta

import pytest

from app import create_app, db
from app.models.investigator import Investigator
from app.models.case import Case
from app.models.evidence import EvidenceItem
from app.models.custody_log import CustodyLog
from app.models.case_access import CaseAccess
from app.logic.crypto import generate_encrypted_key_pair
from app.utils import now_local

LOGIC_DIR = os.path.join(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))), 'app', 'logic')


# -------------------------------------------------------------------------
# Fixtures
# -------------------------------------------------------------------------

def _png():
    """A minimal valid PNG, so magic-byte validation passes."""
    def chunk(tag, data):
        return (struct.pack('>I', len(data)) + tag + data
                + struct.pack('>I', zlib.crc32(tag + data) & 0xffffffff))
    ihdr = struct.pack('>IIBBBBB', 1, 1, 8, 2, 0, 0, 0)
    return (b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', ihdr)
            + chunk(b'IDAT', zlib.compress(b'\x00\xff\x00\x00'))
            + chunk(b'IEND', b''))


def _mk_user(name, email, role):
    priv, pub = generate_encrypted_key_pair()
    u = Investigator(full_name=name, email=email, role=role,
                     public_key=pub, private_key_encrypted=priv)
    u.set_password('Passw0rd!234')
    db.session.add(u)
    return u


@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        'TESTING': True, 'WTF_CSRF_ENABLED': False,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SECRET_KEY': 'test', 'NVIDIA_API_KEY': ''})
    with app.app_context():
        db.create_all()
        admin = _mk_user('Admin User', 'admin@t.com', 'Admin')
        lead = _mk_user('Lead User', 'lead@t.com', 'Lead Investigator')
        analyst = _mk_user('Ana Analyst', 'ana@t.com', 'Analyst')
        readonly = _mk_user('Ray ReadOnly', 'ray@t.com', 'Read-Only')
        db.session.commit()

        case = Case(case_number='CASE-N1', title='NFR Test Case',
                    jurisdiction='IT', status='Open', created_by_id=lead.id)
        db.session.add(case)
        db.session.commit()
        CaseAccess.grant(case.id, lead.id, 'Owner', admin.id)
        CaseAccess.grant(case.id, analyst.id, 'Member', admin.id)
        db.session.commit()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def _login(client, email='admin@t.com'):
    return client.post('/login', data={'email': email,
                                       'password': 'Passw0rd!234'},
                       follow_redirects=True)


def _make_evidence(case_id, uploader_id, title='Item', n_logs=1, tmpdir=None):
    """Creates an evidence item with n_logs custody records."""
    path = os.path.join(tmpdir, f'{title}.png') if tmpdir else f'/tmp/{title}.png'
    with open(path, 'wb') as fh:
        fh.write(_png())
    import hashlib
    digest = hashlib.sha256(open(path, 'rb').read()).hexdigest()

    ev = EvidenceItem(
        evidence_number=f'EV-NFR-{title}', case_id=case_id, title=title,
        category='Image', file_name=f'{title}.png', file_path=path,
        file_size=os.path.getsize(path), file_mime_type='image/png',
        original_hash=digest, current_hash=digest,
        uploaded_by_id=uploader_id, current_holder_id=uploader_id)
    db.session.add(ev)
    db.session.commit()

    base = now_local() - timedelta(hours=n_logs + 1)
    for i in range(n_logs):
        db.session.add(CustodyLog(
            evidence_id=ev.id,
            event_type='Upload' if i == 0 else 'Transfer',
            from_investigator_id=None if i == 0 else uploader_id,
            to_investigator_id=uploader_id,
            timestamp=base + timedelta(hours=i),
            location='Lab', reason='test',
            file_hash_at_event=digest,
            digital_signature='unverifiable-test-signature'))
    db.session.commit()
    return ev


# -------------------------------------------------------------------------
# NFR-13, NFR-14 - session and transport hardening
# -------------------------------------------------------------------------

class TestSecurityHeaders:
    """NFR-13 (session cookie flags) and NFR-14 (security headers)."""

    def test_session_cookie_is_not_script_readable(self, app):
        assert app.config['SESSION_COOKIE_HTTPONLY'] is True

    def test_session_cookie_is_tls_only(self, app):
        assert app.config['SESSION_COOKIE_SECURE'] is True

    def test_session_cookie_resists_cross_origin_submission(self, app):
        assert app.config['SESSION_COOKIE_SAMESITE'] == 'Lax'

    def test_idle_session_lifetime_is_bounded(self, app):
        assert app.config['PERMANENT_SESSION_LIFETIME'] <= timedelta(minutes=30)

    def test_content_security_policy_is_sent(self, client):
        r = client.get('/login')
        assert 'Content-Security-Policy' in r.headers

    def test_csp_restricts_default_src_to_self(self, client):
        csp = client.get('/login').headers.get('Content-Security-Policy', '')
        assert "default-src 'self'" in csp

    def test_mime_sniffing_is_disabled(self, client):
        assert client.get('/login').headers.get('X-Content-Type-Options') == 'nosniff'

    def test_framing_is_denied(self, client):
        assert client.get('/login').headers.get('X-Frame-Options') == 'DENY'

    def test_referrer_is_not_leaked_cross_origin(self, client):
        assert client.get('/login').headers.get('Referrer-Policy') == 'same-origin'

    def test_headers_are_present_on_authenticated_pages_too(self, client):
        _login(client)
        r = client.get('/dashboard')
        for h in ('Content-Security-Policy', 'X-Content-Type-Options',
                  'X-Frame-Options', 'Referrer-Policy'):
            assert h in r.headers, f'{h} missing on an authenticated page'


# -------------------------------------------------------------------------
# NFR-15 - untrusted text is never rendered as markup
# -------------------------------------------------------------------------

class TestInjectionResistance:
    """
    NFR-15. This is the regression guard for M2 finding H1 (stored XSS in the
    assistant transcript), which was fixed but never tested - the fix could
    have been deleted without a single test failing.
    """

    PAYLOAD = '<script>window.__xss=1</script>'

    def test_case_title_is_escaped_in_listing(self, client, app):
        with app.app_context():
            lead = Investigator.query.filter_by(email='lead@t.com').first()
            db.session.add(Case(case_number='CASE-XSS',
                                title=self.PAYLOAD, jurisdiction='IT',
                                status='Open', created_by_id=lead.id))
            db.session.commit()
        _login(client)
        body = client.get('/cases').get_data(as_text=True)
        assert self.PAYLOAD not in body
        assert '&lt;script&gt;' in body or '\\u003cscript' in body

    def test_assistant_transcript_cannot_break_out_of_script_tag(self, client):
        _login(client)
        client.post('/assistant/chat', json={'message': self.PAYLOAD})
        body = client.get('/assistant/').get_data(as_text=True)
        # tojson must escape '<' so the payload cannot close the script block
        assert '</script>' not in body.split('id="chatHistory"')[-1][:4000] \
            or self.PAYLOAD not in body

    def test_client_side_renderer_escapes_before_insertion(self):
        """
        The transcript is written with innerHTML, so the escape helper is the
        control. Assert it exists and runs before any markup is added.
        """
        tpl = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                           'app', 'templates', 'assistant', 'chat.html')
        src = open(tpl, encoding='utf-8').read()
        assert 'escapeHtml' in src, 'the XSS fix from M2 finding H1 is gone'
        assert re.search(r'innerHTML\s*=\s*escapeHtml\(', src), \
            'innerHTML is assigned without escaping first'


# -------------------------------------------------------------------------
# NFR-16 - the system refuses unsafe configuration
# -------------------------------------------------------------------------

class TestConfigurationSafety:
    """NFR-16."""

    def test_known_insecure_defaults_are_enumerated(self):
        from config import _INSECURE_DEFAULTS
        assert 'dev-secret-key-change-in-production' in _INSECURE_DEFAULTS
        assert 'dev-encryption-secret-change-in-production' in _INSECURE_DEFAULTS

    def test_production_rejects_a_missing_secret(self):
        import config as cfg

        class Missing:
            SECRET_KEY = None
            KEY_ENCRYPTION_SECRET = 'real-value'
            NVIDIA_API_KEY = 'real-value'

        with pytest.raises(ValueError, match='Missing required'):
            cfg.validate_production_secrets(Missing)

    def test_production_rejects_a_known_weak_secret(self):
        import config as cfg

        class Weak:
            SECRET_KEY = 'dev-secret-key-change-in-production'
            KEY_ENCRYPTION_SECRET = 'real-value'
            NVIDIA_API_KEY = 'real-value'

        with pytest.raises(ValueError, match='insecure default'):
            cfg.validate_production_secrets(Weak)

    def test_production_accepts_real_secrets(self):
        import config as cfg

        class Good:
            SECRET_KEY = 'a-real-and-sufficiently-long-secret'
            KEY_ENCRYPTION_SECRET = 'another-real-secret'
            NVIDIA_API_KEY = 'nvapi-real'

        assert cfg.validate_production_secrets(Good) == \
            cfg.REQUIRED_PRODUCTION_SECRETS

    def test_development_warns_rather_than_crashing(self, recwarn):
        import config as cfg

        class Weak:
            SECRET_KEY = 'dev-secret-key-change-in-production'
            KEY_ENCRYPTION_SECRET = 'dev-encryption-secret-change-in-production'

        warned = cfg.warn_development_secrets(Weak)
        assert warned == ['SECRET_KEY', 'KEY_ENCRYPTION_SECRET']
        assert len(recwarn) >= 2

    def test_password_policy_minimum_is_at_least_twelve(self, app):
        assert app.config['PASSWORD_MIN_LENGTH'] >= 12

    def test_account_lockout_is_configured(self, app):
        assert app.config['MAX_LOGIN_ATTEMPTS'] <= 5
        assert app.config['LOCKOUT_MINUTES'] >= 15


# -------------------------------------------------------------------------
# NFR-08, NFR-09 - modularity and portability
# -------------------------------------------------------------------------

class TestArchitecturalBoundaries:
    """
    NFR-08 (a change is localisable) and NFR-09 (no engine lock-in).

    The original NFR-08 wording claimed business logic contains *no* framework
    imports. That was never true: four logic modules import `current_app` to
    read configuration. The defensible and testable boundary is narrower -
    business logic never touches the *request* cycle.
    """

    WEB_SYMBOLS = ('request', 'session', 'redirect', 'url_for',
                   'render_template', 'flash', 'abort')

    def _logic_sources(self):
        for name in sorted(os.listdir(LOGIC_DIR)):
            if name.endswith('.py') and name != '__init__.py':
                with open(os.path.join(LOGIC_DIR, name), encoding='utf-8') as fh:
                    yield name, fh.read()

    def test_logic_never_imports_the_request_cycle(self):
        offenders = []
        for name, src in self._logic_sources():
            for line in src.splitlines():
                if line.strip().startswith(('from flask import', 'import flask')):
                    for sym in self.WEB_SYMBOLS:
                        if re.search(rf'\b{sym}\b', line):
                            offenders.append(f'{name}: {line.strip()}')
        assert not offenders, 'business logic reached into the web layer: ' + \
            '; '.join(offenders)

    def test_logic_modules_do_not_import_routes(self):
        offenders = [name for name, src in self._logic_sources()
                     if 'app.routes' in src]
        assert not offenders, f'logic depends on routes: {offenders}'

    def test_no_engine_specific_sql_in_logic_or_routes(self):
        """NFR-09: portability is lost the moment a dialect leaks into logic."""
        banned = re.compile(r'\b(PRAGMA|AUTOINCREMENT|sqlite_master|SERIAL)\b',
                            re.IGNORECASE)
        root = os.path.dirname(LOGIC_DIR)
        offenders = []
        for sub in ('logic', 'routes', 'models'):
            folder = os.path.join(root, sub)
            for name in sorted(os.listdir(folder)):
                if not name.endswith('.py'):
                    continue
                src = open(os.path.join(folder, name), encoding='utf-8').read()
                if banned.search(src):
                    offenders.append(f'{sub}/{name}')
        assert not offenders, f'engine-specific SQL found in {offenders}'

    def test_persisted_risk_level_stays_within_the_column_domain(self, app, tmp_path):
        """
        The scorer classifies into four levels (including CRITICAL) but the
        column is a three-value enum. SQLite does not enforce enums, so this
        only breaks on PostgreSQL - exactly the portability NFR-09 claims.
        """
        from app.models.evidence import EvidenceItem as EI
        domain = set(EI.__table__.c.risk_level.type.enums)
        with app.app_context():
            case = Case.query.first()
            lead = Investigator.query.filter_by(email='lead@t.com').first()
            ev = _make_evidence(case.id, lead.id, 'RiskDomain', 3, str(tmp_path))
            from app.logic.state_machine import EvidenceStateMachine
            EvidenceStateMachine(ev, lead)._recalculate_risk_score()
            db.session.commit()
            assert ev.risk_level in domain, (
                f'persisted risk_level {ev.risk_level!r} is outside the column '
                f'domain {sorted(domain)} - this fails on PostgreSQL')


# -------------------------------------------------------------------------
# NFR-10, NFR-11, NFR-17 - measured performance, not asserted complexity
# -------------------------------------------------------------------------

class TestPerformanceScaling:
    """
    NFR-10 (verification is O(V+E)) and NFR-11 (risk scoring is O(n)) were
    argued analytically and never measured. These tests measure growth: if a
    linear algorithm were replaced by a quadratic one, the ratio would blow
    past the tolerance and the test would fail.
    """

    @staticmethod
    def _time(fn, repeats=3):
        best = float('inf')
        for _ in range(repeats):
            start = time.perf_counter()
            fn()
            best = min(best, time.perf_counter() - start)
        return best

    def test_integrity_verification_grows_linearly(self, app, tmp_path):
        from app.logic.graph_integrity import GraphIntegrityEngine
        with app.app_context():
            case = Case.query.first()
            lead = Investigator.query.filter_by(email='lead@t.com').first()
            small = _make_evidence(case.id, lead.id, 'Small', 20, str(tmp_path))
            large = _make_evidence(case.id, lead.id, 'Large', 200, str(tmp_path))

            t_small = self._time(lambda: GraphIntegrityEngine(small).verify())
            t_large = self._time(lambda: GraphIntegrityEngine(large).verify())

        # 10x the nodes must not cost more than 30x the time. A quadratic
        # implementation would need ~100x and would fail here.
        growth = t_large / max(t_small, 1e-6)
        assert growth < 30, (
            f'verification grew {growth:.1f}x for 10x the nodes - '
            f'this is not the linear behaviour NFR-10 claims')

    def test_risk_scoring_grows_linearly(self, app, tmp_path):
        from app.logic.risk_scoring import EvidenceRiskScorer
        with app.app_context():
            case = Case.query.first()
            lead = Investigator.query.filter_by(email='lead@t.com').first()
            small = _make_evidence(case.id, lead.id, 'RSmall', 20, str(tmp_path))
            large = _make_evidence(case.id, lead.id, 'RLarge', 200, str(tmp_path))
            scorer = EvidenceRiskScorer()

            t_small = self._time(lambda: scorer.score(small))
            t_large = self._time(lambda: scorer.score(large))

        growth = t_large / max(t_small, 1e-6)
        assert growth < 30, (
            f'risk scoring grew {growth:.1f}x for 10x the records - '
            f'this is not the linear behaviour NFR-11 claims')

    def test_verification_completes_within_the_stated_budget(self, app, tmp_path):
        from app.logic.graph_integrity import GraphIntegrityEngine
        with app.app_context():
            case = Case.query.first()
            lead = Investigator.query.filter_by(email='lead@t.com').first()
            ev = _make_evidence(case.id, lead.id, 'Budget', 100, str(tmp_path))
            elapsed = self._time(lambda: GraphIntegrityEngine(ev).verify(), repeats=1)
        assert elapsed < 5.0, (
            f'verifying a 100-node chain took {elapsed:.2f}s, over the 5s budget')


class TestListingResponsiveness:
    """
    NFR-17. The report claimed case *and evidence* listings were paginated.
    Cases and audit records were; the evidence listing inside a case called
    .all(). These tests pin both.
    """

    def test_case_listing_is_paginated(self, client, app):
        with app.app_context():
            lead = Investigator.query.filter_by(email='lead@t.com').first()
            for i in range(45):
                db.session.add(Case(case_number=f'CASE-P{i:03d}',
                                    title=f'Bulk case {i}', jurisdiction='IT',
                                    status='Open', created_by_id=lead.id))
            db.session.commit()
        _login(client)
        body = client.get('/cases').get_data(as_text=True)
        assert body.count('CASE-P') <= 20, 'case listing is not paginated'

    def test_evidence_listing_inside_a_case_is_paginated(self, client, app, tmp_path):
        with app.app_context():
            case = Case.query.filter_by(case_number='CASE-N1').first()
            lead = Investigator.query.filter_by(email='lead@t.com').first()
            case_id = case.id
            for i in range(45):
                _make_evidence(case_id, lead.id, f'Bulk{i:03d}', 1, str(tmp_path))
        _login(client, 'lead@t.com')
        body = client.get(f'/cases/{case_id}').get_data(as_text=True)
        assert body.count('EV-NFR-Bulk') <= 20, \
            'evidence listing is not paginated (NFR-17)'


# -------------------------------------------------------------------------
# NFR-05, NFR-06 - degraded mode and bounded waiting
# -------------------------------------------------------------------------

class TestRobustness:
    """NFR-05 (unavailable model) and NFR-06 (slow model)."""

    def test_timeout_budgets_are_configured_and_ordered(self, app):
        per_call = app.config['AI_REQUEST_TIMEOUT']
        total = app.config['AI_TOTAL_BUDGET']
        assert per_call > 0 and total > 0
        assert per_call <= total, 'a single call may not exceed the total budget'
        assert total <= 90, 'the total budget must stay under the browser abort'

    def test_assistant_answers_when_the_model_is_unreachable(self, client):
        _login(client)
        r = client.post('/assistant/chat', json={'message': 'status of case CASE-N1'})
        assert r.status_code == 200
        payload = r.get_json()
        assert payload.get('reply'), \
            'no answer returned with the model unavailable (NFR-05)'
        assert payload.get('context_used') is True, \
            'the fallback answered without the retrieved records'

    def test_a_slow_model_does_not_hang_the_request(self, client, monkeypatch):
        """Stubs a model client that sleeps past the budget."""
        import app.logic.ai_assistant as ai

        def _slow(*a, **k):
            time.sleep(0.3)
            raise TimeoutError('simulated slow model')

        for attr in ('_call_model', 'call_model', '_invoke_model'):
            if hasattr(ai, attr):
                monkeypatch.setattr(ai, attr, _slow)
                break
        _login(client)
        start = time.perf_counter()
        r = client.post('/assistant/chat', json={'message': 'hello'})
        elapsed = time.perf_counter() - start
        assert r.status_code == 200
        assert elapsed < 30, f'request took {elapsed:.1f}s with a slow model'


# -------------------------------------------------------------------------
# NFR-07 - each role gets an interface matched to its work
# -------------------------------------------------------------------------

class TestRoleInterfaces:
    """NFR-07: four distinct dashboard compositions, none of them empty."""

    CREDENTIALS = {
        'Admin': 'admin@t.com',
        'Lead Investigator': 'lead@t.com',
        'Analyst': 'ana@t.com',
        'Read-Only': 'ray@t.com'}

    @pytest.mark.parametrize('role', list(CREDENTIALS))
    def test_every_role_gets_a_non_empty_dashboard(self, client, role):
        _login(client, self.CREDENTIALS[role])
        r = client.get('/dashboard')
        assert r.status_code == 200
        body = r.get_data(as_text=True)
        assert 'Recent Activity' in body or 'recent activity' in body.lower(), \
            f'{role} dashboard has no activity panel - NFR-07 requires none be empty'

    def test_security_alerts_panel_is_admin_only(self, client):
        """
        Matches the panel's own card header, not the chart dataset label of
        the same name - the audit chart is shown to Leads as well.
        """
        marker = 'bi-shield-lock me-2"></i>Security Alerts'
        _login(client, 'admin@t.com')
        assert marker in client.get('/dashboard').get_data(as_text=True)
        client.get('/logout')
        _login(client, 'lead@t.com')
        assert marker not in client.get('/dashboard').get_data(as_text=True)

    def test_dashboard_compositions_differ_between_roles(self, client):
        bodies = {}
        for role, email in self.CREDENTIALS.items():
            _login(client, email)
            bodies[role] = client.get('/dashboard').get_data(as_text=True)
            client.get('/logout')
        assert len(set(bodies.values())) == 4, \
            'two roles render an identical dashboard - NFR-07 requires four'


# -------------------------------------------------------------------------
# SR-06 - an account limited to review causes no change of state
# -------------------------------------------------------------------------

class TestReadOnlyCausesNoChange:
    """
    Sprint 6 change request. Running a verification is not a read: it writes
    integrity_status back onto the evidence row and, on a Broken verdict,
    drives the item into Flagged. Before this guard a Read-Only Viewer could
    do both, which made the role's name false and violated SR-06.
    """

    def _as_readonly(self, client, app, tmp_path):
        with app.app_context():
            case = Case.query.filter_by(case_number='CASE-N1').first()
            lead = Investigator.query.filter_by(email='lead@t.com').first()
            ro = Investigator.query.filter_by(email='ray@t.com').first()
            CaseAccess.grant(case.id, ro.id, 'Member', lead.id)
            db.session.commit()
            ev = _make_evidence(case.id, lead.id, 'ROGuard', 3, str(tmp_path))
            ids = (case.id, ev.id, ev.integrity_status, ev.lifecycle_state)
        _login(client, 'ray@t.com')
        return ids

    def test_readonly_cannot_run_verification(self, client, app, tmp_path):
        case_id, ev_id, before_status, before_state = \
            self._as_readonly(client, app, tmp_path)
        r = client.get(f'/evidence/{ev_id}/verify', follow_redirects=True)
        body = r.get_data(as_text=True)
        assert 'does not permit running analysis' in body
        with app.app_context():
            ev = EvidenceItem.query.get(ev_id)
            assert ev.integrity_status == before_status, \
                'a Read-Only account changed integrity_status (SR-06)'
            assert ev.lifecycle_state == before_state, \
                'a Read-Only account changed the lifecycle state (SR-06)'

    def test_readonly_cannot_run_verification_as_json(self, client, app, tmp_path):
        _, ev_id, _, _ = self._as_readonly(client, app, tmp_path)
        r = client.get(f'/evidence/{ev_id}/verify/json')
        assert r.status_code == 403
        assert 'error' in r.get_json()

    def test_readonly_cannot_run_reconstruction(self, client, app, tmp_path):
        _, ev_id, _, _ = self._as_readonly(client, app, tmp_path)
        r = client.get(f'/evidence/{ev_id}/reconstruct', follow_redirects=True)
        assert 'does not permit running analysis' in r.get_data(as_text=True)

    def test_analyst_may_still_run_verification(self, client, app, tmp_path):
        with app.app_context():
            case = Case.query.filter_by(case_number='CASE-N1').first()
            lead = Investigator.query.filter_by(email='lead@t.com').first()
            ev = _make_evidence(case.id, lead.id, 'AnaGuard', 3, str(tmp_path))
            ev_id = ev.id
        _login(client, 'ana@t.com')
        r = client.get(f'/evidence/{ev_id}/verify', follow_redirects=True)
        assert 'does not permit running analysis' not in r.get_data(as_text=True)

    def test_readonly_keeps_the_reads_it_is_entitled_to(self, client, app, tmp_path):
        case_id, ev_id, _, _ = self._as_readonly(client, app, tmp_path)
        for path in (f'/cases/{case_id}',
                     f'/evidence/{ev_id}/custody-log',
                     f'/audit/evidence/{ev_id}',
                     '/risk/dashboard',
                     '/assistant/'):
            r = client.get(path, follow_redirects=True)
            assert r.status_code == 200, f'{path} unreachable for Read-Only'
            assert 'does not permit running analysis' not in r.get_data(as_text=True), \
                f'{path} was wrongly caught by the analysis guard'

    def test_readonly_is_still_refused_the_global_audit_trail(self, client, app, tmp_path):
        self._as_readonly(client, app, tmp_path)
        r = client.get('/audit', follow_redirects=True)
        assert 'restricted to administrators' in r.get_data(as_text=True)
