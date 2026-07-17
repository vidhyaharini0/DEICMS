"""
Unit tests for the AI assistant's intent classifier (Stage 1 of the
orchestration pipeline).

These are pure-logic tests: classify_intent() does not touch the database or
the LLM, so they run without an app context. They pin the expected intent for
representative queries and lock in the deterministic tie-break behaviour, so a
future keyword change that silently reshuffles classifications is caught.

Run with:  pytest tests/test_intent_classifier.py -v
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.logic.ai_assistant import AIInvestigationAssistant, IntentCategory


A = AIInvestigationAssistant()


def test_identity_shortcircuits():
    for msg in ["Who am I?", "show my cases", "what is assigned to me"]:
        assert A.classify_intent(msg).category == IntentCategory.IDENTITY


def test_integrity_query():
    r = A.classify_intent("has evidence 5 been tampered with? verify the hash")
    assert r.category == IntentCategory.INTEGRITY_QUERY
    assert r.entity_id == 5


def test_custody_query():
    r = A.classify_intent("who had custody of the item and what transfers happened")
    assert r.category == IntentCategory.CUSTODY_QUERY


def test_risk_query():
    assert A.classify_intent("what is the risk score for this evidence") \
        .category in (IntentCategory.RISK_QUERY, IntentCategory.EVIDENCE_QUERY)


def test_case_query_with_entity_id():
    r = A.classify_intent("show me case 3")
    assert r.category == IntentCategory.CASE_QUERY
    assert r.entity_id == 3


def test_general_forensics():
    r = A.classify_intent("explain the best practice protocol for evidence handling")
    assert r.category in (IntentCategory.GENERAL_FORENSICS, IntentCategory.EVIDENCE_QUERY)


def test_unknown_when_no_keywords():
    r = A.classify_intent("hello there, nice weather today")
    assert r.category == IntentCategory.UNKNOWN
    assert r.confidence == 0.0


def test_entity_id_hash_form():
    assert A.classify_intent("evidence #7 details").entity_id == 7


def test_classification_is_deterministic():
    # Same input must always yield the same category (no dict-order dependence).
    msg = "custody transfer and integrity of evidence 2"
    first = A.classify_intent(msg).category
    for _ in range(20):
        assert A.classify_intent(msg).category == first


def test_confidence_bounded():
    r = A.classify_intent("integrity hash verify tamper custody transfer risk")
    assert 0.0 <= r.confidence <= 1.0
