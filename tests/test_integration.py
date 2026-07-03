"""
End-to-end route integration tests.

Exercises the full web workflow through the Flask test client:
login -> create case -> upload evidence (magic-byte validated, encrypted
at rest) -> transfer custody (Ed25519-signed) -> change lifecycle state ->
verify integrity -> reconstruct chain -> export signed ZIP -> download
chain-of-custody PDF -> edit admin risk settings.
"""
import io
import os
import struct
import zlib

import pytest

from app import create_app, db
from app.models.investigator import Investigator
from app.models.case import Case
from app.models.evidence import EvidenceItem
from app.models.custody_log import CustodyLog


def _minimal_png() -> bytes:
    """Builds a tiny valid 1x1 PNG so magic-byte validation passes."""
    def chunk(tag, data):
        c = struct.pack('>I', len(data)) + tag + data
        return c + struct.pack('>I', zlib.crc32(tag + data) & 0xffffffff)
    ihdr = struct.pack('>IIBBBBB', 1, 1, 8, 2, 0, 0, 0)
    idat = zlib.compress(b'\x00\xff\x00\x00')
    return (b'\x89PNG\r\n\x1a\n'
            + chunk(b'IHDR', ihdr) + chunk(b'IDAT', idat) + chunk(b'IEND', b''))


@pytest.fixture
def app(tmp_path):
    test_app = create_app()
    test_app.config.update({
        'TESTING': True,
        'WTF_CSRF_ENABLED': False,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SECRET_KEY': 'test-secret',
        'UPLOAD_FOLDER': str(tmp_path / 'uploads'),
        'NVIDIA_API_KEY': ''})
    os.makedirs(test_app.config['UPLOAD_FOLDER'], exist_ok=True)

    with test_app.app_context():
        db.create_all()

        from app.logic.crypto import generate_encrypted_key_pair
        priv_enc, pub = generate_encrypted_key_pair()
        admin = Investigator(
            full_name='Admin User', email='admin@test.com', role='Admin',
            public_key=pub, private_key_encrypted=priv_enc)
        admin.set_password('Admin@12345!')

        priv_enc2, pub2 = generate_encrypted_key_pair()
        lead = Investigator(
            full_name='Lead User', email='lead@test.com',
            role='Lead Investigator',
            public_key=pub2, private_key_encrypted=priv_enc2)
        lead.set_password('Lead@123456!')

        db.session.add_all([admin, lead])
        db.session.commit()

        yield test_app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    c = app.test_client()
    c.post('/login', data={'email': 'admin@test.com',
                           'password': 'Admin@12345!'},
           follow_redirects=True)
    return c


def _create_case(client) -> int:
    r = client.post('/cases/new', data={
        'title': 'Integration Case',
        'description': 'Created by the integration test',
        'jurisdiction': 'Italy'}, follow_redirects=True)
    assert r.status_code == 200
    case = Case.query.filter_by(title='Integration Case').first()
    assert case is not None
    return case.id


def _upload_evidence(client, app, case_id) -> int:
    r = client.post(f'/cases/{case_id}/evidence/upload', data={
        'title': 'Integration Photo',
        'description': 'A tiny PNG',
        'category': 'Image',
        'location': 'Digital Lab',
        'file': (io.BytesIO(_minimal_png()), 'photo.png')},
        content_type='multipart/form-data', follow_redirects=True)
    assert r.status_code == 200
    ev = EvidenceItem.query.filter_by(title='Integration Photo').first()
    assert ev is not None
    return ev.id


#  Auth 
class TestAuthFlow:
    def test_login_page_renders(self, app):
        r = app.test_client().get('/login')
        assert r.status_code == 200

    def test_bad_credentials_rejected(self, app):
        c = app.test_client()
        r = c.post('/login', data={'email': 'admin@test.com',
                                   'password': 'wrong'},
                   follow_redirects=True)
        assert b'Invalid' in r.data or b'attempt' in r.data

    def test_login_then_logout(self, app):
        c = app.test_client()
        r = c.post('/login', data={'email': 'admin@test.com',
                                   'password': 'Admin@12345!'},
                   follow_redirects=True)
        assert r.status_code == 200
        r = c.get('/logout', follow_redirects=True)
        assert r.status_code == 200

    def test_protected_route_redirects_anonymous(self, app):
        r = app.test_client().get('/cases', follow_redirects=False)
        assert r.status_code in (301, 302)


#  Case CRUD 
class TestCaseFlow:
    def test_create_view_edit_case(self, client, app):
        with app.app_context():
            case_id = _create_case(client)

            r = client.get(f'/cases/{case_id}')
            assert r.status_code == 200
            assert b'Integration Case' in r.data

            r = client.post(f'/cases/{case_id}/edit', data={
                'title': 'Integration Case (renamed)',
                'description': 'updated',
                'jurisdiction': 'Italy',
                'status': 'Active'}, follow_redirects=True)
            assert r.status_code == 200
            assert db.session.get(Case, case_id).title == 'Integration Case (renamed)'

    def test_case_list_shows_created_case(self, client, app):
        with app.app_context():
            _create_case(client)
            r = client.get('/cases')
            assert r.status_code == 200
            assert b'Integration Case' in r.data


#  Evidence upload & custody 
class TestEvidenceCustodyFlow:
    def test_full_evidence_lifecycle(self, client, app):
        with app.app_context():
            case_id = _create_case(client)
            ev_id = _upload_evidence(client, app, case_id)
            ev = db.session.get(EvidenceItem, ev_id)

            # Upload created hash, custody log, and encrypted file at rest
            assert ev.original_hash and len(ev.original_hash) == 64
            logs = CustodyLog.query.filter_by(evidence_id=ev_id).all()
            assert len(logs) >= 1 and logs[0].event_type == 'Upload'
            assert logs[0].digital_signature

            # View evidence page
            r = client.get(f'/cases/{case_id}/evidence/{ev_id}')
            assert r.status_code == 200

            # Transfer custody to the lead investigator (Ed25519-signed)
            lead = Investigator.query.filter_by(email='lead@test.com').first()
            r = client.post(f'/evidence/{ev_id}/transfer', data={
                'to_investigator_id': lead.id,
                'reason': 'Analysis required',
                'location': 'Forensic Lab',
                'justification': 'Integration test transfer'},
                follow_redirects=True)
            assert r.status_code == 200
            transfer = CustodyLog.query.filter_by(
                evidence_id=ev_id, event_type='Transfer').first()
            assert transfer is not None and transfer.digital_signature

            # The transfer moved the item to 'Transferred'; continue the
            # lifecycle: Transferred -> Under Analysis (valid transition)
            r = client.post(f'/evidence/{ev_id}/change-state', data={
                'target_state': 'Under Analysis',
                'justification': 'Analysis started'}, follow_redirects=True)
            assert r.status_code == 200
            assert db.session.get(EvidenceItem, ev_id).lifecycle_state == 'Under Analysis'

            # State change must refresh the multi-factor risk score
            assert db.session.get(EvidenceItem, ev_id).risk_score is not None

    def test_integrity_and_reconstruction_pages(self, client, app):
        with app.app_context():
            case_id = _create_case(client)
            ev_id = _upload_evidence(client, app, case_id)

            r = client.get(f'/evidence/{ev_id}/verify')
            assert r.status_code == 200

            r = client.get(f'/evidence/{ev_id}/verify/json')
            assert r.status_code == 200
            assert b'verdict' in r.data

            r = client.get(f'/evidence/{ev_id}/reconstruct')
            assert r.status_code == 200

            r = client.get(f'/evidence/{ev_id}/custody-log')
            assert r.status_code == 200

    def test_executable_upload_rejected(self, client, app):
        with app.app_context():
            case_id = _create_case(client)
            r = client.post(f'/cases/{case_id}/evidence/upload', data={
                'title': 'Malware',
                'description': 'Renamed executable',
                'category': 'Other',
                'file': (io.BytesIO(b'MZ\x90\x00\x03' + b'\x00' * 64),
                         'innocent.png')},
                content_type='multipart/form-data', follow_redirects=True)
            # The magic-byte check must refuse an EXE disguised as a PNG
            assert EvidenceItem.query.filter_by(title='Malware').first() is None


#  Export (ZIP + PDF) 
class TestExportFlow:
    def test_signed_zip_export(self, client, app):
        with app.app_context():
            case_id = _create_case(client)
            _upload_evidence(client, app, case_id)
            r = client.get(f'/cases/{case_id}/export')
            assert r.status_code == 200
            assert r.mimetype == 'application/zip'

            import zipfile
            zf = zipfile.ZipFile(io.BytesIO(r.data))
            names = zf.namelist()
            assert 'manifest.json' in names
            assert 'audit_trail.txt' in names
            assert 'manifest_signature.hex' in names

    def test_custody_pdf_report(self, client, app):
        with app.app_context():
            case_id = _create_case(client)
            ev_id = _upload_evidence(client, app, case_id)
            r = client.get(f'/evidence/{ev_id}/custody-report.pdf')
            assert r.status_code == 200
            assert r.mimetype == 'application/pdf'
            assert r.data.startswith(b'%PDF')


#  Admin risk settings 
class TestRiskSettingsFlow:
    def test_settings_page_renders(self, client):
        r = client.get('/admin/risk-settings')
        assert r.status_code == 200
        assert b'Factor Weights' in r.data

    def test_settings_update_persists_and_applies(self, client, app, tmp_path):
        from app.logic.risk_scoring import _WEIGHTS, get_weights
        data = {f'weight_{name}': str(value)
                for name, value in _WEIGHTS.items()}
        data['weight_integrity_status'] = '0.50'  # emphasise integrity
        data.update({'threshold_LOW': '0.20',
                     'threshold_MEDIUM': '0.45',
                     'threshold_HIGH': '0.70'})
        r = client.post('/admin/risk-settings', data=data,
                        follow_redirects=True)
        assert r.status_code == 200

        with app.app_context():
            weights = get_weights()
            # Weights are re-normalised; integrity must now dominate
            assert weights['integrity_status'] == max(weights.values())
            assert abs(sum(weights.values()) - 1.0) < 1e-9

        # Clean up the persisted overrides file
        from app.routes.admin import risk_settings_path
        with app.app_context():
            path = risk_settings_path()
        if os.path.exists(path):
            os.remove(path)

    def test_invalid_thresholds_rejected(self, client, app):
        from app.logic.risk_scoring import _WEIGHTS
        data = {f'weight_{name}': str(value)
                for name, value in _WEIGHTS.items()}
        data.update({'threshold_LOW': '0.80',   # not increasing
                     'threshold_MEDIUM': '0.45',
                     'threshold_HIGH': '0.70'})
        r = client.post('/admin/risk-settings', data=data,
                        follow_redirects=True)
        assert b'strictly increasing' in r.data


#  AI assistant hallucination check 
class TestHallucinationCheck:
    def test_unknown_entity_is_flagged(self, app):
        with app.app_context():
            from app.logic.ai_assistant import (AIInvestigationAssistant,
                                                ClassifiedIntent,
                                                IntentCategory,
                                                RetrievedContext)
            assistant = AIInvestigationAssistant()
            intent = ClassifiedIntent(
                category=IntentCategory.CASE_QUERY, confidence=1.0,
                entity_id=1, keywords_matched=['case'])
            context = RetrievedContext(
                intent=intent, records={},
                context_text="Case #1: 'Real Case' | Status: Open")
            flags = assistant.check_hallucinations(
                "Case #1 is open, but Case #99 was closed yesterday.", context)
            assert any('#99' in f for f in flags)
            assert not any('#1 ' in f for f in flags)

    def test_clean_reply_produces_no_flags(self, app):
        with app.app_context():
            from app.logic.ai_assistant import (AIInvestigationAssistant,
                                                ClassifiedIntent,
                                                IntentCategory,
                                                RetrievedContext)
            assistant = AIInvestigationAssistant()
            intent = ClassifiedIntent(
                category=IntentCategory.CASE_QUERY, confidence=1.0,
                entity_id=1, keywords_matched=['case'])
            context = RetrievedContext(
                intent=intent, records={},
                context_text="Case #1: 'Real Case' | Status: Open")
            flags = assistant.check_hallucinations(
                "Case #1 is currently open.", context)
            assert flags == []
