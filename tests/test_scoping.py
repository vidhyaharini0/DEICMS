"""
Role-scoped access tests (change request CR-01 / US-28, US-29).

Verifies that non-Admin investigators only ever see aggregates and AI
answers over the cases they are members of, and that a Read-Only user with
no shared cases gets a safe empty dashboard rather than global data.
"""
import io
import struct
import zlib

import pytest

from app import create_app, db
from app.models.investigator import Investigator
from app.models.case import Case
from app.models.evidence import EvidenceItem
from app.models.custody_log import CustodyLog
from app.models.case_access import CaseAccess
from app.logic.crypto import generate_encrypted_key_pair
from app.utils import now_local


def _png():
    def chunk(tag, data):
        return (struct.pack('>I', len(data)) + tag + data
                + struct.pack('>I', zlib.crc32(tag + data) & 0xffffffff))
    ihdr = struct.pack('>IIBBBBB', 1, 1, 8, 2, 0, 0, 0)
    return (b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', ihdr)
            + chunk(b'IDAT', zlib.compress(b'\x00\xff\x00\x00')) + chunk(b'IEND', b''))


@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        'TESTING': True, 'WTF_CSRF_ENABLED': False,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SECRET_KEY': 'test', 'NVIDIA_API_KEY': ''})
    with app.app_context():
        db.create_all()
        _seed(app)
        yield app
        db.session.remove()
        db.drop_all()


def _mk_user(name, email, role):
    priv, pub = generate_encrypted_key_pair()
    u = Investigator(full_name=name, email=email, role=role,
                     public_key=pub, private_key_encrypted=priv)
    u.set_password('Passw0rd!234')
    db.session.add(u)
    return u


def _seed(app):
    admin = _mk_user('Admin User', 'admin@t.com', 'Admin')
    lead_a = _mk_user('Lead Alpha', 'lead.a@t.com', 'Lead Investigator')
    lead_b = _mk_user('Lead Bravo', 'lead.b@t.com', 'Lead Investigator')
    analyst = _mk_user('Ana Analyst', 'ana@t.com', 'Analyst')
    readonly = _mk_user('Ray ReadOnly', 'ray@t.com', 'Read-Only')
    db.session.commit()

    # Case ALPHA owned by lead_a; case BRAVO owned by lead_b
    case_a = Case(case_number='CASE-A', title='Alpha Secret Case',
                  jurisdiction='IT', status='Open', created_by_id=lead_a.id)
    case_b = Case(case_number='CASE-B', title='Bravo Hidden Case',
                  jurisdiction='IT', status='Open', created_by_id=lead_b.id)
    db.session.add_all([case_a, case_b])
    db.session.commit()

    CaseAccess.grant(case_a.id, lead_a.id, 'Owner', lead_a.id)
    CaseAccess.grant(case_a.id, analyst.id, 'Member', lead_a.id)
    CaseAccess.grant(case_b.id, lead_b.id, 'Owner', lead_b.id)
    # readonly is deliberately a member of NOTHING
    db.session.commit()

    for case, holder in [(case_a, analyst), (case_b, lead_b)]:
        ev = EvidenceItem(
            evidence_number=f'EV-{case.case_number}',
            case_id=case.id, title=f'{case.title} evidence',
            category='Image', lifecycle_state='Collected',
            file_name='f.png', file_path='/tmp/f.png',
            original_hash='a' * 64, current_hash='a' * 64,
            uploaded_by_id=holder.id, current_holder_id=holder.id)
        db.session.add(ev)
        db.session.flush()
        db.session.add(CustodyLog(
            evidence_id=ev.id, event_type='Upload', to_investigator_id=holder.id,
            timestamp=now_local(), file_hash_at_event='a' * 64,
            digital_signature='sig'))
    db.session.commit()

    app._ids = {
        'admin': admin.id, 'lead_a': lead_a.id, 'lead_b': lead_b.id,
        'analyst': analyst.id, 'readonly': readonly.id,
        'case_a': case_a.id, 'case_b': case_b.id}


def _login(app, email):
    c = app.test_client()
    c.post('/login', data={'email': email, 'password': 'Passw0rd!234'},
           follow_redirects=True)
    return c


#  accessible_case_ids helper 
class TestAccessibleCaseIds:
    def test_admin_gets_none(self, app):
        admin = db.session.get(Investigator, app._ids['admin'])
        assert CaseAccess.accessible_case_ids(admin) is None

    def test_lead_sees_only_own(self, app):
        lead_a = db.session.get(Investigator, app._ids['lead_a'])
        assert CaseAccess.accessible_case_ids(lead_a) == [app._ids['case_a']]

    def test_readonly_sees_nothing(self, app):
        ro = db.session.get(Investigator, app._ids['readonly'])
        assert CaseAccess.accessible_case_ids(ro) == []


#  Dashboard scoping 
class TestDashboardScoping:
    def test_admin_sees_both_cases(self, app):
        r = _login(app, 'admin@t.com').get('/dashboard')
        assert b'Alpha Secret Case' in r.data and b'Bravo Hidden Case' in r.data

    def test_lead_a_cannot_see_bravo(self, app):
        r = _login(app, 'lead.a@t.com').get('/dashboard')
        assert b'Alpha Secret Case' in r.data
        assert b'Bravo Hidden Case' not in r.data

    def test_analyst_cannot_see_bravo(self, app):
        r = _login(app, 'ana@t.com').get('/dashboard')
        assert b'Bravo Hidden Case' not in r.data

    def test_readonly_empty_state(self, app):
        r = _login(app, 'ray@t.com').get('/dashboard')
        assert b'No cases have been shared with you yet' in r.data
        assert b'Alpha Secret Case' not in r.data
        assert b'Bravo Hidden Case' not in r.data


#  Risk dashboard scoping 
class TestRiskScoping:
    def test_lead_a_risk_dashboard_excludes_bravo(self, app):
        r = _login(app, 'lead.a@t.com').get('/risk/dashboard')
        assert b'Bravo Hidden Case' not in r.data

    def test_evidence_risk_json_denied_cross_case(self, app):
        # lead_a asks for BRAVO's evidence risk -> 403
        bravo_ev = EvidenceItem.query.filter_by(case_id=app._ids['case_b']).first()
        r = _login(app, 'lead.a@t.com').get(f'/risk/evidence/{bravo_ev.id}/json')
        assert r.status_code == 403


#  AI assistant scoping & identity 
class TestAssistantScoping:
    def test_lead_a_cannot_list_bravo_via_chat(self, app):
        c = _login(app, 'lead.a@t.com')
        r = c.post('/assistant/chat', json={'message': 'list all cases'})
        data = r.get_json()
        # Mock backend echoes the retrieved context; Bravo must never appear
        assert 'Bravo Hidden Case' not in data['reply']

    def test_identity_question_scoped(self, app):
        c = _login(app, 'lead.a@t.com')
        r = c.post('/assistant/chat', json={'message': 'what are the cases assigned to me?'})
        data = r.get_json()
        assert data['intent'] == 'IDENTITY'
        assert 'Alpha Secret Case' in data['reply']
        assert 'Bravo Hidden Case' not in data['reply']

    def test_who_am_i_names_user(self, app):
        c = _login(app, 'lead.a@t.com')
        r = c.post('/assistant/chat', json={'message': 'who am I?'})
        data = r.get_json()
        assert 'Lead Alpha' in data['reply']


#  History isolation across logout/login 
class TestChatHistoryIsolation:
    def test_history_not_shared_between_users(self, app):
        # Lead A chats, then "logs out"; Admin logs in on the SAME client
        c = app.test_client()
        c.post('/login', data={'email': 'lead.a@t.com', 'password': 'Passw0rd!234'},
               follow_redirects=True)
        c.post('/assistant/chat', json={'message': 'my cases'})
        c.get('/logout', follow_redirects=True)

        c.post('/login', data={'email': 'admin@t.com', 'password': 'Passw0rd!234'},
               follow_redirects=True)
        page = c.get('/assistant/')
        # Admin must not see Lead A's previous turn replayed
        assert b'my cases' not in page.data.lower() or b'Start the conversation' in page.data

    def test_clear_endpoint(self, app):
        c = _login(app, 'admin@t.com')
        c.post('/assistant/chat', json={'message': 'hello'})
        r = c.post('/assistant/clear')
        assert r.get_json()['status'] == 'cleared'
