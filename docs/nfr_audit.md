# NFR Audit - evidence of enforcement, as of 3 November 2026

Method: each NFR in Table 7.6 of the v2 report was checked against (a) the code
that enforces it and (b) an automated test that would fail if the enforcement
were removed. "Tested" below means an automated test exists; a manual check,
a configuration review or an analytical argument does not count.

## Summary

| Verdict | Count | NFRs |
|---|---|---|
| Implemented and automatically tested | 8 | 01, 02, 03, 04, 05, 07, 12, 18 |
| Implemented but **not** tested | 7 | 06, 08, 09, 13, 14, 15, 16 |
| Asserted analytically, never measured | 2 | 10, 11 |
| **Claim does not match the code** | 1 | 17 |

Only **8 of 18** NFRs are backed by a test that would fail on regression.

## Detail

| NFR | Property | Enforced in code? | Automated test? | Action |
|---|---|---|---|---|
| 01 | Case-scoped confidentiality | Yes - `accessible_case_ids` | Yes - `test_scoping` (14) | Keep; add exhaustive route-matrix test |
| 02 | Hash verifiability | Yes - `graph_integrity` | Yes - `test_increment2` | Keep |
| 03 | Non-repudiation | Yes - Ed25519 | Yes - `test_increment2` | Keep |
| 04 | Append-only audit | Yes - ORM listeners | Yes - `test_increment1` | Keep |
| 05 | Degraded-mode availability | Yes - assistant fallback | Yes - `test_increment3` | Keep |
| 06 | Clean timeout on slow model | Yes - 20s/60s/90s budgets | **No** | Add timeout test with a stubbed slow client |
| 07 | Role-matched interface | Yes - `panels` dict | Partial - `test_scoping` | Add per-role panel assertions |
| 08 | Modular localisability | Yes - by convention | **No** | Add import-boundary test (logic imports no Flask) |
| 09 | Engine portability | Yes - by convention | **No** | Add test asserting no engine-specific SQL |
| 10 | Verification O(V+E) | n/a - analytical | **No measurement** | Add scaling benchmark |
| 11 | Risk scoring O(n) | n/a - analytical | **No measurement** | Add scaling benchmark |
| 12 | Password strength | Yes - 12 chars | Yes - `test_increment3` | Keep |
| 13 | Session cookie flags | Yes - `config.py` 65-73 | **No** | Add cookie-flag assertions |
| 14 | Security headers | Yes - `app/__init__.py` 99-129 | **No** | Add header-presence test |
| 15 | No markup from untrusted text | Yes - `escapeHtml`, chat.html 111 | **No** | Add stored-XSS regression test (this was M2 finding H1 - a fixed defect with no regression test) |
| 16 | Refuse insecure defaults | Yes - `config.py` 134-160 | **No** | Add production-profile raises test |
| 17 | Listings remain responsive | **Partly** - cases and audit paginate; **evidence listing in `view_case` calls `.all()`** | **No** | Implement evidence pagination, then test |
| 18 | Offline test suite | Yes | Yes - suite runs | Keep |

## The one real correctness issue

`app/routes/cases.py`, `view_case()`:

```python
evidence_items = (case.evidence_items
              .filter_by(is_deleted=False)
              .order_by(EvidenceItem.created_at.desc())
              .all())
```

NFR-17 in the report states "Case **and evidence** listings paginated". Cases
and audit records are paginated; the evidence listing inside a case is not.
The requirement as written is not met, so either the code changes or the
requirement does. The code should change - an evidence-heavy case is exactly
the realistic scenario.

## Planned additions

A new `tests/test_nfr.py` holding one test class per quality attribute, so the
report can cite a named test against every NFR acceptance criterion:

- `TestSecurityHeaders` - NFR-13, 14
- `TestInjectionResistance` - NFR-15
- `TestConfigurationSafety` - NFR-16
- `TestPerformanceScaling` - NFR-10, 11, 17 (measured, with thresholds)
- `TestRobustness` - NFR-06
- `TestArchitecturalBoundaries` - NFR-08, 09
- `TestRoleInterfaces` - NFR-07
