# Chapter 21 — Appendices

---

## Appendix A — User-Story Catalogue

The twenty-seven original stories and the two maintenance change-request stories, with their feature category, MoSCoW priority, story-point estimate and delivering iteration. Acceptance criteria are given in Sections 7.5 and 7.6 and in the planning sections of Chapter 5.

| ID | Title | Category | MoSCoW | Pts | Iteration |
|---|---|---|---|---|---|
| US-01 | Secure login and logout | A / Sec | Must | 3 | 1 |
| US-02 | Role-based access control | A | Must | 5 | 1 |
| US-03 | Case CRUD, search and archive | A | Must | 5 | 1 |
| US-04 | Upload and register evidence | A | Must | 5 | 1 |
| US-05 | SHA-256 fingerprint at upload | B | Must | 2 | 1 |
| US-06 | EXIF / MIME metadata extraction | B | Must | 3 | 1 |
| US-07 | Edit and categorise evidence | A | Must | 3 | 1 |
| US-08 | Record custody transfers and access events | A | Must | 5 | 1 |
| US-09 | Append-only audit trail | A | Must | 5 | 1 |
| US-10 | Formula-based audit checks | A | Should | 3 | 1 |
| US-11 | Admin-only account creation | A | Must | 1 | 1 |
| US-12 | Ed25519-signed custody events | B | Must | 5 | 2 |
| US-13 | Graph integrity verification algorithm | **C** | Must | **13** | 2 |
| US-14 | Evidence lifecycle state machine | **C** | Must | 8 | 2 |
| US-15 | Custody chain reconstruction algorithm | **C** | Must | 8 | 2 |
| US-16 | Integrity verification report UI | A | Should | 2 | 2 |
| US-17 | Chain reconstruction report UI | A | Should | 2 | 2 |
| US-18 | Multi-factor risk scoring algorithm | **C** | Must | 8 | 3 |
| US-19 | Admin-configurable risk weights | C / A | Should | 3 | 3 |
| US-20 | AI assistant orchestration pipeline | **C** | Must | 8 | 3 |
| US-21 | Hallucination detection | **C** | Must | 3 | 3 |
| US-22 | Isolation Forest anomaly detection | B | Could | 5 | 3 |
| US-23 | Risk and anomaly dashboards | A | Should | 3 | 3 |
| US-24 | 2FA, lockout and session timeout | Sec / B | Should | 5 | 3 |
| US-25 | Encryption at rest and magic-byte checks | Sec / B | Should | 3 | 3 |
| US-26 | Tamper-evident signed ZIP export | B | Should | 2 | 3 |
| US-27 | PDF chain-of-custody report | B | Could | 2 | 3 |
| US-28 | Role-scoped dashboard and aggregated views | A / Sec | Must | 5 | M1 |
| US-29 | Access-scoped AI assistant and chat isolation | C / Sec | Must | 5 | M1 |
| | **Total** | | | **130** | |

The M2 defect findings (D1–D6, H1–H3, R1–R2) are catalogued in Table 5.9 rather than as backlog stories, because repairing a defect restores a requirement already accepted rather than introducing a new one.

---

## Appendix B — HTTP Interface Reference

Routes grouped by blueprint. Methods are shown as G (GET) and P (POST). All routes require authentication except the login and one-time-password routes.

| Method | Path | Purpose | Minimum role |
|---|---|---|---|
| G/P | `/login` (and `/`) | Log in | — |
| G | `/logout` | Log out | Any |
| G/P | `/verify-otp` | Second-factor verification | — |
| G/P | `/2fa/setup`, `/2fa/disable` | Enrol or disable TOTP | Any (own account) |
| G | `/dashboard` | Role-tailored dashboard | Any |
| G | `/cases` | List accessible cases (paginated) | Any |
| G/P | `/cases/new` | Create a case | Lead Investigator |
| G | `/cases/<id>` | View a case and its evidence | Case member |
| G/P | `/cases/<id>/edit` | Edit a case | Lead Investigator |
| P | `/cases/<id>/archive` | Archive a case (soft) | Lead Investigator |
| P | `/cases/<id>/members/add`, `/members/remove` | Manage case membership | Lead Investigator |
| G | `/cases/<id>/export` | Download the signed ZIP export | Lead Investigator |
| G/P | `/cases/<id>/evidence/upload` | Upload and register evidence | Analyst |
| G | `/cases/<id>/evidence/<eid>` | View an evidence item | Case member |
| G/P | `/cases/<id>/evidence/<eid>/edit` | Edit evidence metadata | Analyst |
| P | `/cases/<id>/evidence/<eid>/delete` | Soft-delete an evidence item | Lead Investigator |
| G/P | `/evidence/<eid>/transfer` | Record a signed custody transfer | Current holder or Admin |
| G/P | `/evidence/<eid>/change-state` | Trigger a lifecycle transition | Per transition table |
| G | `/evidence/<eid>/custody-log` | View the custody log | Case member |
| G | `/evidence/<eid>/verify` (+ `/verify/json`) | Run graph integrity verification | Analyst |
| G | `/evidence/<eid>/reconstruct` | Run custody-chain reconstruction | Analyst |
| G | `/evidence/<eid>/custody-report.pdf` | Download the PDF custody report | Case member |
| G | `/risk/dashboard` | Risk-ranked evidence (scoped) | Any |
| G | `/risk/anomaly` | Isolation Forest anomaly view | Lead Investigator |
| G | `/risk/evidence/<eid>` (+ `/json`) | Per-item risk report | Case member |
| G | `/audit` | Global audit trail | **Admin only** |
| G | `/audit/evidence/<eid>` (+ `/formula-check`) | Per-item trail and formula checks | Case member |
| G | `/assistant/` | AI assistant chat page | Any |
| P | `/assistant/chat`, `/assistant/clear` | Query the assistant / clear history | Any |
| G | `/admin/users` (+ `/new`) | List or create investigator accounts | **Admin only** |
| P | `/admin/users/<id>/change-role`, `/toggle-active`, `/unlock` | Account management | **Admin only** |
| G/P | `/admin/risk-settings` | Configure risk weights and thresholds | **Admin only** |

---

## Appendix C — Database Schema Reference

The six entities and their principal columns. Primary keys are integer surrogates; unique business keys and foreign keys are noted. The visual form is Figure 8.3.

**INVESTIGATORS**

| Column | Type | Constraints |
|---|---|---|
| id | INTEGER | PK |
| full_name | VARCHAR(150) | NOT NULL |
| email | VARCHAR(150) | NOT NULL, UNIQUE |
| password_hash | VARCHAR(256) | NOT NULL |
| role | ENUM | NOT NULL — Admin, Lead Investigator, Analyst, Read-Only |
| public_key | TEXT | Ed25519 public key |
| private_key_encrypted | TEXT | Fernet-encrypted private key |
| totp_secret | VARCHAR(255) | Nullable — set when 2FA is enrolled |
| is_active | BOOLEAN | NOT NULL |
| failed_login_count | INTEGER | NOT NULL |
| locked_until | DATETIME | Nullable |
| created_at, updated_at | DATETIME | NOT NULL |

**CASES**

| Column | Type | Constraints |
|---|---|---|
| id | INTEGER | PK |
| case_number | VARCHAR(50) | NOT NULL, UNIQUE |
| title | VARCHAR(200) | NOT NULL |
| description | TEXT | |
| jurisdiction | VARCHAR(150) | |
| status | ENUM | NOT NULL — Open, Active, Pending, Closed, Archived |
| is_archived | BOOLEAN | NOT NULL — soft archive |
| date_opened | DATE | NOT NULL |
| date_closed | DATE | Nullable |
| created_by_id | INTEGER | FK → investigators.id, NOT NULL |
| assigned_to_id | INTEGER | FK → investigators.id |

**EVIDENCE_ITEMS**

| Column | Type | Constraints |
|---|---|---|
| id | INTEGER | PK |
| evidence_number | VARCHAR(50) | NOT NULL, UNIQUE |
| case_id | INTEGER | FK → cases.id, NOT NULL |
| title | VARCHAR(200) | NOT NULL |
| category | ENUM | NOT NULL — Image, Video, Audio, Document, Database, Log File, Other |
| lifecycle_state | ENUM | NOT NULL — Collected, Submitted, Under Analysis, Transferred, Archived, Flagged |
| file_name, file_path | VARCHAR | NOT NULL |
| file_size, file_mime_type | BIGINT / VARCHAR(100) | |
| **original_hash** | CHAR(64) | NOT NULL — **immutable ground truth** |
| **current_hash** | CHAR(64) | NOT NULL — latest verified state |
| exif_metadata | TEXT | |
| uploaded_by_id | INTEGER | FK → investigators.id, NOT NULL |
| current_holder_id | INTEGER | FK → investigators.id |
| risk_score, risk_level | FLOAT / ENUM | Written by the risk scorer |
| **integrity_status** | ENUM | VERIFIED / NOT_CHECKED / FAILED — *added in M2* |
| **is_deleted** | BOOLEAN | NOT NULL — soft delete, *added in M2* |

**CUSTODY_LOGS**

| Column | Type | Constraints |
|---|---|---|
| id | INTEGER | PK |
| evidence_id | INTEGER | FK → evidence_items.id, NOT NULL |
| event_type | ENUM | NOT NULL — Upload, Transfer, Access, Verification |
| from_investigator_id, to_investigator_id | INTEGER | FK → investigators.id |
| timestamp | DATETIME | NOT NULL |
| location, reason, notes | VARCHAR / TEXT | |
| file_hash_at_event | CHAR(64) | NOT NULL |
| **digital_signature** | TEXT | **NOT NULL — an unsigned custody record cannot exist** |

**AUDIT_RECORDS** — *updates and deletes are blocked at the ORM layer (append-only)*

| Column | Type | Constraints |
|---|---|---|
| id | INTEGER | PK |
| event_type | ENUM | NOT NULL |
| investigator_id, evidence_id, case_id | INTEGER | FK, nullable |
| description | TEXT | NOT NULL |
| ip_address | VARCHAR(50) | |
| result | ENUM | NOT NULL — Success, Failure, Warning |
| integrity_check_result | TEXT | |
| timestamp | DATETIME | NOT NULL |

**CASE_ACCESS** — *unique on (case_id, investigator_id)*

| Column | Type | Constraints |
|---|---|---|
| id | INTEGER | PK |
| case_id | INTEGER | FK → cases.id, NOT NULL |
| investigator_id | INTEGER | FK → investigators.id, NOT NULL |
| permission | ENUM | NOT NULL — Owner, Member, ReadOnly |
| granted_at | DATETIME | NOT NULL |
| granted_by_id | INTEGER | FK → investigators.id |

---

## Appendix D — Requirements Traceability Matrix

Each functional requirement traced forward to the user story that carries it, the module that implements it, and the test module that verifies it. This is the artefact that makes the validity, consistency and completeness checks of Section 7.12 checkable rather than asserted.

| FR | Story | Implemented in | Verified by | Iteration |
|---|---|---|---|---|
| FR-01, FR-02 | US-01 | `routes/auth.py`, `models/investigator.py` | `test_increment1` | 1 |
| FR-03 | US-01, US-24 | `app/__init__.py` (before_request), `config.py` | `test_increment3` | 1, 3 |
| FR-04, FR-05, FR-06 | US-02 | `models/investigator.py`, `utils/decorators.py` | `test_increment1`, `test_scoping` | 1 |
| FR-07, FR-08 | US-03 | `routes/cases.py`, `models/case.py` | `test_increment1` | 1 |
| FR-09 | US-02, US-28 | `models/case_access.py` | `test_scoping` | 1, M1 |
| FR-10, FR-11, FR-12 | US-04 | `routes/evidence.py`, `logic/validators.py` | `test_increment1` | 1 |
| FR-13 | US-05 | `logic/crypto.py` (`hashlib`) | `test_increment1` | 1 |
| FR-14 | US-06, US-25 | `logic/validators.py` (Pillow, python-magic) | `test_increment1`, `test_increment3` | 1, 3 |
| FR-15 | US-07 | `routes/evidence.py` | `test_increment1` | 1 |
| FR-16, FR-17 | US-08 | `routes/custody.py`, `models/custody_log.py` | `test_increment1`, `test_increment2` | 1 |
| FR-18, FR-19 | US-09 | `models/audit_record.py`, `utils/audit.py` | `test_increment1` | 1 |
| FR-20 | US-10 | `logic/audit_formulas.py` | `test_day2` | 1 |
| FR-21, FR-22 | US-11 | `routes/admin.py`, `logic/crypto.py` | `test_increment1` | 1 |
| FR-23, FR-24 | US-12 | `logic/crypto.py`, `routes/custody.py` | `test_increment2`, `test_day2` | 2 |
| FR-25, FR-26, FR-27 | US-13 | `logic/graph_integrity.py` | `test_increment2` | 2 |
| FR-28, FR-29, FR-30 | US-14 | `logic/state_machine.py` | `test_increment2` | 2 |
| FR-31, FR-32, FR-33 | US-15 | `logic/chain_reconstruction.py` | `test_increment2` | 2 |
| FR-34 | US-16 | `routes/custody.py`, templates | `test_increment2` | 2 |
| FR-35 | US-17 | `routes/custody.py`, templates | `test_increment2` | 2 |
| FR-36, FR-37, FR-38 | US-18 | `logic/risk_scoring.py` | `test_increment3` | 3 |
| FR-39 | US-19 | `routes/admin.py`, `logic/risk_scoring.py` | `test_increment3` | 3 |
| FR-40 | US-20 | `logic/ai_assistant.py` | `test_intent_classifier` | 3 |
| FR-41 | US-20, US-29 | `logic/ai_assistant.py`, `models/case_access.py` | `test_scoping` | 3, M1 |
| FR-42 | US-20 | `logic/ai_assistant.py` | `test_increment3` | 3 |
| FR-43 | US-21 | `logic/ai_assistant.py` | `test_increment3` | 3 |
| FR-44, FR-45 | US-22 | `logic/anomaly_detection.py` (scikit-learn) | `test_increment3` | 3 |
| FR-46 | US-23 | `routes/risk.py`, `routes/dashboard.py` | `test_increment3` | 3 |
| FR-47 | US-24 | `routes/auth.py`, `config.py` (PyOTP) | `test_increment3` | 3 |
| FR-48 | US-25 | `logic/file_crypto.py`, `logic/keyderive.py` | `test_increment3` | 3 |
| FR-49 | US-26 | `routes/export.py` | `test_increment3`, `test_integration` | 3 |
| FR-50 | US-27 | `logic/pdf_report.py` (ReportLab) | `test_integration` | 3 |
| FR-51, FR-52 | US-28 | `models/case_access.py`, `routes/dashboard.py` | `test_scoping` | M1 |
| FR-53 | US-29 | `logic/ai_assistant.py` | `test_intent_classifier` | M1 |
| FR-54 | US-29 | `routes/assistant.py`, `routes/auth.py` | `test_scoping` | M1 |
| FR-55 | D1 | `models/evidence.py`, `routes/evidence.py` | `test_integration` | M2 |
| FR-56 | D2 | `models/evidence.py`, `logic/graph_integrity.py` | `test_integration` | M2 |

**Coverage of the matrix:** all 56 functional requirements trace to at least one implementing module and at least one verifying test module. No requirement is unimplemented, and none is unverified.

---

## Appendix E — Glossary and Acronyms

**AES-256-GCM** — Advanced Encryption Standard, 256-bit key, Galois/Counter Mode; an authenticated encryption scheme used for evidence at rest. Provides both confidentiality and tamper-detection.

**Append-only** — a persistence discipline in which records may be inserted but never updated or deleted. Enforced in DEICMS at the ORM layer.

**Burndown chart** — a plot of remaining story points against time across an iteration, with an ideal line for comparison. The instrument by which process timeliness is made visible.

**Chain of custody** — the documented, unbroken record of who has held an item of evidence and what was done to it; required for legal admissibility.

**Cohesion** — the degree to which the elements of a module belong together. High cohesion is desirable.

**Coupling** — the degree of interaction between modules. Low coupling is desirable.

**COTS** — Commercial Off-The-Shelf; a large-scale existing system reused rather than built.

**CSP** — Content-Security-Policy; an HTTP header restricting the origins from which a page may load resources.

**CSRF** — Cross-Site Request Forgery; an attack in which a user is tricked into submitting an unwanted state-changing request.

**DAG** — Directed Acyclic Graph; the in-memory structure into which the custody history is built for verification.

**DEICMS** — Digital Evidence Integrity & Chain-of-Custody Management System; this project.

**DevOps** — a set of practices unifying development and operations, characterised by continuous integration, continuous delivery, infrastructure as code and monitoring.

**DFS** — Depth-First Search; the traversal used by the graph integrity verifier.

**Ed25519** — an Edwards-curve digital signature scheme used to sign custody events; chosen for its strong security margin and small keys.

**EXIF** — Exchangeable Image File Format; metadata embedded in image files.

**Fail-visible** — an error-handling posture in which a failure is recorded and made conspicuous rather than silently absorbed (fail-silent) or blocking the operation entirely (fail-closed).

**Fernet** — an authenticated symmetric-encryption token format used to protect private keys at rest.

**HSTS** — HTTP Strict-Transport-Security; a header preventing fallback from HTTPS to HTTP.

**IDOR** — Insecure Direct Object Reference; an access-control flaw in which an object is reached by identifier without verifying the requester's right to it. Fixed as M2 finding D3.

**Isolation Forest** — an unsupervised machine-learning algorithm for anomaly detection, used to flag statistical outliers among evidence items.

**Lehman's laws** — eight empirical observations about how software systems evolve, applied in Section 14.2.

**LLM** — Large Language Model; the pre-trained model underlying the AI assistant.

**MDE** — Model-Driven Engineering; an approach in which models are the primary artefacts and code is generated from them. *Not* practised in this project.

**MIME** — Multipurpose Internet Mail Extensions; the content-type of a file, validated in DEICMS against its magic bytes rather than its extension.

**MoSCoW** — a prioritisation scheme: Must have, Should have, Could have, Won't have this time.

**NIM** — NVIDIA Inference Microservices; the OpenAI-compatible endpoint through which the language model is consumed.

**ORM** — Object-Relational Mapper; SQLAlchemy, mapping Python objects to database rows.

**Plausibility threshold** — the minimum score (0.40) a candidate must reach before the reconstruction algorithm will infer a custody link rather than mark the gap unresolved.

**SHA-256** — Secure Hash Algorithm producing a 256-bit fingerprint, used for evidence file integrity.

**Story point** — a unit of relative size on a Fibonacci scale (1, 2, 3, 5, 8, 13), used in estimation. Independent of MoSCoW priority.

**TDD** — Test-Driven Development; writing a test before the code that satisfies it.

**TOTP** — Time-based One-Time Password; the second authentication factor.

**V-model** — a refinement of the waterfall model pairing each construction phase with the test level that validates it.

**Velocity** — the number of story points a team delivers in one iteration; an observed property, not a target.

**WAL** — Write-Ahead Log; SQLite's journaling mode, relevant to inspecting the live database (see `flush_db.py`).

**XSS** — Cross-Site Scripting; an injection attack whose stored variant in the chat interface was fixed as M2 finding H1.

---

*[End of Report]*
